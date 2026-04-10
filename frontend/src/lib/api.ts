/**
 * API client for the SQL Practice Platform backend.
 */

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api";

async function fetchJson<T>(url: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${API_BASE}${url}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(err.detail || `API error: ${res.status}`);
  }
  return res.json();
}

// Questions
export const getQuestions = (params?: string) =>
  fetchJson<import("./types").QuestionListResponse>(`/questions${params ? `?${params}` : ""}`);

export const getQuestion = (id: number) =>
  fetchJson<import("./types").Question>(`/questions/${id}`);

export const getSolution = (id: number) =>
  fetchJson<import("./types").SolutionResponse>(`/questions/${id}/solution`);

export const getTags = () =>
  fetchJson<string[]>(`/questions/tags`);

// Execute & Validate
export const executeSQL = (sql: string) =>
  fetchJson<import("./types").ExecuteResponse>("/execute", {
    method: "POST",
    body: JSON.stringify({ sql }),
  });

export const validateSQL = (question_id: number, user_sql: string) =>
  fetchJson<import("./types").ValidateResponse>("/validate", {
    method: "POST",
    body: JSON.stringify({ question_id, user_sql }),
  });

// Datasets
export const getDatasets = () =>
  fetchJson<import("./types").TableInfo[]>("/datasets");

export const getDatasetDetail = (name: string) =>
  fetchJson<import("./types").TableDetail>(`/datasets/${name}`);

// Progress
export const getProgress = () =>
  fetchJson<import("./types").ProgressSummary>("/progress");

export const getRecentAttempts = () =>
  fetchJson<{ id: number; question_id: number; verdict: string; attempted_at: string }[]>(
    "/progress/recent"
  );

export const getQuestionProgress = (id: number) =>
  fetchJson<import("./types").QuestionProgress>(`/progress/${id}`);

export const toggleBookmark = (question_id: number, bookmarked: boolean) =>
  fetchJson<{ status: string }>("/progress/bookmark", {
    method: "POST",
    body: JSON.stringify({ question_id, bookmarked }),
  });

export const saveNotes = (question_id: number, notes: string) =>
  fetchJson<{ status: string }>("/progress/notes", {
    method: "POST",
    body: JSON.stringify({ question_id, notes }),
  });
