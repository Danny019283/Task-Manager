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
