---
name: Agenda
description: A personal task manager styled as a day-planner page — due dates read like a ledger, not a to-do list.
colors:
  cream-page: "#f5f1e6"
  desk-backdrop: "#efe8d6"
  rule-hairline: "#d8cfb8"
  ink: "#1f1c18"
  ink-soft: "#6b6255"
  ink-faint: "#96876c"
  date-red: "#b5352a"
  date-red-wash: "rgba(181, 53, 42, 0.12)"
typography:
  display:
    fontFamily: "ui-monospace, 'SF Mono', 'Cascadia Code', 'Roboto Mono', Menlo, Consolas, monospace"
    fontSize: "3.75rem"
    fontWeight: 600
    lineHeight: 1
    letterSpacing: "normal"
  headline:
    fontFamily: "'Segoe UI', ui-sans-serif, system-ui, -apple-system, Roboto, Helvetica, Arial, sans-serif"
    fontSize: "1.875rem"
    fontWeight: 600
    lineHeight: 1.25
  title:
    fontFamily: "'Segoe UI', ui-sans-serif, system-ui, -apple-system, Roboto, Helvetica, Arial, sans-serif"
    fontSize: "0.95rem"
    fontWeight: 400
    lineHeight: 1.4
  body:
    fontFamily: "'Segoe UI', ui-sans-serif, system-ui, -apple-system, Roboto, Helvetica, Arial, sans-serif"
    fontSize: "0.875rem"
    fontWeight: 400
    lineHeight: 1.5
  label:
    fontFamily: "ui-monospace, 'SF Mono', 'Cascadia Code', 'Roboto Mono', Menlo, Consolas, monospace"
    fontSize: "0.75rem"
    fontWeight: 400
    letterSpacing: "0.14em"
rounded:
  none: "0px"
  sm: "2px"
spacing:
  xs: "4px"
  sm: "8px"
  md: "12px"
  lg: "16px"
  xl: "24px"
  2xl: "32px"
components:
  button-primary:
    backgroundColor: "transparent"
    textColor: "{colors.ink}"
    rounded: "{rounded.sm}"
    padding: "8px 16px"
  button-primary-hover:
    backgroundColor: "{colors.ink}"
    textColor: "{colors.cream-page}"
  tab-active:
    backgroundColor: "{colors.cream-page}"
    textColor: "{colors.ink}"
    rounded: "{rounded.sm}"
  tab-inactive:
    backgroundColor: "{colors.desk-backdrop}"
    textColor: "{colors.ink-soft}"
    rounded: "{rounded.sm}"
---

# Design System: Agenda

## Overview

**Creative North Star: "The Day Planner Grid"**

Agenda treats a due date as a page in a day planner, not a field in a form. Opening the app opens today's page: the huge tabular date numeral anchors the view, overdue items are stamped out in the one reserved red, and everything else reads as ruled ledger lines — a tick box, a description, a time, a way to strike it out. The system is deliberately flat and typographic: no cards, no shadows, no icon-as-decoration. Two direction rounds were considered and rejected in favor of this one — "Courier Tracking Slip" (tasks as parcels in transit) and "Manual Tab Rail" (a boxed-software reference manual) — both are documented in the direction contract at the top of `frontend/src/layouts/Layout.astro` for provenance.

One deliberate revision happened after first ship: the page originally carried a continuous ruled-paper background texture (horizontal hairlines behind all content). The user rejected it explicitly — the lines fought visually with the ledger rows' own dividers and read as inconsistent — and asked instead for the page to read as a bordered sheet against a desk-toned backdrop. That is the current, intentional state; do not reintroduce a decorative background rule pattern.

**Key Characteristics:**
- Flat cream "page" bordered like a sheet, floating on a slightly darker desk-toned backdrop (border only appears at ≥640px; full-bleed edge-to-edge below that, matching the mobile-primary usage scene)
- Every date and time numeral in tabular monospace; every other word in a workhorse system sans
- Exactly one accent color (date-red), spent only on overdue/urgent/error meaning
- State changes are marks (a drawn checkmark, a strikethrough), never a second hue
- No shadows, no gradients, no glass — the world is paper, not glass or metal

## Colors

A restrained palette: neutrals carry the page, one accent carries urgency. Roughly 90%+ of any screen is neutral; date-red never exceeds a small minority of the surface and disappears entirely on a screen with nothing overdue.

### Primary
- **Date Red** (#b5352a): The single accent. Used only for the "Vencidas" (overdue) heading, an overdue row's tick outline and time, the drawn-in checkmark's hover state on an overdue row, and error banners/text. Never used decoratively.

### Neutral
- **Cream Page** (#f5f1e6): The page surface itself — body background inside the bordered sheet.
- **Desk Backdrop** (#efe8d6): The backdrop behind the page on ≥640px screens; also the inactive-tab fill and scrollbar track.
- **Rule Hairline** (#d8cfb8): Row dividers between ledger items, the page's own border edge, dashed input underlines.
- **Ink** (#1f1c18): Primary text, the completed-tick fill, focus/caret color is date-red but body text is always ink.
- **Ink Soft** (#6b6255): Secondary text — meta labels, times, completed/struck descriptions, placeholder text. Passes 4.5:1 against Cream Page; this is the floor for anything that must read as body text.
- **Ink Faint** (#96876c): Decorative-only tone — dashed borders, the unchecked tick's invisible glyph fill. Passes ~3:1 (non-text UI floor) but not 4.5:1, so it is never used for readable text.

### Named Rules
**The One Accent Rule.** Date-red appears nowhere except to mark overdue, urgent, or error state. If you're reaching for it to decorate a button, a tab, or a heading that isn't about urgency, stop — that's the rule breaking.

## Typography

**Display Font:** ui-monospace stack (with system mono fallbacks)
**Body Font:** system UI sans stack ("Segoe UI", ui-sans-serif, system-ui, -apple-system, Roboto, Helvetica, Arial)
**Label/Mono Font:** same ui-monospace stack as Display

**Character:** A workhorse pairing, deliberately — the brief is Operate-mode (a personal tool, not a marketing surface), so the type voice is a system sans doing prose and a tabular mono doing every number. No display serif, no "AI-default" faces; the planner-ledger feel comes from the mono/sans split, not from a characterful display face.

### Hierarchy
- **Display** (600, 3.75rem / text-6xl, leading-none, tabular-nums): the day-of-month numeral on the Hoy view. The single largest element in the system.
- **Headline** (600, 1.875rem / text-3xl): page titles ("Todas las tareas").
- **Title** (400, 0.95rem): a task's own description text — the thing being read at a glance.
- **Body** (400, 0.875rem / text-sm): supporting prose — empty states, loading text, error messages.
- **Label** (400, 0.75rem / text-xs, 0.14em tracking, uppercase, mono): tab names, section headers ("VENCIDAS", "PRÓXIMAS"), the weekday line, button text ("AÑADIR"), date/time meta next to a row.

### Named Rules
**The Tabular Rule.** Every date and every time numeral renders in the monospace stack with tabular figures (`tabular-nums`) — never the body sans. This is what makes the list read as a ledger instead of a sentence.

## Layout

Single-column, mobile-first. Content lives inside one `max-w-2xl` (42rem) container. At ≥640px (`sm:`) that container becomes a bordered "sheet" (`border` in Rule Hairline, `bg-cream-page`) with vertical margin, floating on the Desk Backdrop body color. Below 640px the sheet has no border and no margin — it *is* the viewport, full-bleed, matching the confirmed primary device (mobile, "no descarto abrirlo en el PC" as secondary).

Two screens share one shell (`Layout.astro` + `TabRail.astro`): a "Hoy" (Home) view and a "Todas" (All Tasks) view, switched by a two-tab strip at the top styled as planner index tabs (the active tab overlaps the content edge via a negative margin and loses its bottom border, so it reads as physically attached to the current page; the inactive tab sits recessed one shade darker).

Row rhythm: ledger rows use Tailwind's default spacing scale (`py-2.5` per row, `gap-3` between a row's tick/description/time/delete). Section spacing is generous relative to row spacing — more space above a section label than below it (`mb-8` between sections, `mb-1` between a section's label and its first row).

## Elevation & Depth

Flat by design — no shadows, no blur, anywhere in the system. This was explicitly reaffirmed after the user reviewed the first ruled-paper-background version and asked for less flatness; the fix was a **border**, not a shadow: the bordered sheet against the desk-toned backdrop is the system's only depth cue.

### Named Rules
**The Flat-By-Default Rule.** No `box-shadow` exists anywhere in this codebase. Depth comes from a 1px border and a background-color step between the page and its backdrop, never from blur or offset shadow. A future component that reaches for a shadow to "lift" itself is breaking the system, not extending it.

## Shapes

Corners are almost square. The only rounded elements are the primary button and the error banner, both at `rounded-sm` (2px) — enough to soften an interactive edge, not enough to read as "app chrome." Task rows, tick boxes, and the tab strip are all hard corners. The tick box and the tab pills are the only bordered shapes besides the page sheet itself; everything else is typographic (rules and text), not boxed.

## Components

### Tabs (`TabRail.astro`)
- **Shape:** `rounded-t-md` on each tab, square everywhere else; the active tab's bottom edge disappears into the page via `-mb-px` and `z-10`.
- **Active:** Cream Page background, Ink text — visually the same surface as the content below it.
- **Inactive:** Desk Backdrop background, Ink Soft text, hover brightens to Ink.
- **Divider:** a Rule Hairline border runs the full width beneath both tabs.

### Buttons
- **Shape:** `rounded-sm` (2px), 1px Ink border.
- **Primary ("Añadir"):** transparent fill, Ink text and border by default; inverts to Ink fill / Cream Page text on hover — a stamp-like invert, not a color swap.
- **Focus:** a 2px Date Red outline with 2px offset (`:focus-visible`), consistent with the accent's "attention" role.

### Task Row (signature component)
- **Tick box:** 20×20px square, 1px border, holds a hand-authored inline SVG checkmark (never a Unicode glyph). Unchecked: border in Ink Soft (or Date Red when the task is overdue), glyph invisible until hover/focus. Checked: Ink fill, Cream Page glyph, permanently disabled (there is no "undo complete" — the backend has no such endpoint). Completing a task plays a single authored signature interaction: the checkmark draws itself in via `stroke-dashoffset` (320ms, `cubic-bezier(0.16,1,0.3,1)`) rather than popping or fading in.
- **Description:** Title-scale text; Ink normally, Ink Soft + strikethrough once completed.
- **Time / date meta:** Label-scale, tabular mono; Ink Soft normally, bold Date Red when overdue.
- **Delete control:** a drawn × (SVG, not a glyph), Ink Faint at rest, Date Red on hover/focus. Deliberately **always visible**, never hover-gated — the primary device is mobile, which has no hover state, so a hover-only delete affordance would be undiscoverable there.

### Inputs (add-task form)
- **Style:** no box, no border-all — a single dashed bottom border in Ink Faint, background transparent. Reads as a blank ruled line waiting to be written on.
- **Focus:** border solidifies to Ink; caret color is Date Red.
- **Layout:** description input flexes to fill available width; the datetime input holds a fixed width on `sm:` and up, full width below it.

### Feedback states
- **Error banner:** Date Red text on a Date Red Wash background, `rounded-sm`, 1px Date-Red-at-40%-opacity border. Used for both form-level and list-level API failures; copy names the actual problem (e.g. "No se pudo conectar con el backend…") rather than a generic failure string.
- **Empty state:** centered Body-scale text in Ink Soft ("Página en blanco — nada pendiente por ahora."), no illustration.
- **Loading state:** centered Label-scale mono text ("Cargando…"), no spinner.

## Do's and Don'ts

### Do:
- **Do** reserve Date Red exclusively for overdue/urgent/error meaning — grep the codebase before adding a new use.
- **Do** render every date and time value in the tabular monospace stack, never the body sans.
- **Do** author icons as hand-drawn inline SVG at a consistent stroke weight; never a Unicode glyph (✓, ×, etc.) standing in for an icon.
- **Do** keep functional controls (delete, in particular) visible by default rather than hover-gated — the primary device has no hover.
- **Do** show state changes as a written mark (a filled tick, a strikethrough) rather than a new color.

### Don't:
- **Don't** add a decorative background ruled-line texture behind page content. This was tried and explicitly rejected by the user for reading as inconsistent with the row dividers; only per-row hairline dividers (`divide-paper-line`) are part of the system now.
- **Don't** add `box-shadow`, glass, or blur anywhere. Depth is a border + background-color step, never a shadow.
- **Don't** introduce a second accent color. If a new state needs distinguishing, express it as a mark (icon, strikethrough, weight) before reaching for color.
- **Don't** use a kicker/eyebrow label above a heading — delete the label and let the heading (or, on Hoy, the date numeral itself) carry the weight.
- **Don't** round corners past `rounded-sm` (2px) — the system's silhouette is almost entirely square.
