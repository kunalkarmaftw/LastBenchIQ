import type { CSSProperties, ReactNode } from 'react';
import Logo from './Logo';
import MorphField from './MorphField';
import ShowcaseReel from './ShowcaseReel';

/**
 * The shell both auth pages sit in: brand on the left, form card on the right,
 * stacked on a phone.
 *
 * Shared rather than copied into each page so the two screens cannot drift
 * apart — a sign-in page that looks subtly different from sign-up is the kind
 * of thing nobody notices until a demo.
 */

/**
 * Slow embers rising through the empty space beside the card. Positions and
 * timings are spread by hand rather than randomised, so the field looks
 * composed instead of clumped, and so it renders identically every load —
 * a random field makes screenshot comparisons useless.
 *
 * `left` is a percentage of the shell, `delay` and `dur` are seconds.
 */
const EMBERS = [
  { left: 62, delay: 0, dur: 19, size: 3 },
  { left: 71, delay: 6.5, dur: 24, size: 2 },
  { left: 78, delay: 2.2, dur: 21, size: 4 },
  { left: 84, delay: 11, dur: 26, size: 2 },
  { left: 90, delay: 4.4, dur: 18, size: 3 },
  { left: 95, delay: 14, dur: 23, size: 2 },
  { left: 67, delay: 16.5, dur: 27, size: 2 },
  { left: 88, delay: 8.8, dur: 20, size: 3 },
];

export default function AuthLayout({ children }: { children: ReactNode }) {
  return (
    <div className="auth-shell">
      {/* Two drifting dot grids and two red glows, out of phase so the page
          never sits still. All CSS: no JavaScript, no main-thread repaints. */}
      <div className="dots" aria-hidden="true" />
      <div className="dots dots-far" aria-hidden="true" />
      <div className="glow" aria-hidden="true" />
      <div className="glow glow-right" aria-hidden="true" />
      <MorphField />

      <div className="embers" aria-hidden="true">
        {EMBERS.map((e, i) => (
          <span
            key={i}
            className="ember"
            style={
              {
                '--x': `${e.left}%`,
                '--delay': `${e.delay}s`,
                '--dur': `${e.dur}s`,
                '--size': `${e.size}px`,
              } as CSSProperties
            }
          />
        ))}
      </div>

      <div className="auth-grid">
        <div className="brand-head">
          <Logo size={34} scale={1.3} />

          <h1 className="brand-line">
            The topics that carry the <em>marks</em>.
          </h1>

          <p className="brand-sub">
            LastBenchIQ reads your own past papers, ranks every topic by the marks it
            actually carries, and checks that ranking against this year&rsquo;s syllabus.
          </p>

          <ShowcaseReel />
        </div>

        <div className="card-wrap">
          {/* A soft halo bleeding out past the card. It has to live outside the
              card, because the card clips its own overflow to make the edge
              light work. */}
          <span className="card-halo" aria-hidden="true" />

          <div className="auth-card">
            {/* A light that travels the card's edge: a large conic gradient
                rotating behind an inset panel, so only the ring of it shows.
                Rotating an element works everywhere; animating a gradient's
                angle needs @property, which does not. */}
            <span className="card-edge" aria-hidden="true" />
            <div className="auth-card-in">{children}</div>
          </div>
        </div>
      </div>
    </div>
  );
}
