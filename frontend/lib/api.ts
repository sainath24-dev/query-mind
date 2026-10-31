import {
  QueryResponse,
  DashboardStats,
  SchemaResponse,
  QueryHistoryResponse
} from "../types";
import { FALLBACK_DASHBOARD, FALLBACK_SCHEMA } from "./fallbackData";

// Dynamically resolve API URL across local, Vercel Services (internal binding), and production
const getApiBase = (): string => {
  // Client-side execution (browser)
  if (typeof window !== "undefined") {
    // In local development, call the local backend port directly
    if (window.location.hostname === "localhost" || window.location.hostname === "127.0.0.1") {
      return "http://127.0.0.1:8008/api";
    }
    // On Vercel / production public domain, use relative /api (routed by top-level rewrite)
    return "/api";
  }

  // Server-side execution (Next.js server runtime / functions)
  if (typeof process !== "undefined") {
    // 1. Bound internal service URL injected by Vercel Services
    if (process.env.BACKEND_URL) {
      const cleanUrl = process.env.BACKEND_URL.replace(/\/$/, "");
      return cleanUrl.endsWith("/api") ? cleanUrl : `${cleanUrl}/api`;
    }
    // 2. Custom public API URL
    if (process.env.NEXT_PUBLIC_API_URL) {
      return process.env.NEXT_PUBLIC_API_URL.replace(/\/$/, "");
    }
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
    if (err.name === "TypeError" || err.message?.includes("fetch")) {
      throw new Error(
        `Backend service unreachable at ${API_BASE}. To connect your live PostgreSQL database, ensure the FastAPI server is running on port 8008, or configure BACKEND_URL / NEXT_PUBLIC_API_URL.`
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
