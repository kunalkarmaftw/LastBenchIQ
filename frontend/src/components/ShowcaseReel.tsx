import { useEffect, useState } from 'react';

/**
 * A four-beat loop of what the product actually does, shown beside the sign-in
 * form: read the papers, rank by marks, cut the list, hand back an order.
 *
 * Every number in here is real — it comes from the Computer Networks analysis
 * in `ml/data/demo_bundle.json` (7 papers, 145 questions, 39 topics, 12 of them
 * carrying 58.9% of the marks). Inventing a prettier number would make the
 * first thing a student sees the first thing the product lies about.
 *
 * Decorative for assistive tech: the reel is aria-hidden and the same three
 * claims sit in a visually hidden list, because a panel that rewrites itself
 * every four seconds is hostile to a screen reader.
 */

const PAPERS = 7;
const QUESTIONS = 145;
const TOPICS = 39;
const BAND_A = 12;
const BAND_A_SHARE = 59; // per cent of total marks

/** The five heaviest CN topics, with each one's real share of the marks. */
const TOP_TOPICS = [
  { name: 'Transport layer protocols', share: 8.0 },
  { name: 'Error detection & correction', share: 7.3 },
  { name: 'Multiplexing (WDM, TDM, FDM)', share: 6.7 },
  { name: 'Static & dynamic routing', share: 5.0 },
  { name: 'Connection management', share: 4.9 },
];
// Derived, not hardcoded to TOP_TOPICS[0]: the bars stay correct if the list
// is ever reordered or replaced with live data.
const WIDEST = Math.max(...TOP_TOPICS.map((t) => t.share));

const PLAN = [
  { day: 'Day 1–2', task: 'Transport layer protocols' },
  { day: 'Day 3', task: 'Error detection & correction' },
  { day: 'Day 4', task: 'Multiplexing' },
  { day: 'Day 5', task: 'Routing' },
];

const SCENES = ['Reads', 'Ranks', 'Cuts', 'Plans'] as const;
const DWELL_MS = 4200;

function prefersReducedMotion(): boolean {
  if (typeof window === 'undefined' || !window.matchMedia) return false;
  return window.matchMedia('(prefers-reduced-motion: reduce)').matches;
}

export default function ShowcaseReel() {
  const [still] = useState(prefersReducedMotion);
  const [i, setI] = useState(0);

  useEffect(() => {
    // Someone who asked for less motion gets the first scene, held still.
    if (still) return;
    const t = setInterval(() => setI((n) => (n + 1) % SCENES.length), DWELL_MS);
    return () => clearInterval(t);
  }, [still]);

  return (
    <div className="reel-wrap">
      {/* `key` restarts the scene's entry animation on every change. */}
      <div className="reel" aria-hidden="true">
        <div className="reel-stage" key={i}>
          {i === 0 && <SceneRead />}
          {i === 1 && <SceneRank />}
          {i === 2 && <SceneCut />}
          {i === 3 && <ScenePlan />}
        </div>

        <div className="reel-dots">
          {SCENES.map((label, n) => (
            <span key={label} className="reel-dot" data-on={n === i} />
          ))}
        </div>
      </div>

      <ul className="sr-only">
        <li>Ranks every topic by the marks it carries, using your own past papers.</li>
        <li>Flags topics that are no longer on the current syllabus.</li>
        <li>Says so plainly when there are too few papers to rank anything.</li>
      </ul>
    </div>
  );
}

/* -- 1. reads ------------------------------------------------------------- */
function SceneRead() {
  return (
    <>
      <p className="reel-kicker">Reads your own papers</p>
      <div className="paper-stack">
        {Array.from({ length: PAPERS }, (_, n) => (
          <span key={n} className="paper" style={{ animationDelay: `${n * 95}ms` }} />
        ))}
      </div>
      <p className="reel-line">
        <b>{QUESTIONS} questions</b> pulled from {PAPERS} Computer Networks papers
      </p>
    </>
  );
}

/* -- 2. ranks ------------------------------------------------------------- */
function SceneRank() {
  return (
    <>
      <p className="reel-kicker">Ranks them by marks</p>
      <div className="bars">
        {TOP_TOPICS.map((t, n) => (
          <div className="bar-row" key={t.name} style={{ animationDelay: `${n * 110}ms` }}>
            <span className="bar-name">{t.name}</span>
            <span className="bar-track">
              <span
                className="bar-fill"
                style={{
                  width: `${(t.share / WIDEST) * 100}%`,
                  animationDelay: `${n * 110 + 120}ms`,
                }}
              />
            </span>
            <span className="bar-pct">{t.share.toFixed(1)}%</span>
          </div>
        ))}
      </div>
      <p className="reel-line">Share of total marks across every paper</p>
    </>
  );
}

/* -- 3. cuts -------------------------------------------------------------- */
function SceneCut() {
  return (
    <>
      <p className="reel-kicker">Cuts the list</p>
      <div className="cut">
        <span className="cut-from">{TOPICS}</span>
        <span className="cut-arrow" aria-hidden="true">
          →
        </span>
        <span className="cut-to">{BAND_A}</span>
      </div>
      <p className="reel-line">
        <b>{BAND_A} topics</b> carry <b>{BAND_A_SHARE}%</b> of the marks. The other{' '}
        {TOPICS - BAND_A} can wait.
      </p>
    </>
  );
}

/* -- 4. plans ------------------------------------------------------------- */
function ScenePlan() {
  return (
    <>
      <p className="reel-kicker">Hands back an order</p>
      <ol className="plan">
        {PLAN.map((p, n) => (
          <li key={p.day} style={{ animationDelay: `${n * 130}ms` }}>
            <span className="plan-day">{p.day}</span>
            <span className="plan-task">{p.task}</span>
          </li>
        ))}
      </ol>
      <p className="reel-line">Heaviest topics first, so the first hour is the one that pays</p>
    </>
  );
}
