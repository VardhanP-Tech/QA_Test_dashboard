const API_URL = import.meta.env.VITE_API_URL ?? "http://localhost:8000";

export type Summary = { total_test_cases: number; total_executions: number; pass_rate: number; open_defects: number; by_status: Record<string, number> };
export type TestCase = { id: number; title: string; module: string; priority: string; created_at: string };
export type Execution = { id: number; test_case_id: number; cycle: string; status: "passed" | "failed" | "blocked" | "not_run"; executed_by: string; notes: string; executed_at: string };
export type Defect = { id: number; title: string; severity: string; status: string; test_case_id: number | null; description: string; created_at: string };

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const response = await fetch(`${API_URL}${path}`, { headers: { "Content-Type": "application/json" }, ...options });
  if (!response.ok) throw new Error("Request failed");
  return response.json();
}

export async function getSummary(): Promise<Summary> {
  return request("/api/dashboard/summary");
}

export async function getTestCases(): Promise<TestCase[]> {
  return request("/api/test-cases");
}

export const getExecutions = () => request<Execution[]>("/api/executions");
export const getDefects = () => request<Defect[]>("/api/defects");
export const createTestCase = (body: object) => request<TestCase>("/api/test-cases", { method: "POST", body: JSON.stringify(body) });
export const createExecution = (body: object) => request<Execution>("/api/executions", { method: "POST", body: JSON.stringify(body) });
export const createDefect = (body: object) => request<Defect>("/api/defects", { method: "POST", body: JSON.stringify(body) });
