import {
  QueryResponse,
  DashboardStats,
  SchemaResponse,
  QueryHistoryResponse
} from "../types";

// Base API URL falls back to Next.js proxy route /api
const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8008/api";

export async function executeQuery(question: string, sessionId: string = "default_session"): Promise<QueryResponse> {
  const res = await fetch(`${API_BASE}/query`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question, session_id: sessionId }),
  });

  if (!res.ok) {
    const errorData = await res.json().catch(() => ({}));
    throw new Error(errorData.detail || `Server error (${res.status})`);
  }

  return res.json();
}

export async function fetchDashboard(): Promise<DashboardStats> {
  const res = await fetch(`${API_BASE}/dashboard`, {
    method: "GET",
    headers: { "Content-Type": "application/json" },
    cache: "no-store",
  });

  if (!res.ok) {
    throw new Error(`Failed to fetch dashboard metrics (${res.status})`);
  }

  return res.json();
}

export async function fetchSchema(): Promise<SchemaResponse> {
  const res = await fetch(`${API_BASE}/schema`, {
    method: "GET",
    headers: { "Content-Type": "application/json" },
  });

  if (!res.ok) {
    throw new Error(`Failed to fetch database schema (${res.status})`);
  }

  return res.json();
}

export async function fetchQueryHistory(limit: number = 50, offset: number = 0): Promise<QueryHistoryResponse> {
  const res = await fetch(`${API_BASE}/query-history?limit=${limit}&offset=${offset}`, {
    method: "GET",
    headers: { "Content-Type": "application/json" },
    cache: "no-store",
  });

  if (!res.ok) {
    throw new Error(`Failed to fetch query history (${res.status})`);
  }

  return res.json();
}

export async function validateSQL(sql: string) {
  const res = await fetch(`${API_BASE}/query/validate`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ sql }),
  });

  if (!res.ok) {
    throw new Error(`Failed to validate SQL (${res.status})`);
  }

  return res.json();
}
