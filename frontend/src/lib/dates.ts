const WEEKDAYS = [
  "domingo",
  "lunes",
  "martes",
  "miércoles",
  "jueves",
  "viernes",
  "sábado",
];

const MONTHS = [
  "enero",
  "febrero",
  "marzo",
  "abril",
  "mayo",
  "junio",
  "julio",
  "agosto",
  "septiembre",
  "octubre",
  "noviembre",
  "diciembre",
];

export function todayHeading(now: Date) {
  return {
    weekday: WEEKDAYS[now.getDay()],
    day: String(now.getDate()).padStart(2, "0"),
    month: MONTHS[now.getMonth()],
    year: now.getFullYear(),
  };
}

export function isSameDay(a: Date, b: Date) {
  return (
    a.getFullYear() === b.getFullYear() &&
    a.getMonth() === b.getMonth() &&
    a.getDate() === b.getDate()
  );
}

export function isOverdue(task: { date_limit: string; is_completed: boolean }, now = new Date()) {
  return !task.is_completed && new Date(task.date_limit) < now;
}

export function formatTime(iso: string) {
  const d = new Date(iso);
  return `${String(d.getHours()).padStart(2, "0")}:${String(d.getMinutes()).padStart(2, "0")}`;
}

export function formatDateLabel(iso: string, now = new Date()) {
  const d = new Date(iso);
  if (isSameDay(d, now)) return "hoy";
  const tomorrow = new Date(now);
  tomorrow.setDate(now.getDate() + 1);
  if (isSameDay(d, tomorrow)) return "mañana";
  return `${WEEKDAYS[d.getDay()].slice(0, 3)} ${String(d.getDate()).padStart(2, "0")} ${MONTHS[d.getMonth()].slice(0, 3)}`;
}

/** Value suitable for an <input type="datetime-local"> defaulting to +1h from now. */
export function defaultDueValue(now = new Date()) {
  const d = new Date(now.getTime() + 60 * 60 * 1000);
  d.setSeconds(0, 0);
  const pad = (n: number) => String(n).padStart(2, "0");
  return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}T${pad(d.getHours())}:${pad(d.getMinutes())}`;
}
