"use client";

import React, { useState } from "react";
import {
  QueryResponse,
  VisualizationConfig
} from "../types";
import {
  Table as TableIcon,
  BarChart2,
  Code2,
  Copy,
  Check,
  Clock,
  Database,
  Tag,
  AlertTriangle,
  Info,
  ChevronDown,
  ChevronUp,
  ShieldAlert
} from "lucide-react";
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  LineChart,
  Line,
  PieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend
} from "recharts";

interface ResultSectionProps {
  data: QueryResponse;
}

const CHART_COLORS = [
  "#3b82f6", "#10b981", "#f59e0b", "#8b5cf6",
  "#ec4899", "#06b6d4", "#f97316", "#14b8a6"
];

export const ResultSection: React.FC<ResultSectionProps> = ({ data }) => {
  const [activeView, setActiveView] = useState<"table" | "chart" | "sql">(
    data.visualization.can_visualize ? "chart" : "table"
  );
  const [copied, setCopied] = useState(false);
  const [isSqlExpanded, setIsSqlExpanded] = useState(true);
  const [currentPage, setCurrentPage] = useState(1);
  const rowsPerPage = 10;

  const handleCopySQL = () => {
    navigator.clipboard.writeText(data.sql);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  // Pagination calculation
  const totalPages = Math.ceil((data.rows?.length || 0) / rowsPerPage) || 1;
  const paginatedRows = data.rows?.slice((currentPage - 1) * rowsPerPage, currentPage * rowsPerPage) || [];

  // Render Chart based on backend recommendation
  const renderVisualization = () => {
    if (!data.visualization.can_visualize || !data.rows || data.rows.length === 0) {
      return (
        <div className="h-64 flex flex-col items-center justify-center text-slate-400 bg-slate-950/50 rounded-lg border border-slate-800">
          <BarChart2 className="w-8 h-8 opacity-40 mb-2" />
          <p className="text-sm">Visualization not suitable or data is empty for this query structure.</p>
        </div>
      );
    }

    const { recommended_chart, x_axis_key, y_axis_key, title } = data.visualization;
    const xKey = x_axis_key || data.columns[0];
    const yKey = y_axis_key || (data.columns[1] || data.columns[0]);

    // Format chart rows so numbers are properly parsed
    const chartData = data.rows.map((r) => {
      const formatted: Record<string, any> = { ...r };
      if (yKey && typeof formatted[yKey] === "string" && !isNaN(Number(formatted[yKey]))) {
        formatted[yKey] = Number(formatted[yKey]);
      }
      return formatted;
    });

    return (
      <div className="bg-slate-950 p-4 rounded-lg border border-slate-800">
        {title && <h4 className="text-sm font-semibold text-slate-300 mb-4">{title}</h4>}
        <div className="h-80 w-full">
          <ResponsiveContainer width="100%" height="100%">
            {recommended_chart === "line" ? (
              <LineChart data={chartData} margin={{ top: 10, right: 30, left: 10, bottom: 25 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                <XAxis dataKey={xKey} stroke="#64748b" tick={{ fill: "#94a3b8", fontSize: 11 }} angle={-20} textAnchor="end" />
                <YAxis stroke="#64748b" tick={{ fill: "#94a3b8", fontSize: 11 }} />
                <Tooltip contentStyle={{ backgroundColor: "#0f172a", borderColor: "#334155", borderRadius: "8px", color: "#f8fafc" }} />
                <Legend />
                <Line type="monotone" dataKey={yKey} stroke="#3b82f6" strokeWidth={2.5} dot={{ r: 4 }} activeDot={{ r: 6 }} />
              </LineChart>
            ) : recommended_chart === "pie" ? (
              <PieChart margin={{ top: 10, right: 10, left: 10, bottom: 10 }}>
                <Pie
                  data={chartData}
                  dataKey={yKey}
                  nameKey={xKey}
                  cx="50%"
                  cy="50%"
                  outerRadius={95}
                  innerRadius={50}
                  paddingAngle={3}
                  label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
                >
                  {chartData.map((_, index) => (
                    <Cell key={`cell-${index}`} fill={CHART_COLORS[index % CHART_COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip contentStyle={{ backgroundColor: "#0f172a", borderColor: "#334155", borderRadius: "8px", color: "#f8fafc" }} />
                <Legend />
              </PieChart>
            ) : (
              <BarChart data={chartData} margin={{ top: 10, right: 30, left: 10, bottom: 35 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                <XAxis dataKey={xKey} stroke="#64748b" tick={{ fill: "#94a3b8", fontSize: 11 }} angle={-25} textAnchor="end" />
                <YAxis stroke="#64748b" tick={{ fill: "#94a3b8", fontSize: 11 }} />
                <Tooltip contentStyle={{ backgroundColor: "#0f172a", borderColor: "#334155", borderRadius: "8px", color: "#f8fafc" }} />
                <Bar dataKey={yKey} fill="#3b82f6" radius={[4, 4, 0, 0]}>
                  {chartData.map((_, index) => (
                    <Cell key={`bar-${index}`} fill={CHART_COLORS[index % CHART_COLORS.length]} />
                  ))}
                </Bar>
              </BarChart>
            )}
          </ResponsiveContainer>
        </div>
      </div>
    );
  };

  // Handle Unanswerable / Security Alert state
  if (data.status === "UNANSWERABLE" || !data.is_answerable) {
    return (
      <div className="w-full bg-slate-900 border border-amber-900/50 rounded-xl p-6 shadow-xl">
        <div className="flex items-start space-x-3">
          <div className="p-2 rounded-lg bg-amber-950/60 border border-amber-700/50 text-amber-400">
            <Info className="w-6 h-6" />
          </div>
          <div>
            <h3 className="text-base font-semibold text-amber-300">Question Cannot Be Answered From Schema</h3>
            <p className="mt-1.5 text-sm text-slate-300 leading-relaxed">{data.explanation}</p>
            <div className="mt-4 p-3 rounded-lg bg-slate-950 border border-slate-800 text-xs text-slate-400">
              <strong>Database Scope:</strong> The university schema supports inquiries on <em>students, departments, subjects, faculty, enrollments, marks (internal/external/total/grades), and attendance</em>.
            </div>
          </div>
        </div>
      </div>
    );
  }

  // Handle Destructive / Security Violation state
  if (data.intent === "DESTRUCTIVE_PROHIBITED" || (data.status === "ERROR" && data.error_message?.toLowerCase().includes("prohibited"))) {
    return (
      <div className="w-full bg-slate-900 border border-rose-900/50 rounded-xl p-6 shadow-xl">
        <div className="flex items-start space-x-3">
          <div className="p-2 rounded-lg bg-rose-950/60 border border-rose-700/50 text-rose-400">
            <ShieldAlert className="w-6 h-6" />
          </div>
          <div>
            <h3 className="text-base font-semibold text-rose-400">Security Policy Violation: Destructive Statement Prohibited</h3>
            <p className="mt-1.5 text-sm text-slate-300 leading-relaxed">{data.explanation}</p>
            <div className="mt-4 p-3 rounded-lg bg-slate-950 border border-slate-800 text-xs text-rose-300 font-mono">
              Enforcement: All queries run through AST parser rejecting DELETE/DROP/UPDATE/TRUNCATE. Database connected with restricted user `querymind_readonly`.
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="w-full bg-slate-900 border border-slate-800 rounded-xl shadow-xl overflow-hidden">
      {/* 1. Header: Query Interpretation & Pipeline Metadata */}
      <div className="p-5 border-b border-slate-800 bg-slate-900/60">
        <div className="flex flex-wrap items-center justify-between gap-3">
          {/* Intent & Entity Pills */}
          <div className="flex flex-wrap items-center gap-2">
            <span className="text-xs uppercase font-bold tracking-wider px-2.5 py-1 rounded-md bg-blue-900/50 border border-blue-700/60 text-blue-300 flex items-center space-x-1.5">
              <Tag className="w-3.5 h-3.5 text-blue-400" />
              <span>Intent: {data.intent}</span>
            </span>

            {data.entities.departments?.map((dept, i) => (
              <span key={`dept-${i}`} className="text-xs px-2 py-0.5 rounded bg-slate-800 border border-slate-700 text-slate-300">
                Dept: <strong>{dept}</strong>
              </span>
            ))}

            {data.entities.subjects?.map((sub, i) => (
              <span key={`sub-${i}`} className="text-xs px-2 py-0.5 rounded bg-slate-800 border border-slate-700 text-slate-300">
                Subject: <strong>{sub}</strong>
              </span>
            ))}

            {data.entities.limit && (
              <span className="text-xs px-2 py-0.5 rounded bg-slate-800 border border-slate-700 text-slate-300">
                Limit: <strong>{data.entities.limit}</strong>
              </span>
            )}

            {data.entities.conditions?.map((c, i) => (
              <span key={`cond-${i}`} className="text-xs px-2 py-0.5 rounded bg-emerald-950/40 border border-emerald-800/40 text-emerald-300">
                {c.attribute || c.column} {c.operator} {c.value}
              </span>
            ))}
          </div>

          {/* Performance & Execution Metadata */}
          <div className="flex items-center space-x-4 text-xs text-slate-400">
            <div className="flex items-center space-x-1">
              <Clock className="w-3.5 h-3.5 text-blue-400" />
              <span>{data.execution_time_ms.toFixed(2)} ms</span>
            </div>
            <div className="flex items-center space-x-1">
              <TableIcon className="w-3.5 h-3.5 text-emerald-400" />
              <span>{data.row_count} {data.row_count === 1 ? "row" : "rows"}</span>
            </div>
            <div className="flex items-center space-x-1">
              <Database className="w-3.5 h-3.5 text-purple-400" />
              <span>{data.tables_used?.join(", ") || "db"}</span>
            </div>
          </div>
        </div>
      </div>

      {/* 2. Natural Language Explanation Card */}
      <div className="px-5 py-3.5 bg-blue-950/20 border-b border-slate-800/80 flex items-start space-x-2.5">
        <div className="p-1 rounded bg-blue-600/20 text-blue-400 mt-0.5">
          <Info className="w-4 h-4" />
        </div>
        <p className="text-sm text-slate-200 leading-relaxed font-sans">{data.explanation}</p>
      </div>

      {/* 3. Main Result View Switcher (Table / Chart / Raw SQL) */}
      <div className="p-5">
        <div className="flex items-center justify-between mb-4">
          <div className="flex space-x-1 bg-slate-950 p-1 rounded-lg border border-slate-800">
            <button
              id="view-tab-table"
              onClick={() => setActiveView("table")}
              className={`flex items-center space-x-1.5 px-3 py-1.5 rounded-md text-xs font-medium transition-colors ${
                activeView === "table"
                  ? "bg-slate-800 text-blue-400 shadow-sm"
                  : "text-slate-400 hover:text-slate-200"
              }`}
            >
              <TableIcon className="w-3.5 h-3.5" />
              <span>Table Grid ({data.row_count})</span>
            </button>

            <button
              id="view-tab-chart"
              onClick={() => setActiveView("chart")}
              className={`flex items-center space-x-1.5 px-3 py-1.5 rounded-md text-xs font-medium transition-colors ${
                activeView === "chart"
                  ? "bg-slate-800 text-blue-400 shadow-sm"
                  : "text-slate-400 hover:text-slate-200"
              }`}
            >
              <BarChart2 className="w-3.5 h-3.5" />
              <span>Visualization {data.visualization.can_visualize ? "(Active)" : ""}</span>
            </button>

            <button
              id="view-tab-sql"
              onClick={() => setActiveView("sql")}
              className={`flex items-center space-x-1.5 px-3 py-1.5 rounded-md text-xs font-medium transition-colors ${
                activeView === "sql"
                  ? "bg-slate-800 text-blue-400 shadow-sm"
                  : "text-slate-400 hover:text-slate-200"
              }`}
            >
              <Code2 className="w-3.5 h-3.5" />
              <span>Raw SQL</span>
            </button>
          </div>
        </div>

        {/* View Content: Table */}
        {activeView === "table" && (
          <div>
            <div className="overflow-x-auto rounded-lg border border-slate-800 bg-slate-950">
              <table className="w-full text-left border-collapse ide-table">
                <thead>
                  <tr className="bg-slate-900 border-b border-slate-800 text-slate-400">
                    <th className="py-2.5 px-3 text-slate-500 w-12 text-center">#</th>
                    {data.columns.map((col, idx) => (
                      <th key={idx} className="py-2.5 px-4 font-semibold text-slate-300">
                        {col}
                      </th>
                    ))}
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-800/60 font-mono-code text-xs">
                  {paginatedRows.length > 0 ? (
                    paginatedRows.map((row, rIdx) => (
                      <tr key={rIdx} className="hover:bg-slate-900/60 transition-colors">
                        <td className="py-2.5 px-3 text-center text-slate-600">
                          {(currentPage - 1) * rowsPerPage + rIdx + 1}
                        </td>
                        {data.columns.map((col, cIdx) => (
                          <td key={cIdx} className="py-2.5 px-4 text-slate-200">
                            {row[col] !== null && row[col] !== undefined ? String(row[col]) : (
                              <span className="text-slate-600 italic">null</span>
                            )}
                          </td>
                        ))}
                      </tr>
                    ))
                  ) : (
                    <tr>
                      <td colSpan={data.columns.length + 1} className="py-8 text-center text-slate-500 font-sans">
                        No rows returned for this query.
                      </td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>

            {/* Pagination Controls */}
            {totalPages > 1 && (
              <div className="flex items-center justify-between mt-3 text-xs text-slate-400">
                <span>
                  Showing {(currentPage - 1) * rowsPerPage + 1} to{" "}
                  {Math.min(currentPage * rowsPerPage, data.rows.length)} of {data.rows.length} records
                </span>
                <div className="flex space-x-1.5">
                  <button
                    disabled={currentPage === 1}
                    onClick={() => setCurrentPage((p) => Math.max(1, p - 1))}
                    className="px-2.5 py-1 rounded bg-slate-800 hover:bg-slate-700 disabled:opacity-40 disabled:hover:bg-slate-800 text-slate-300"
                  >
                    Previous
                  </button>
                  <span className="px-2 py-1 text-slate-500">
                    Page {currentPage} of {totalPages}
                  </span>
                  <button
                    disabled={currentPage === totalPages}
                    onClick={() => setCurrentPage((p) => Math.min(totalPages, p + 1))}
                    className="px-2.5 py-1 rounded bg-slate-800 hover:bg-slate-700 disabled:opacity-40 disabled:hover:bg-slate-800 text-slate-300"
                  >
                    Next
                  </button>
                </div>
              </div>
            )}
          </div>
        )}

        {/* View Content: Visualization */}
        {activeView === "chart" && renderVisualization()}

        {/* View Content: Raw SQL */}
        {activeView === "sql" && (
          <div className="bg-slate-950 rounded-lg border border-slate-800 overflow-hidden">
            <div className="flex items-center justify-between px-4 py-2 border-b border-slate-800 bg-slate-900/70 text-xs">
              <span className="font-mono text-slate-400">PostgreSQL Generated Statement</span>
              <button
                onClick={handleCopySQL}
                className="flex items-center space-x-1 px-2 py-1 rounded bg-slate-800 hover:bg-slate-700 text-slate-300 transition-colors"
              >
                {copied ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
                <span>{copied ? "Copied" : "Copy SQL"}</span>
              </button>
            </div>
            <pre className="p-4 font-mono-code text-xs text-blue-300 overflow-x-auto whitespace-pre leading-relaxed">
              {data.sql}
            </pre>
          </div>
        )}
      </div>

      {/* 4. Collapsible Transparent SQL Drawer below results (for educational viva inspection) */}
      {activeView !== "sql" && (
        <div className="border-t border-slate-800 bg-slate-950/60">
          <button
            onClick={() => setIsSqlExpanded(!isSqlExpanded)}
            className="w-full flex items-center justify-between px-5 py-2.5 text-xs text-slate-400 hover:text-slate-200 transition-colors"
          >
            <div className="flex items-center space-x-2">
              <Code2 className="w-4 h-4 text-blue-400" />
              <span className="font-medium">Underlying Generated SQL Query (Educational Transparency)</span>
            </div>
            <div className="flex items-center space-x-2">
              <span className="text-[11px] text-slate-500 font-mono">SELECT ...</span>
              {isSqlExpanded ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
            </div>
          </button>
          {isSqlExpanded && (
            <div className="px-5 pb-4">
              <div className="relative bg-slate-950 p-3.5 rounded-lg border border-slate-800 font-mono-code text-xs text-blue-300 overflow-x-auto whitespace-pre">
                <button
                  onClick={handleCopySQL}
                  className="absolute top-2 right-2 p-1.5 rounded bg-slate-900 hover:bg-slate-800 text-slate-400 hover:text-slate-200"
                  title="Copy SQL"
                >
                  {copied ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
                </button>
                {data.sql}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
};
