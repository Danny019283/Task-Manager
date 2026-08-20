const API_BASE = import.meta.env.PUBLIC_API_BASE ?? "http://127.0.0.1:8000";

export interface Task {
  id: number;
  description: string;
  date_limit: string;
  is_completed: boolean;
}

export class ApiError extends Error {}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  let res: Response;
  try {
    res = await fetch(`${API_BASE}${path}`, {
      headers: { "Content-Type": "application/json" },
      ...init,
    });
  } catch {
    throw new ApiError(
      "No se pudo conectar con el backend. ¿Está corriendo en " + API_BASE + "?",
    );
  }

  if (!res.ok) {
    let detail = `Error ${res.status}`;
    try {
      const body = await res.json();
      detail = Array.isArray(body.detail)
        ? body.detail.map((d: { msg: string }) => d.msg).join(", ")
        : (body.detail ?? detail);
    } catch {
      // response had no JSON body
    }
    throw new ApiError(detail);
  }

  if (res.status === 204) return undefined as T;
  return res.json();
}

export const api = {
  list: () => request<Task[]>("/tasks/"),
  create: (data: { description: string; date_limit: string; is_completed?: boolean }) =>
    request<Task>("/tasks/register", {
      method: "POST",
      body: JSON.stringify({ is_completed: false, ...data }),
    }),
  complete: (id: number) =>
    request<Task>(`/tasks/${id}/complete`, { method: "PUT" }),
  remove: (id: number) => request<void>(`/tasks/${id}`, { method: "DELETE" }),
};
