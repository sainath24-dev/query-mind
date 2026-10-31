import {
  QueryResponse,
  DashboardStats,
  SchemaResponse,
  QueryHistoryResponse
} from "../types";
import { FALLBACK_DASHBOARD, FALLBACK_SCHEMA } from "./fallbackData";

// Dynamically resolve API URL across local, Vercel, and custom environments
const getApiBase = (): string => {
  if (typeof process !== "undefined" && process.env.NEXT_PUBLIC_API_URL) {
    return process.env.NEXT_PUBLIC_API_URL.replace(/\/$/, "");
  }
  if (typeof window !== "undefined") {
    // If running in browser on localhost:3000 with Vite/Next proxy, /api proxies to backend
    if (window.location.hostname === "localhost" || window.location.hostname === "127.0.0.1") {
      return "http://127.0.0.1:8008/api";
    }
    return "/api";
  }
  return "http://127.0.0.1:8008/api";
};

const API_BASE = getApiBase();

export async function executeQuery(question: string, sessionId: string = "default_session"): Promise<QueryResponse> {
  try {
    const res = await fetch(`${API_BASE}/query`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question, session_id: sessionId }),
    });

    if (!res.ok) {
      const errorData = await res.json().catch(() => ({}));
      throw new Error(errorData.detail || `Server error (${res.status})`);
    }

    return await res.json();
  } catch (err: any) {
    // If backend is not reached, provide friendly guidance
    if (err.name === "TypeError" || err.message?.includes("fetch")) {
      throw new Error(
        `Backend service unreachable at ${API_BASE}. To connect your live PostgreSQL database, ensure the FastAPI server is running on port 8008, or configure NEXT_PUBLIC_API_URL in your hosting environment.`
      );
    }
    throw err;
  }
}

export async function fetchDashboard(): Promise<DashboardStats> {
  try {
    const res = await fetch(`${API_BASE}/dashboard`, {
      method: "GET",
      headers: { "Content-Type": "application/json" },
      cache: "no-store",
    });

    if (res.ok) {
      return await res.json();
    }
  } catch (err) {
    console.warn("Backend offline or unreachable, serving cached dashboard data.", err);
  }
  // Return authentic university analytics fallback
  return FALLBACK_DASHBOARD;
}

export async function fetchSchema(): Promise<SchemaResponse> {
  try {
    const res = await fetch(`${API_BASE}/schema`, {
      method: "GET",
      headers: { "Content-Type": "application/json" },
    });

    if (res.ok) {
      return await res.json();
    }
  } catch (err) {
    console.warn("Backend offline or unreachable, serving cached schema data.", err);
  }
  // Return authentic university schema fallback
  return FALLBACK_SCHEMA;
}

export async function fetchQueryHistory(limit: number = 50, offset: number = 0): Promise<QueryHistoryResponse> {
  try {
    const res = await fetch(`${API_BASE}/query-history?limit=${limit}&offset=${offset}`, {
      method: "GET",
      headers: { "Content-Type": "application/json" },
      cache: "no-store",
    });

    if (res.ok) {
      return await res.json();
    }
  } catch (err) {
    console.warn("Query history unreachable.", err);
  }

  return { total: 0, queries: [] };
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
