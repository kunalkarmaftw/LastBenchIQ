import { useState } from 'react';

/**
 * A password input with a reveal toggle.
 *
 * Details that matter and are easy to get wrong:
 *  - `type="button"`, or the toggle submits the form on every click.
 *  - The label is "Show password" / "Hide password", not "eye". A screen
 *    reader user needs the action, not the icon.
 *  - `aria-pressed` carries the on/off state, so it is announced as a toggle.
 *  - The toggle is never inside a <label>, which would focus the input and
 *    swallow the click on some browsers.
 *  - Revealing is per-field and resets on every page load; the password is
 *    never written anywhere to remember the choice.
 */

type Props = {
  id: string;
  value: string;
  onChange: (v: string) => void;
  /** "current-password" on sign-in, "new-password" on sign-up. */
  autoComplete: 'current-password' | 'new-password';
  minLength?: number;
};

export default function PasswordField({ id, value, onChange, autoComplete, minLength }: Props) {
  const [shown, setShown] = useState(false);

  return (
    <div className="pw">
      <input
        id={id}
        name={id}
        type={shown ? 'text' : 'password'}
        autoComplete={autoComplete}
        value={value}
        required
        minLength={minLength}
        onChange={(e) => onChange(e.target.value)}
      />
      <button
        type="button"
        className="pw-eye"
        onClick={() => setShown((s) => !s)}
        aria-pressed={shown}
        aria-controls={id}
        aria-label={shown ? 'Hide password' : 'Show password'}
        title={shown ? 'Hide password' : 'Show password'}
      >
        <Eye open={shown} />
      </button>
    </div>
  );
}

/** One eye, with a slash drawn across it when the password is visible. */
function Eye({ open }: { open: boolean }) {
  return (
    <svg viewBox="0 0 24 24" width="18" height="18" fill="none" aria-hidden="true">
      <path
        d="M2.2 12S5.8 5.5 12 5.5 21.8 12 21.8 12 18.2 18.5 12 18.5 2.2 12 2.2 12Z"
        stroke="currentColor"
        strokeWidth="1.6"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
      <circle cx="12" cy="12" r="3.1" stroke="currentColor" strokeWidth="1.6" />
      {open && (
        <path d="M4 20 20 4" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" />
      )}
    </svg>
  );
}
