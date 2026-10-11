import { useState, type FormEvent } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { login, messageFor } from '../api/auth';
import { useAuth } from '../auth/AuthContext';
import AuthLayout from '../components/AuthLayout';
import PasswordField from '../components/PasswordField';

export default function Login() {
  const { signIn } = useAuth();
  const navigate = useNavigate();
  const [enrollment, setEnrollment] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);

  async function onSubmit(e: FormEvent) {
    e.preventDefault();
    setError(null);
    setBusy(true);
    try {
      const res = await login(enrollment, password);
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
      <h1 className="auth-title">Sign in</h1>
      <p className="auth-sub">Use the enrollment number printed on your ID card.</p>

      <form onSubmit={onSubmit} className="auth-form">
        <label htmlFor="enrollment">Enrollment number</label>
        <input
          id="enrollment" name="enrollment" inputMode="numeric" autoComplete="username"
          placeholder="03514902024" value={enrollment} required
          onChange={(e) => setEnrollment(e.target.value)}
        />

        <label htmlFor="password">Password</label>
        <PasswordField
          id="password"
          value={password}
          onChange={setPassword}
          autoComplete="current-password"
        />

        {error && <p role="alert" className="auth-error">{error}</p>}

        <button type="submit" className="auth-btn" disabled={busy}>
          {busy ? 'Signing in…' : 'Sign in'}
        </button>
      </form>

      <p className="auth-alt">
        New here? <Link to="/signup">Create an account</Link>
      </p>
    </AuthLayout>
  );
}
