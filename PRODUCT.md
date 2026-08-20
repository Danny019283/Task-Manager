# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Stack

Astro + Tailwind CSS (confirmed by the user for the upcoming `frontend/` build). The existing backend is Python/FastAPI, consumed as a plain JSON API — see `CLAUDE.md` for the full contract (base URL, endpoints, DTOs, error shape).

## Users

A single primary user: the product's own developer, using it as their personal day-to-day task manager. No multi-user accounts, roles, or auth exist or are planned.

## Product Purpose

A simple, low-friction way to register, track, and complete personal tasks, with a due date (`date_limit`) and a WhatsApp reminder on creation/completion (via CallMeBot). Success is: adding a task takes seconds, the list of open tasks is always clear, and completing a task is one action.

## Positioning

Not a competitive/differentiated product — the user explicitly framed it as "a simple, direct tool," not a project aiming to out-position other task managers. Its one genuinely distinct mechanism is the WhatsApp notification on task events, which most minimal task-manager builds skip.

## Operating Context

- Backend: working FastAPI service backed by a live Supabase Postgres database (see `CLAUDE.md` for schema/migration workflow via the Supabase MCP server).
- Frontend: not started; will be a client of the FastAPI JSON API described in `CLAUDE.md` (base URL `http://127.0.0.1:8000`, CORS open to any origin, dates as naive ISO 8601 strings).
- Notifications: outbound-only WhatsApp messages via the free CallMeBot API; a failed send is logged, never surfaced as an error to the user.

## Capabilities and Constraints

- Task fields: `description` (string), `date_limit` (datetime, must not be in the past), `is_completed` (boolean).
- No authentication/authorization layer exists; this is intentional for a single personal user, not an oversight to fix.
- Full CRUD + a dedicated "complete" action are already implemented backend-side (`POST /tasks/register`, `GET /tasks/`, `GET /tasks/{id}`, `PUT /tasks/{id}`, `PUT /tasks/{id}/complete`, `DELETE /tasks/{id}`).
- No linter/formatter configured for the backend; a small pytest suite covers only the `Task` entity so far.

## Brand Commitments

None — no existing name, logo, or visual identity constraints beyond the plain "task manager" framing. Open for the frontend's visual world to be established in a later `new-work` pass.

## Evidence on Hand

None — no real content, sample data, testimonials, or design assets exist yet. `frontend/` is empty; future work must not fabricate sample tasks as if they were real user data (mock/demo data should be clearly synthetic).

## Product Principles

- Keep the core loop trivial: add a task, see it, complete it — friction is the enemy on a personal-use tool.
- The API is the source of truth for what the frontend can do; consult `CLAUDE.md` / `/docs` rather than assuming endpoints.
- No auth, no multi-user complexity — don't design flows that imply accounts, sharing, or permissions.
- WhatsApp notification is a nice-to-have side effect, never a blocking dependency of the core task flow.
