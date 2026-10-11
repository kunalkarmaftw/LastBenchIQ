import { useState, type FormEvent } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { messageFor, signup, type SignupInput } from '../api/auth';
import { useAuth } from '../auth/AuthContext';
import AuthLayout from '../components/AuthLayout';
import PasswordField from '../components/PasswordField';

const DIGITS_ONLY = /^\d{8,15}$/;

export default function Signup() {
  const { signIn } = useAuth();
  const navigate = useNavigate();
  const [f, setF] = useState({
    enrollment_number: '', email: '', password: '', name: '',
    college: '', branch: '', graduation_year: '',
  });
  const [error, setError] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);

  const set = (k: keyof typeof f) => (e: { target: { value: string } }) =>
    setF((p) => ({ ...p, [k]: e.target.value }));

  // Validated here as well as on the server, so a typo is caught before a
  // round trip rather than after it.
  const cleaned = f.enrollment_number.replace(/[\s-]/g, '');
  const enrollmentOk = DIGITS_ONLY.test(cleaned);
  const showEnrollmentHint = f.enrollment_number.length > 0 && !enrollmentOk;

  async function onSubmit(e: FormEvent) {
    e.preventDefault();
    setError(null);
    if (!enrollmentOk) { setError('Enrollment number must be 8 to 15 digits.'); return; }
    if (f.password.length < 8) { setError('Password must be at least 8 characters.'); return; }

    setBusy(true);
    try {
      const body: SignupInput = {
        enrollment_number: cleaned,
        email: f.email,
        password: f.password,
        name: f.name,
      };
      if (f.college.trim()) body.college = f.college.trim();
      if (f.branch.trim()) body.branch = f.branch.trim();
      if (f.graduation_year.trim()) body.graduation_year = Number(f.graduation_year);

      const res = await signup(body);
      signIn(res.access_token, res.user);
      navigate('/');
    } catch (err) {
      setError(messageFor(err));
    } finally {
      setBusy(false);
    }
  }

  return (
    <AuthLayout>
      <h1 className="auth-title">Create your account</h1>
      <p className="auth-sub">
        Your enrollment number is your account. It is unique to you, so no one else
        can register with it.
      </p>

      <form onSubmit={onSubmit} className="auth-form">
        <label htmlFor="enrollment">Enrollment number</label>
        <input
          id="enrollment" name="enrollment" inputMode="numeric" autoComplete="username"
          placeholder="03514902024" value={f.enrollment_number} required
          aria-invalid={showEnrollmentHint} onChange={set('enrollment_number')}
        />
        <p className="auth-hint" data-bad={showEnrollmentHint}>
          {showEnrollmentHint
            ? 'That does not look right — it should be 8 to 15 digits.'
            : 'Spaces and dashes are fine; we clean them up.'}
        </p>

        <label htmlFor="name">Full name</label>
        <input id="name" name="name" autoComplete="name" value={f.name} required onChange={set('name')} />

        <label htmlFor="email">Email</label>
        <input id="email" name="email" type="email" autoComplete="email" value={f.email} required onChange={set('email')} />

        <label htmlFor="password">Password</label>
        <PasswordField
          id="password"
          value={f.password}
          onChange={(v) => setF((prev) => ({ ...prev, password: v }))}
          autoComplete="new-password"
          minLength={8}
        />
        <p className="auth-hint">At least 8 characters.</p>

        <div className="auth-row">
          <div>
            <label htmlFor="branch">Branch</label>
            <input id="branch" name="branch" placeholder="BCA" value={f.branch} onChange={set('branch')} />
          </div>
          <div>
            <label htmlFor="grad">Graduating</label>
            <input
              id="grad" name="grad" inputMode="numeric" placeholder="2027"
              value={f.graduation_year} onChange={set('graduation_year')}
            />
          </div>
        </div>

        <label htmlFor="college">College</label>
        <input id="college" name="college" value={f.college} onChange={set('college')} />

        {error && <p role="alert" className="auth-error">{error}</p>}

        <button type="submit" className="auth-btn" disabled={busy}>
          {busy ? 'Creating account…' : 'Create account'}
        </button>
      </form>

      <p className="auth-alt">
        Already registered? <Link to="/login">Sign in</Link>
      </p>
    </AuthLayout>
  );
}
