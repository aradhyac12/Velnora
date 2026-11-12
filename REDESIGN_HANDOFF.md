# VELNORA redesign: Phase 0 and Phase 1 handoff

## Status
- Phase 0 (audit, baseline): done.
- Phase 1 (design tokens, type system): done, build passes.
- Phase 2 (shared components): DONE except notification centre. Done: button, input, textarea, card, table, shadow scale, overlays (dialog, alert-dialog, sheet, menus, popover, hover-card), select, tabs, toasts, checkbox/radio/switch, breadcrumb primitive (mono, flat), header on layout tokens (`--header-h`, smaller seal, flat account chip), and a new phone bottom nav (`src/components/mobile-nav.tsx`, mounted in `_authenticated/route.tsx`, hidden on /submit and /auth and while a field is focused, role-filtered via `useVisibleLinks`).
- NOT done in Phase 2: notification centre (no notifications table or API exists; needs a data-model decision), sidebar shell (shadcn sidebar exists but no route uses it; desktop keeps the top header + account menu), article route still uses its own inline breadcrumb markup, search icon still hidden in the native app.
- Phase 3 (public site): STARTED, first pass only. Done: home and article header/abstract flattened (no gradients, glow or top bar; radii rounded-lg; abstract in Source Serif at --reading-w), shared `.surface` (card bg, radius-lg, no hover lift), search field focus ring. Not done: per-route audit notes, explore, about, fees, editorial-board, policies, verify, paper, auth, article body/sidebar content, promo banners, empty/error states, mobile layout review.
- Phases 4-12: NOT started.

## Baseline (before and after Phase 1)
- `vite build`: passes.
- `vitest`: 463 pass, 3 fail. Failures are unrelated to styling: native deep-link test, migration-journal test (58 vs 60 files), referral-domain test.
- `tsc --noEmit`: 5 errors, all pre-existing (`upload-progress.tsx`, `submit.tsx`).
- Not tested: runtime behaviour of any route, auth, payments, certificates, PDFs, mobile layouts. Visual output has not been viewed.

## Files changed (Phase 2 adds: button.tsx, input.tsx, textarea.tsx, card.tsx, table.tsx, site-header.tsx)
- `src/styles.css`: Porcelain and Obsidian tokens, layout tokens, font tokens.
- `src/routes/__root.tsx`: Google Fonts link adds Geist, Geist Mono, Source Serif 4.
- `src/components/ui/badge.tsx`, `src/lib/ui.tsx`: new "review" badge tone for under-review statuses.
- `src/lib/domain/site-meta.ts`, `public/site.webmanifest`: theme colour = Porcelain.

## Deliberate deviations from the spec (accessibility)
- Muted text uses #62655e, not #74766f (spec value is ~4.1:1 on Porcelain, below AA). #92938c kept as `--faint` for non-essential metadata.
- Warning text uses #7f5b1d (deeper step of #a77b36) so badge labels reach AA.

## Type system
- UI: Geist (fallback Public Sans). Headings: Lora (bundled). Reading and articles: Source Serif 4 (`--font-reading`). Metadata: Geist Mono (`--font-mono`).
- Fonts load from Google Fonts like the existing setup. Offline/Android falls back to system fonts, same as before.

## Layout tokens
`--header-h` 3.5rem, `--sidebar-w` 15rem, `--content-w` 72rem, `--reading-w` 68ch.

## Route inventory (38 files in src/routes)
Public: index, about, explore, fees, editorial-board, policies.index, policies.$slug, article.$velnoraId (+ .pdf), paper.$publicId, verify, verify_.$certId, verify_.certificate.$certId, auth, r.$code, robots.txt, sitemap.xml.
Authenticated (guarded by `_authenticated/route.tsx`): dashboard, submit, my-research.index, my-research.$id, manuscript.$paperId, reviews, certificates, profile, dues, founder, admin, orcid.callback, zenodo.callback.
API (no UI): api/public/health, client-error, mail/process, payments/razorpay-webhook, publish/process.
Per-route roles, data dependencies and responsive notes are NOT yet recorded.

## Not yet done
P0: Phase 2 shell and shared components; per-route audit. P1: public site, author workspace, submission flow, editorial, reviewer, article reader. P2: certificate and PDF layout, admin. P3: responsive pass, accessibility audit, performance, full regression run.
Known hard-coded colours remaining: maintenance.tsx, master-pause.tsx, upload-progress.tsx (amber/emerald). Android launcher icon background still navy.

## Phase 2 session checks
- v30: `vite build` passes; `tsc` = same 5 pre-existing errors; `vitest` 463 pass / 3 fail (same 3 as baseline). Visual output and real-device behaviour NOT viewed.
- Unverified risks: bottom nav on Android (viewport has no `viewport-fit=cover`, so safe-area inset is 0 there), pages with their own fixed bottom elements other than /submit, header height change 4rem to 3.5rem.
- Next: decide notification centre scope; then Phase 3 (public site), starting with a per-route audit.

## Phase 3 session check (v31)
- `vite build` passes; `tsc` same 5 pre-existing errors; `vitest` 463 pass / 3 fail (baseline). No browser available in the sandbox, so NOTHING was viewed. Changes are class and CSS edits chosen from reading the code.
- Next: open each public route in a browser, record roles/data/responsive notes, then restyle remaining public routes.

## App-wide flatten pass (v32)
- All `rounded-2xl`/`rounded-xl` in routes and components (outside ui/) became `rounded-lg` (20+29 hits, 11 files incl. admin, reviews, manuscript, referral, dues prompt, full-text).
- Hard-coded amber/emerald/sky removed: maintenance banner, master pause, upload progress now use caution/positive/primary tokens; upload progress gradients and glow removed. Zero amber/emerald classes remain in src outside ui/.
- Explore: native selects use card surface, 15px text and focus ring; checkbox uses accent-primary.
- Checks: build passes, tsc same 5 pre-existing errors, vitest 463/3 (baseline). NOT viewed in a browser.
- Still open: per-route audit notes, visual review of every route, certificate/PDF layout (Phase P2, immutable issued PDFs), Android launcher icon background still navy, notification centre, sidebar shell.
