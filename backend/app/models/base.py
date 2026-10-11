"""Declarative base and the mixins every table is built from.

`UserOwnedMixin` exists because of a finding in the Step 3 audit: the data model
stated "every user-owned table is filtered by user_id — no exceptions" and then
omitted the column from seven child tables. Routes take bare UUIDs, so a handler
that forgot to join through to `users` would have leaked another student's data.

Making it a mixin turns that rule from a sentence in a document into something
the schema enforces.
"""

import uuid
from datetime import UTC, datetime
from typing import ClassVar

from sqlalchemy import DateTime, ForeignKey, Index, func
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import DeclarativeBase, Mapped, declared_attr, mapped_column


class Base(DeclarativeBase):
    """Base class for all ORM models."""


class IDMixin:
    @declared_attr.directive
    def id(cls) -> Mapped[uuid.UUID]:  # noqa: N805
        return mapped_column(PGUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)


class TimestampMixin:
    @declared_attr.directive
    def created_at(cls) -> Mapped[datetime]:  # noqa: N805
        return mapped_column(
            DateTime(timezone=True),
            server_default=func.now(),
            default=lambda: datetime.now(UTC),
            nullable=False,
        )


class UserOwnedMixin:
    """Adds an indexed, non-null `user_id` to any table that holds student data.

    Denormalised deliberately: a child row carries its owner even when it is
    several levels below `users`. One column, and an entire class of
    broken-access-control bug disappears.
    """

    # Declared by the concrete model; named here so the mixin type-checks.
    __tablename__: ClassVar[str]

    @declared_attr.directive
    def user_id(cls) -> Mapped[uuid.UUID]:  # noqa: N805
        return mapped_column(
            PGUUID(as_uuid=True),
            ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
            index=True,
        )

    @declared_attr.directive
    def __table_args__(cls) -> tuple[Index, ...]:  # noqa: N805
        return (Index(f"ix_{cls.__tablename__}_user_created", "user_id", "created_at"),)
