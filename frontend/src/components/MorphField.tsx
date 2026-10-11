import { useEffect, useRef } from 'react';

/**
 * A wireframe solid that morphs between four shapes, with smaller solids on
 * dotted orbits around it. Drawn on a 2D canvas with hand-written 3D maths.
 *
 * Why not three.js: it is ~160KB gzipped and a WebGL context, for one
 * decorative object behind a login form. All this needs is a parametric
 * surface, two rotation matrices and a perspective divide — about 120 lines.
 * Keeping it means the bundle stays small and every line is explainable.
 *
 * The shapes come from the Gielis superformula, which produces spheres, stars,
 * rounded cubes and flowers from one equation by changing four numbers. Morphing
 * is therefore just interpolating those numbers, not interpolating meshes.
 *
 *   r(a) = ( |cos(m·a/4)|^n2 + |sin(m·a/4)|^n3 ) ^ (-1/n1)
 */

type Shape = { m: number; n1: number; n2: number; n3: number };

const ROUND: Shape = { m: 0, n1: 1, n2: 1, n3: 1 };

/**
 * A solid is two profiles, not one: `u` is swept around the equator, `v` from
 * pole to pole. Using the same starred profile for both multiplies the spikes
 * together and the result is needles rather than lobes — so a star here is a
 * starred equator with a round pole-to-pole profile.
 */
type Preset = { u: Shape; v: Shape };

/** The fallback, named so nothing downstream needs a non-null assertion. */
const SPHERE: Preset = { u: ROUND, v: ROUND };

/** Four presets. Order is the loop order. */
const SHAPES: Preset[] = [
  SPHERE,                                                        // the whole syllabus
  { u: { m: 6, n1: 0.55, n2: 0.6, n3: 0.6 }, v: ROUND },         // lobed star
  { u: { m: 4, n1: 11, n2: 14, n3: 14 },
    v: { m: 4, n1: 11, n2: 14, n3: 14 } },                       // rounded cube
  { u: { m: 5, n1: 1.1, n2: 1.4, n3: 1.4 },
    v: { m: 3, n1: 2.2, n2: 5, n3: 5 } },                        // flower
];

/** Line colour by depth bucket: far, middle, near. A tuple, so index 0 is
    statically known to exist and needs no assertion. */
const DEPTH_STYLES: readonly [string, string, string] = [
  'rgba(196,43,43,0.16)',
  'rgba(255,77,77,0.34)',
  'rgba(255,138,138,0.62)',
];

const SEG_U = 40; // longitude steps
const SEG_V = 20; // latitude steps
const DWELL = 4200; // ms per shape — matched to the showcase reel beside it
const BLEND = 1400; // ms of morph between two shapes

/** One superformula radius. */
function superR(angle: number, s: Shape): number {
  const t = (s.m * angle) / 4;
  const a = Math.abs(Math.cos(t)) ** s.n2;
  const b = Math.abs(Math.sin(t)) ** s.n3;
  const sum = a + b;
  if (sum === 0) return 0;
  return sum ** (-1 / s.n1);
}

function lerpOne(a: Shape, b: Shape, e: number): Shape {
  return {
    m: a.m + (b.m - a.m) * e,
    n1: a.n1 + (b.n1 - a.n1) * e,
    n2: a.n2 + (b.n2 - a.n2) * e,
    n3: a.n3 + (b.n3 - a.n3) * e,
  };
}

function lerpShape(a: Preset, b: Preset, t: number): Preset {
  // smoothstep, so the morph eases in and out instead of starting abruptly
  const e = t * t * (3 - 2 * t);
  return { u: lerpOne(a.u, b.u, e), v: lerpOne(a.v, b.v, e) };
}

type Pt = { x: number; y: number; d: number };

/** Small solids that orbit the main shape: [vertices, edges]. */
const TETRA: [number[][], number[][]] = [
  [[1, 1, 1], [-1, -1, 1], [-1, 1, -1], [1, -1, -1]],
  [[0, 1], [0, 2], [0, 3], [1, 2], [1, 3], [2, 3]],
];
const OCTA: [number[][], number[][]] = [
  [[1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0], [0, 0, 1], [0, 0, -1]],
  [[0, 2], [0, 3], [0, 4], [0, 5], [1, 2], [1, 3], [1, 4], [1, 5],
   [2, 4], [2, 5], [3, 4], [3, 5]],
];
const CUBE: [number[][], number[][]] = [
  [[-1, -1, -1], [1, -1, -1], [1, 1, -1], [-1, 1, -1],
   [-1, -1, 1], [1, -1, 1], [1, 1, 1], [-1, 1, 1]],
  [[0, 1], [1, 2], [2, 3], [3, 0], [4, 5], [5, 6], [6, 7], [7, 4],
   [0, 4], [1, 5], [2, 6], [3, 7]],
];

const ORBITERS = [
  { solid: TETRA, radius: 1.52, tilt: 0.42, speed: 0.00042, size: 0.085, phase: 0 },
  { solid: OCTA, radius: 1.78, tilt: -0.72, speed: -0.00029, size: 0.075, phase: 2.1 },
  { solid: CUBE, radius: 1.34, tilt: 1.02, speed: 0.00036, size: 0.062, phase: 4.3 },
];

export default function MorphField() {
  const ref = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    const canvas = ref.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    const still =
      typeof window.matchMedia === 'function' &&
      window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    let w = 0;
    let h = 0;
    const dpr = Math.min(window.devicePixelRatio || 1, 2); // cap: 3x costs 2.25x the pixels

    function resize() {
      if (!canvas) return;
      const r = canvas.getBoundingClientRect();
      w = r.width;
      h = r.height;
      canvas.width = Math.round(w * dpr);
      canvas.height = Math.round(h * dpr);
      ctx?.setTransform(dpr, 0, 0, dpr, 0, 0);
    }
    resize();
    const ro = new ResizeObserver(resize);
    ro.observe(canvas);

    /** Rotate, then divide by depth for perspective. */
    function project(
      x: number, y: number, z: number,
      ry: number, rx: number, scale: number,
    ): Pt {
      const cy = Math.cos(ry), sy = Math.sin(ry);
      let X = x * cy - z * sy;
      let Z = x * sy + z * cy;
      const cx = Math.cos(rx), sx = Math.sin(rx);
      let Y = y * cx - Z * sx;
      Z = y * sx + Z * cx;

      const camera = 4.2;
      const k = camera / (camera + Z);
      X *= k;
      Y *= k;
      // d is 0 (far) to 1 (near): used for line brightness, so the far side of
      // the mesh recedes instead of tangling with the near side.
      return { x: w / 2 + X * scale, y: h / 2 + Y * scale, d: (k - 0.66) / 0.72 };
    }

    function drawShape(s: Preset, ry: number, rx: number, scale: number) {
      if (!ctx) return;

      // Build the surface in object space first. Each preset has a different
      // natural radius — the star's is roughly twice the sphere's — so drawing
      // them all at a fixed scale makes the object visibly swell and shrink
      // through the loop. Measuring the widest point and dividing by it keeps
      // the silhouette the same size whatever shape it is currently in.
      const obj: { x: number; y: number; z: number }[][] = [];
      let maxR = 1e-6;
      for (let i = 0; i <= SEG_U; i++) {
        const u = -Math.PI + (i / SEG_U) * 2 * Math.PI;
        const r1 = superR(u, s.u);
        const row: { x: number; y: number; z: number }[] = [];
        for (let j = 0; j <= SEG_V; j++) {
          const v = -Math.PI / 2 + (j / SEG_V) * Math.PI;
          const r2 = superR(v, s.v);
          const x = r1 * Math.cos(u) * r2 * Math.cos(v);
          const y = r1 * Math.sin(u) * r2 * Math.cos(v);
          const z = r2 * Math.sin(v);
          const d = Math.hypot(x, y, z);
          if (d > maxR) maxR = d;
          row.push({ x, y, z });
        }
        obj.push(row);
      }

      const norm = 1 / maxR;
      const grid: Pt[][] = obj.map((row) =>
        row.map((q) => project(q.x * norm, q.y * norm, q.z * norm, ry, rx, scale)),
      );

      // Three depth buckets, each stroked once. Setting strokeStyle per segment
      // would be thousands of state changes a frame; this is three.
      const buckets: Path2D[] = [new Path2D(), new Path2D(), new Path2D()];
      const bucketOf = (a: Pt, b: Pt) => {
        const d = (a.d + b.d) / 2;
        return d < 0.34 ? 0 : d < 0.68 ? 1 : 2;
      };
      const seg = (a: Pt, b: Pt) => {
        const p = buckets[bucketOf(a, b)];
        if (!p) return;
        p.moveTo(a.x, a.y);
        p.lineTo(b.x, b.y);
      };

      for (let i = 0; i < SEG_U; i++) {
        const row = grid[i];
        const next = grid[i + 1];
        if (!row || !next) continue;
        for (let j = 0; j < SEG_V; j++) {
          const a = row[j], b = row[j + 1], c = next[j];
          if (a && b) seg(a, b);
          if (a && c) seg(a, c);
        }
      }

      ctx.lineWidth = 1;
      buckets.forEach((p, n) => {
        ctx.strokeStyle = DEPTH_STYLES[n] ?? DEPTH_STYLES[0];
        ctx.stroke(p);
      });
    }

    function drawOrbits(t: number, scale: number) {
      if (!ctx) return;
      for (const o of ORBITERS) {
        const ang = o.phase + t * o.speed;

        // the dotted orbit path
        ctx.strokeStyle = 'rgba(255,77,77,0.20)';
        ctx.setLineDash([1.5, 6]);
        ctx.lineWidth = 1;
        ctx.beginPath();
        for (let k = 0; k <= 72; k++) {
          const a = (k / 72) * Math.PI * 2;
          const p = project(
            Math.cos(a) * o.radius, 0, Math.sin(a) * o.radius,
            0, o.tilt, scale,
          );
          if (k === 0) ctx.moveTo(p.x, p.y); else ctx.lineTo(p.x, p.y);
        }
        ctx.stroke();
        ctx.setLineDash([]);

        // the solid riding it
        const centre = project(
          Math.cos(ang) * o.radius, 0, Math.sin(ang) * o.radius,
          0, o.tilt, scale,
        );
        const [verts, edges] = o.solid;
        const sz = o.size * scale * (0.72 + centre.d * 0.55);
        const spin = t * 0.0009;
        const pts = verts.map((v) => {
          const [vx = 0, vy = 0, vz = 0] = v;
          const cs = Math.cos(spin), sn = Math.sin(spin);
          const X = vx * cs - vz * sn;
          const Z = vx * sn + vz * cs;
          const cs2 = Math.cos(spin * 0.7), sn2 = Math.sin(spin * 0.7);
          return { x: centre.x + X * sz, y: centre.y + (vy * cs2 - Z * sn2) * sz };
        });
        ctx.strokeStyle = `rgba(255,120,120,${(0.22 + centre.d * 0.5).toFixed(3)})`;
        ctx.beginPath();
        for (const e of edges) {
          const a = pts[e[0] ?? 0];
          const b = pts[e[1] ?? 0];
          if (!a || !b) continue;
          ctx.moveTo(a.x, a.y);
          ctx.lineTo(b.x, b.y);
        }
        ctx.stroke();
      }
    }

    let raf = 0;
    const start = performance.now();

    function frame(now: number) {
      if (!ctx) return;
      const t = now - start;
      ctx.clearRect(0, 0, w, h);

      const scale = Math.min(w, h) * 0.33;
      const cycle = DWELL + BLEND;
      const idx = Math.floor(t / cycle) % SHAPES.length;
      const into = t % cycle;
      const from = SHAPES[idx] ?? SPHERE;
      const to = SHAPES[(idx + 1) % SHAPES.length] ?? SPHERE;
      const k = into < DWELL ? 0 : (into - DWELL) / BLEND;

      drawOrbits(t, scale);
      drawShape(lerpShape(from, to, k), t * 0.00018, 0.42 + Math.sin(t * 0.00013) * 0.22, scale);

      raf = requestAnimationFrame(frame);
    }

    if (still) {
      // One static frame: the shape is still worth seeing, the motion is not.
      const scale = Math.min(w, h) * 0.33;
      drawOrbits(0, scale);
      drawShape(SPHERE, 0.6, 0.4, scale);
    } else {
      raf = requestAnimationFrame(frame);
    }

    // A background animation has no business burning a laptop battery while the
    // tab is in the background.
    function onVisibility() {
      if (still) return;
      if (document.hidden) {
        cancelAnimationFrame(raf);
      } else {
        raf = requestAnimationFrame(frame);
      }
    }
    document.addEventListener('visibilitychange', onVisibility);

    return () => {
      cancelAnimationFrame(raf);
      ro.disconnect();
      document.removeEventListener('visibilitychange', onVisibility);
    };
  }, []);

  return <canvas ref={ref} className="morph" aria-hidden="true" />;
}
