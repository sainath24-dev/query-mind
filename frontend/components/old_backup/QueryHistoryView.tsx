"use client";

import React, { useState } from "react";
import { QueryHistoryItem } from "../types";
import { History, Play, Code2, Clock, CheckCircle2, AlertCircle, Copy, Check } from "lucide-react";

interface QueryHistoryViewProps {
  history: QueryHistoryItem[];
  onRerunQuery: (question: string) => void;
}

export const QueryHistoryView: React.FC<QueryHistoryViewProps> = ({ history, onRerunQuery }) => {
  const [selectedSQL, setSelectedSQL] = useState<string | null>(null);
  const [copied, setCopied] = useState(false);

  const handleCopy = (sql: string) => {
    navigator.clipboard.writeText(sql);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="space-y-6">
      {/* 1. Header */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-xl flex items-center justify-between">
        <div>
          <h2 className="text-xl font-bold text-white tracking-tight">Audit Trail & Query Execution Log</h2>
          <p className="text-sm text-slate-400 mt-1">
            Persisted history of all natural language questions, generated SQL statements, and PostgreSQL execution benchmarks.
          </p>
        </div>
        <div className="flex items-center space-x-1.5 px-3 py-1.5 rounded-lg bg-slate-950 border border-slate-800 text-xs text-slate-400">
          <History className="w-4 h-4 text-blue-400" />
          <span>{history.length} Queries Logged</span>
        </div>
      </div>

      {/* 2. SQL Modal / Drawer if inspected */}
      {selectedSQL && (
        <div className="bg-slate-950 border border-slate-800 rounded-xl p-5 shadow-2xl relative">
          <div className="flex items-center justify-between border-b border-slate-800 pb-3 mb-3">
            <span className="text-xs font-mono font-medium text-slate-400">Inspecting Generated SQL</span>
            <div className="flex items-center space-x-2">
              <button
                onClick={() => handleCopy(selectedSQL)}
                className="flex items-center space-x-1 px-2.5 py-1 rounded bg-slate-800 hover:bg-slate-700 text-xs text-slate-200 transition-colors"
              >
                {copied ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
                <span>{copied ? "Copied" : "Copy"}</span>
              </button>
              <button
                onClick={() => setSelectedSQL(null)}
                className="text-xs px-2 py-1 rounded bg-slate-800 hover:bg-slate-700 text-slate-400 hover:text-slate-200"
              >
                Close
              </button>
            </div>
          </div>
          <pre className="font-mono-code text-xs text-blue-300 overflow-x-auto whitespace-pre leading-relaxed">
            {selectedSQL}
          </pre>
        </div>
      )}

      {/* 3. History Table */}
      <div className="overflow-x-auto rounded-xl border border-slate-800 bg-slate-900 shadow-xl">
        <table className="w-full text-left border-collapse ide-table">
          <thead>
            <tr className="bg-slate-950 border-b border-slate-800 text-slate-400 text-xs">
              <th className="py-3 px-4 w-12 text-center">ID</th>
              <th className="py-3 px-4">Natural Language Question</th>
              <th className="py-3 px-3">Intent</th>
              <th className="py-3 px-3">Execution</th>
              <th className="py-3 px-3">Rows</th>
              <th className="py-3 px-3">Status</th>
              <th className="py-3 px-4">Timestamp</th>
              <th className="py-3 px-4 text-right">Actions</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800/60 font-mono-code text-xs">
            {history.length > 0 ? (
              history.map((item) => (
                <tr key={item.query_id} className="hover:bg-slate-800/40 transition-colors">
                  <td className="py-3 px-4 text-center text-slate-500">{item.query_id}</td>
                  <td className="py-3 px-4 font-sans font-medium text-slate-200 max-w-xs truncate">
                    {item.natural_language_question}
                  </td>
                  <td className="py-3 px-3">
                    <span className="text-[11px] px-2 py-0.5 rounded bg-blue-950/60 border border-blue-800/50 text-blue-300">
                      {item.intent || "QUERY"}
                    </span>
                  </td>
                  <td className="py-3 px-3 text-slate-400">
                    <div className="flex items-center space-x-1">
                      <Clock className="w-3 h-3 text-blue-400" />
                      <span>{item.execution_time_ms.toFixed(1)}ms</span>
                    </div>
                  </td>
                  <td className="py-3 px-3 text-slate-300">{item.row_count}</td>
                  <td className="py-3 px-3">
                    {item.status === "SUCCESS" ? (
                      <span className="inline-flex items-center space-x-1 text-emerald-400">
                        <CheckCircle2 className="w-3.5 h-3.5" />
                        <span>SUCCESS</span>
                      </span>
                    ) : (
                      <span className="inline-flex items-center space-x-1 text-rose-400">
                        <AlertCircle className="w-3.5 h-3.5" />
                        <span>{item.status}</span>
                      </span>
                    )}
                  </td>
                  <td className="py-3 px-4 text-slate-500 font-sans text-[11px]">
                    {new Date(item.created_at).toLocaleString()}
                  </td>
                  <td className="py-3 px-4 text-right font-sans">
                    <div className="flex items-center justify-end space-x-2">
                      <button
                        onClick={() => setSelectedSQL(item.generated_sql)}
                        className="p-1.5 rounded hover:bg-slate-800 text-slate-400 hover:text-blue-400 transition-colors"
                        title="View SQL"
                      >
                        <Code2 className="w-4 h-4" />
                      </button>
                      <button
                        onClick={() => onRerunQuery(item.natural_language_question)}
                        className="flex items-center space-x-1 px-2.5 py-1 rounded bg-blue-600/20 hover:bg-blue-600/30 text-blue-400 text-xs font-medium transition-colors"
                        title="Rerun Query"
                      >
                        <Play className="w-3 h-3" />
                        <span>Rerun</span>
                      </button>
                    </div>
                  </td>
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan={8} className="py-12 text-center text-slate-500 font-sans">
                  No query history recorded yet. Execute a query to populate the audit log.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};
