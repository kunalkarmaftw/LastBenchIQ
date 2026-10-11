import { useAuth } from '../auth/AuthContext';
import { ApiStatus } from '../components/ApiStatus';
import Logo from '../components/Logo';

export default function Dashboard() {
  const { user, signOut } = useAuth();
  if (!user) return null;

  const goal =
    user.career_goal === 'mba' ? 'Higher studies'
    : user.career_goal === 'job' ? 'Placement'
    : 'Not set yet';

  return (
    <>
      <header className="app-bar">
        <div className="app-bar-in">
          <Logo size={26} scale={1} />
          <button className="link-btn" onClick={signOut}>Sign out</button>
        </div>
      </header>

      <div className="page">
        <div className="page-top">
          <div>
            <h1 className="page-title">Welcome, {user.name.split(' ')[0]}</h1>
            <p className="page-sub">
              Signed in as <span className="mono accent">{user.enrollment_number}</span>
            </p>
          </div>
        </div>

        <section className="card">
          <h2 className="card-title">Your account</h2>
          <dl className="kv">
            <div><dt>Enrollment number</dt><dd className="mono">{user.enrollment_number}</dd></div>
            <div><dt>Email</dt><dd>{user.email}</dd></div>
            <div><dt>Branch</dt><dd>{user.branch ?? '—'}</dd></div>
            <div><dt>Graduating</dt><dd>{user.graduation_year ?? '—'}</dd></div>
            <div><dt>College</dt><dd>{user.college ?? '—'}</dd></div>
            <div><dt>Goal</dt><dd>{goal}</dd></div>
          </dl>
        </section>

        <section className="card">
          <h2 className="card-title">Next</h2>
          <p className="card-note">
            Upload your past question papers to see which topics carry the most marks.
            Paper upload is the next feature being built.
          </p>
          <ApiStatus />
        </section>
      </div>
    </>
  );
}
