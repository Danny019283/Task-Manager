import type { Task } from "./api";
import { formatTime, formatDateLabel, isOverdue } from "./dates";

export interface RowHandlers {
  /** Resolves true on success. On false/rejection the row's tick reverts. */
  onToggle: (task: Task) => Promise<boolean>;
  onDelete: (task: Task) => void;
}

const TICK_SVG = `<svg viewBox="0 0 16 16" width="12" height="12" fill="none" aria-hidden="true">
  <path class="tick-mark" d="M3 8.5 L6.5 12 L13 4" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
</svg>`;

const CROSS_SVG = `<svg viewBox="0 0 16 16" width="11" height="11" fill="none" aria-hidden="true">
  <path d="M3 3 L13 13 M13 3 L3 13" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" />
</svg>`;

/** A single ruled ledger line: tick box · description · date/time · delete mark. */
export function taskRow(task: Task, opts: RowHandlers & { showDate?: boolean }): HTMLLIElement {
  const li = document.createElement("li");
  li.className = "flex items-center gap-3 py-2.5";
  li.dataset.taskId = String(task.id);

  const overdue = isOverdue(task);

  const tick = document.createElement("button");
  tick.type = "button";
  tick.disabled = task.is_completed;
  tick.dataset.checked = String(task.is_completed);
  tick.setAttribute("aria-label", task.is_completed ? "Completada" : "Marcar como completada");
  tick.innerHTML = TICK_SVG;
  const uncheckedClass = [
    "grid h-5 w-5 shrink-0 place-items-center border transition-colors",
    overdue
      ? "border-accent text-transparent hover:bg-accent hover:text-paper"
      : "border-ink-soft text-transparent hover:border-ink hover:text-ink-soft",
  ].join(" ");
  tick.className = task.is_completed
    ? "grid h-5 w-5 shrink-0 place-items-center border transition-colors cursor-default border-ink-faint bg-ink text-paper"
    : uncheckedClass;
  if (task.is_completed) tick.querySelector("path")!.setAttribute("stroke-dashoffset", "0");
  if (!task.is_completed) {
    tick.addEventListener("click", async () => {
      tick.disabled = true;
      tick.dataset.checked = "true";
      tick.classList.add("text-paper", "bg-ink", "border-ink-faint");
      const ok = await opts.onToggle(task);
      if (!ok) {
        tick.disabled = false;
        tick.dataset.checked = "false";
        tick.className = uncheckedClass;
      }
    });
  }

  const desc = document.createElement("span");
  desc.className = [
    "flex-1 truncate text-[0.95rem]",
    task.is_completed ? "text-ink-soft line-through" : "text-ink",
  ].join(" ");
  desc.textContent = task.description;

  const when = document.createElement("span");
  when.className = [
    "shrink-0 font-mono text-xs tabular-nums",
    task.is_completed ? "text-ink-soft" : overdue ? "font-semibold text-accent" : "text-ink-soft",
  ].join(" ");
  when.textContent = opts.showDate
    ? `${formatDateLabel(task.date_limit)} ${formatTime(task.date_limit)}`
    : formatTime(task.date_limit);

  const del = document.createElement("button");
  del.type = "button";
  del.setAttribute("aria-label", "Eliminar tarea");
  del.innerHTML = CROSS_SVG;
  del.className = "shrink-0 text-ink-soft transition-colors hover:text-accent";
  del.addEventListener("click", () => opts.onDelete(task));

  li.append(tick, desc, when, del);
  return li;
}
