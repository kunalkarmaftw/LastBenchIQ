/**
 * The LastBenchIQ mark.
 *
 * Four seats in a row, rising left to right, with the last one — the back
 * bench — red and tallest. It reads as a bar chart because that is literally
 * what the product does: rank what carries the most marks. The baseline is the
 * bench itself.
 *
 * Drawn as SVG rather than a PNG so it stays sharp on a projector, costs ~1KB,
 * and takes its red from the theme instead of baking a colour into a file.
 */

type MarkProps = {
  /** Rendered size in px. The viewBox is square, so this is width and height. */
  size?: number;
};

export function LogoMark({ size = 32 }: MarkProps) {
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 32 32"
      fill="none"
      role="img"
      aria-label="LastBenchIQ"
    >
      {/* The three front rows: present, but not the point. */}
      <g fill="currentColor" opacity="0.38">
        <rect x="2" y="18" width="6" height="10" rx="1.6" />
        <rect x="9" y="14.5" width="6" height="13.5" rx="1.6" />
        <rect x="16" y="11" width="6" height="17" rx="1.6" />
      </g>
      {/* The last bench. */}
      <rect x="23" y="5" width="6" height="23" rx="1.6" fill="var(--red)" />
      {/* The bench line they all sit on. */}
      <rect x="1" y="29.4" width="30" height="1.6" rx="0.8" fill="var(--red)" opacity="0.55" />
    </svg>
  );
}

type LogoProps = MarkProps & {
  /** Font size of the wordmark in rem. */
  scale?: number;
};

export default function Logo({ size = 30, scale = 1.12 }: LogoProps) {
  return (
    <span className="logo">
      <LogoMark size={size} />
      <span className="logo-word" style={{ fontSize: `${scale}rem` }}>
        LastBench<span className="logo-iq">IQ</span>
      </span>
    </span>
  );
}
