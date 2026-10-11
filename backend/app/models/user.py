"""User and StudentProfile models.

`StudentProfile` is separate from `User` because its columns are the Placement
Predictor's feature vector, and they must be **derived from the chosen dataset**
rather than invented (DATA_MODEL §1). Keeping them in their own table makes that
dependency explicit: when the dataset is fixed, this table changes and `users`
does not.

The columns below follow the standard campus-placement dataset shape. Confirm
against the actual dataset before the migration is considered final.
"""

import enum
import uuid
from decimal import Decimal

from sqlalchemy import Boolean, Enum, ForeignKey, Integer, Numeric, String
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, IDMixin, TimestampMixin

# SQLAlchemy resolves these annotations at runtime, so `uuid` and `Decimal`
# must be imported for real - a TYPE_CHECKING-only import fails at mapper
# configuration with "Could not resolve all types within mapped annotation".


class CareerGoal(enum.StrEnum):
    MBA = "mba"
    JOB = "job"
    UNDECIDED = "undecided"


class User(Base, IDMixin, TimestampMixin):
    __tablename__ = "users"

    # The student's university enrollment number is the account's real identity.
    # Email changes and gets shared; an enrollment number is issued once, is
    # unique across the university, and is the number a student already knows by
    # heart. It is what they sign in with.
    enrollment_number: Mapped[str] = mapped_column(String(32), unique=True, index=True)

    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    name: Mapped[str] = mapped_column(String(120))

    college: Mapped[str | None] = mapped_column(String(200), nullable=True)
    branch: Mapped[str | None] = mapped_column(String(80), nullable=True)
    graduation_year: Mapped[int | None] = mapped_column(Integer, nullable=True)

    career_goal: Mapped[CareerGoal] = mapped_column(
        # values_callable stores the enum VALUES ("mba") rather than the member
        # NAMES ("MBA"), which is SQLAlchemy's default. Without it the database
        # holds "MBA" while the API speaks "mba", and every round-trip needs a
        # translation that will eventually be forgotten somewhere.
        Enum(CareerGoal, name="career_goal", values_callable=lambda e: [m.value for m in e]),
        default=CareerGoal.UNDECIDED,
        server_default=CareerGoal.UNDECIDED.value,
    )
    target_role: Mapped[str | None] = mapped_column(String(120), nullable=True)

    profile: Mapped["StudentProfile | None"] = relationship(
        back_populates="user", uselist=False, cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<User {self.email}>"


class StudentProfile(Base, IDMixin, TimestampMixin):
    """Feature vector for the Placement Predictor."""

    __tablename__ = "student_profiles"

    user_id: Mapped[uuid.UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        index=True,
    )

    ssc_percentage: Mapped[Decimal | None] = mapped_column(Numeric(5, 2), nullable=True)
    hsc_percentage: Mapped[Decimal | None] = mapped_column(Numeric(5, 2), nullable=True)
    degree_percentage: Mapped[Decimal | None] = mapped_column(Numeric(5, 2), nullable=True)
    degree_stream: Mapped[str | None] = mapped_column(String(80), nullable=True)
    work_experience: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    entrance_test_percentage: Mapped[Decimal | None] = mapped_column(Numeric(5, 2), nullable=True)
    specialisation: Mapped[str | None] = mapped_column(String(80), nullable=True)

    user: Mapped[User] = relationship(back_populates="profile")

    # Every column the model consumes. Kept as one list so `is_complete` can
    # never drift from the feature set the predictor actually needs.
    REQUIRED_FIELDS = (
        "ssc_percentage",
        "hsc_percentage",
        "degree_percentage",
        "degree_stream",
        "work_experience",
    )

    @property
    def is_complete(self) -> bool:
        """True only when every model input is present.

        The Career Agent checks this before calling `predict_placement`.
        Predicting from nulls would produce a confident number from nothing.
        """
        return all(getattr(self, f) is not None for f in self.REQUIRED_FIELDS)

    @property
    def missing_fields(self) -> list[str]:
        return [f for f in self.REQUIRED_FIELDS if getattr(self, f) is None]
