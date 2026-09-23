# Offline HTML report format

Architecture reports are sensitive local artifacts. Generate one self-contained
HTML file that renders with networking disabled and performs no active content.
Follow the repository [security policy](../../../SECURITY.md).

## Hard requirements

- Inline CSS only.
- Inline static SVG only for diagrams.
- No JavaScript or event handlers.
- No external stylesheets, imports, fonts, images, analytics, links required for
  rendering, or other remote resources.
- Escape every repository-derived value before placing it in HTML or SVG text.
- Do not embed source code, secrets, logs, or sensitive details beyond what the
  architecture decision requires.

## Scaffold

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <meta name="referrer" content="no-referrer" />
    <meta http-equiv="Content-Security-Policy"
          content="default-src 'none'; style-src 'unsafe-inline'; img-src data:; font-src 'none'; script-src 'none'; connect-src 'none'; object-src 'none'; base-uri 'none'; form-action 'none'" />
    <title>Architecture review — {{escaped repository name}}</title>
    <style>
      :root {
        color-scheme: light;
        --paper: #fafaf9;
        --ink: #0f172a;
        --muted: #64748b;
        --line: #cbd5e1;
        --deep: #1e293b;
        --accent: #047857;
        --warn: #b45309;
        --leak: #dc2626;
      }
      * { box-sizing: border-box; }
      body { margin: 0; background: var(--paper); color: var(--ink);
             font-family: ui-sans-serif, system-ui, sans-serif; }
      main { max-width: 72rem; margin: 0 auto; padding: 3rem 1.5rem; }
      header, article, #top-recommendation { margin-bottom: 2.5rem; }
      article { border: 1px solid var(--line); border-radius: .75rem;
                background: white; padding: 1.5rem; }
      .diagrams { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr));
                  gap: 1rem; }
      .diagram { min-height: 20rem; border: 1px solid var(--line);
                 border-radius: .5rem; padding: 1rem; }
      .badge { display: inline-block; border-radius: 999px; padding: .2rem .6rem;
               color: white; background: var(--accent); font-size: .75rem; }
      .muted { color: var(--muted); }
      .seam { stroke-dasharray: 4 4; }
      .leak { stroke: var(--leak); }
      .deep { fill: var(--deep); color: white; }
      @media (max-width: 48rem) { .diagrams { grid-template-columns: 1fr; } }
    </style>
  </head>
  <body>
    <main>
      <header>...</header>
      <section id="candidates">...</section>
      <section id="top-recommendation">...</section>
    </main>
  </body>
</html>
```

The content security policy is defense in depth. The generator must still omit
all active and remote content rather than relying on the browser to block it.

## Header

Show the repository name, date, and a compact legend: solid box = module,
dashed line = seam, red arrow = leakage, thick dark box = deep module. Start
with the candidates rather than an introduction.

## Candidate card

Each candidate is one `<article>` with:

- **Title** — names the deepening.
- **Badge row** — recommendation strength (`Strong`, `Worth exploring`, or
  `Speculative`) and dependency category (`in-process`, `local-substitutable`,
  `ports & adapters`, or `mock`).
- **Files** — a minimal monospaced list.
- **Before / After diagram** — side-by-side inline static SVG or HTML/CSS.
- **Problem** and **Solution** — one sentence each.
- **Wins** — at most six short bullets.
- **ADR callout** — one line only when applicable.

## Static diagram patterns

- **Dependency or call flow:** inline `<svg>` with fixed boxes, paths, arrow
  markers, and escaped `<text>` labels.
- **Boxes and arrows:** HTML boxes with an overlaid inline SVG for arrows.
- **Cross-section:** stacked horizontal bands showing several shallow modules
  becoming one deep module.
- **Mass diagram:** compare interface area with implementation area.
- **Call-graph collapse:** show the prior calls as faded labels inside one deep
  module.

Every diagram needs a short text alternative in the surrounding HTML. Keep
diagrams near 320px tall and make them legible without animation or interaction.

## Style and language

Use generous whitespace and system fonts. Use one accent, red for leakage, and
amber for warnings. Keep repository-derived details minimal.

Use exactly the architecture vocabulary from `$codebase-design`: module,
interface, implementation, depth, deep, shallow, seam, adapter, leverage, and
locality. Do not substitute component, service, unit, API, signature, or
boundary when the glossary term applies.

## Top recommendation

End with one larger card: candidate name and one sentence explaining why it is
the strongest next step. Internal fragment links are allowed but not required.
