# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project state

Task manager application. The backend is a working Python/FastAPI service backed by a live Supabase Postgres database, with WhatsApp notifications via CallMeBot. `frontend/` is still empty, not started. The backend has a dependency manifest (`backend/src/pyproject.toml` + `uv.lock`, managed with `uv`) and a small pytest suite; there is no linter/formatter configured.

## Structure

- `backend/src/` — Python backend, organized in layers. The import root is the `src` package (not `backend`) — internal code uses relative imports like `from ..data_access.task_repository import TaskRepository`.
  - `model/entities/` — domain entities. `task.py`'s `Task` uses name-mangled private attributes (`id`, `description`, `limit_date`, `is_completed`) with property getters; `id` is optional (`None` until persisted); the constructor validates `limit_date` isn't in the past; `mark_completed()` is the only mutator besides construction.
  - `model/services/` — cross-cutting service interfaces + implementations: `Inotifier.py` (abstract `send_notification(self, task: Task) -> None`) and `ws_notifier.py` (`WsNotifier`, sends a WhatsApp message via the free CallMeBot HTTP API using `CALLMEBOT_PHONE`/`CALLMEBOT_APIKEY` from `model/services/.env`; a failed HTTP call is logged as a warning, not raised, so a notification failure never breaks a use case).
  - `data_access/` — persistence layer: `task_model.py` (`TaskModel`, the SQLModel/ORM row for the `tasks` table), `Itask_repository.py` (`ITaskRepository` interface — the source of truth for the method names/signatures `application/` calls), `task_repository.py` (`TaskRepository`, the Supabase/Postgres implementation, converts between `TaskModel` rows and `Task` entities), `database/datebase_connection.py` (SQLAlchemy engine + session factory, reads `DATABASE_URL` from `database/.env`; note the filename typo, `datebase_connection.py`, is intentional/existing — don't silently rename it).
  - `application/` — use cases: `task_application.py` (`TaskApplication`, orchestrates the repository and notifier, raises typed exceptions), `task_mapper.py` (`TaskMapper`, converts between router DTOs and the `Task` entity), `exeptions.py` (note the typo — existing filename, don't rename without asking; defines the `TaskApplicationError` hierarchy: `InvalidTaskDataError`, `TaskNotFoundError`, `NoTasksFoundError`, `TaskPersistenceError`).
  - `routers/` — FastAPI layer: `task_dtos.py` (pydantic request/response DTOs) and `task_router.py` (the `/tasks` endpoints, wired to `TaskApplication` via `Depends`, mapping application exceptions to HTTP status codes).
  - `main.py` — FastAPI app entrypoint, mounts the task router.
  - `tests/` — pytest suite (currently covers `model/entities/task.py` only).
- `frontend/` — empty, not started.

## Database

The backend talks to a real Supabase Postgres project — there is no local/mocked database. Schema changes should go through the Supabase MCP server (`apply_migration` / `list_migrations` / `list_tables`, etc.), which is registered in `backend/.mcp.json`; don't hand-run ad hoc DDL outside of a tracked migration unless asked to. The `tasks` table lives in the `public` schema with RLS enabled and no policies — that's intentional, the backend connects with a direct Postgres role rather than through PostgREST/the anon key, so RLS policies aren't load-bearing here yet.

## Secrets

`backend/src/data_access/database/.env` (`DATABASE_URL=...`) and `backend/src/model/services/.env` (`CALLMEBOT_PHONE=...`, `CALLMEBOT_APIKEY=...`) hold real credentials and are gitignored via `backend/src/.gitignore`. Never commit them, and never print their contents — if you need to check their shape, inspect structure only (e.g. `grep -oE '^[A-Z_]+=' <file>`), not values.

## Consuming the API (for frontend work)

Start the backend first (see Commands below); once it's running you generally shouldn't need to open any backend source to build against it:

- **Interactive docs (source of truth)**: `http://127.0.0.1:8000/docs` (Swagger UI) and `http://127.0.0.1:8000/openapi.json` (raw schema, e.g. to generate a typed client). If this doc and `/docs` ever disagree, trust `/docs`.
- **Base URL**: `http://127.0.0.1:8000` (default `uvicorn` port; add `--port` to change it). All task endpoints are under `/tasks`.
- **CORS**: open to any origin (`main.py` adds `CORSMiddleware` with `allow_origins=["*"]`), so a browser frontend on any dev port can call it directly.
- **Dates**: `date_limit` is a full ISO 8601 datetime string, e.g. `"2026-08-21T00:24:56.024796"` (no timezone suffix — treat it as local/naive, don't append `Z`). `date_limit` must not be in the past or the API rejects the request.
- **Errors**: every non-2xx response is JSON `{"detail": "<message>"}`, except FastAPI's own request-validation failures (e.g. missing/malformed field), which return `422` with `{"detail": [{...pydantic error...}]}`.

### Endpoints

| Method | Path | Body | Success | Notes |
|---|---|---|---|---|
| POST | `/tasks/register` | `CreateTaskDTO` | `201` → `TaskResponseDTO` | Creates a task; also fires a best-effort WhatsApp notification (never blocks/fails the response). |
| GET | `/tasks/` | — | `200` → `TaskResponseDTO[]` | `[]` when there are no tasks. |
| GET | `/tasks/{task_id}` | — | `200` → `TaskResponseDTO` | `404` if `task_id` doesn't exist. |
| PUT | `/tasks/{task_id}` | `UpdateTaskDTO` | `200` → `TaskResponseDTO` | Partial update — omit fields you don't want to change. Any `id` in the body is ignored/overwritten by the path's `task_id`. `404` if it doesn't exist. |
| PUT | `/tasks/{task_id}/complete` | — | `200` → `TaskResponseDTO` | Marks the task completed; fires a notification. `404` if it doesn't exist. |
| DELETE | `/tasks/{task_id}` | — | `204`, empty body | `404` if it doesn't exist. |

### DTOs

```
CreateTaskDTO   { description: string, date_limit: datetime, is_completed: boolean }
UpdateTaskDTO   { description?: string, date_limit?: datetime, is_completed?: boolean }  // id comes from the URL, not the body
TaskResponseDTO { id: int, description: string, date_limit: datetime, is_completed: boolean }
```

`POST /tasks/register` requires all three `CreateTaskDTO` fields (`is_completed` is normally `false` for a new task, but the API accepts any value). Every other endpoint returns/consumes `TaskResponseDTO`-shaped data as described above.

## Commands

Everything runs through the `uv`-managed venv at `backend/src/.venv` (Python 3.14).

- Install/sync dependencies: `cd backend/src && uv sync`
- Run the API: `cd backend && src/.venv/bin/uvicorn src.main:app --reload` — must run with `backend/` as the working directory (not `backend/src/`), since the app's relative imports are rooted at `src`.
- Run tests: `cd /home/danny/Proyectos/task_manager && backend/src/.venv/bin/python -m pytest backend/src/tests` — must run with the repo root (one level above `backend/`) as the working directory, since `tests/test_task.py` imports as `backend.src...`.

There is no lint or build tooling configured.

## Conventions

- Layering is entities → services/data_access → application → routers; follow it for new backend code, using relative imports rooted at `src`.
- Domain entities keep name-mangled private attributes with property getters and explicit mutator methods (e.g. `Task.mark_completed()`) instead of public setters. Persistence rows (`TaskModel`) are separate SQLModel classes, never the domain entities themselves — conversion happens in `task_repository.py`.
- `Itask_repository.py` and `Inotifier.py` are contracts: if you change a method name/signature on one side (e.g. in `TaskApplication` or a router), update the interface and its implementation(s) to match, in the same change.
