"use client";

import React, { useState, useRef, useEffect } from "react";
import {
  QueryResponse,
  VisualizationConfig
} from "../types";
import {
  ArrowUp,
  Copy,
  Check,
  Table as TableIcon,
  BarChart2,
  ChevronLeft,
  ChevronRight,
  Database,
  Clock,
  Code2,
  AlertCircle,
  HelpCircle,
  CornerDownLeft,
  Loader2
} from "lucide-react";
import { AppleBarChart } from "./AppleBarChart";

export interface ChatMessage {
  id: string;
  role: "user" | "assistant";
  text: string;
  queryResponse?: QueryResponse;
  error?: string;
  timestamp: string;
}

interface ChatInterfaceProps {
  messages: ChatMessage[];
  onSendMessage: (question: string) => void;
  isLoading: boolean;
}

const SAMPLE_PROMPTS = [
  "give me the data of student of all the aiml student",
  "Show top 10 students by CGPA in Computer Science",
  "Find all students with attendance below 75%",
  "List faculty members in Information Science department",
  "What is the average CGPA across all departments?",
  "Show total enrollment counts by department",
];

export const ChatInterface: React.FC<ChatInterfaceProps> = ({
  messages,
  onSendMessage,
  isLoading,
}) => {
  const [input, setInput] = useState("");
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLTextAreaElement>(null);

  // Auto scroll to bottom when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isLoading]);

  // Auto focus input
  useEffect(() => {
    inputRef.current?.focus();
  }, []);

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const handleSend = () => {
    if (!input.trim() || isLoading) return;
    const query = input.trim();
    setInput("");
    onSendMessage(query);
  };

  return (
    <div className="flex flex-col min-h-[calc(100vh-96px)] max-w-[860px] mx-auto w-full px-4 sm:px-6">
      {/* Empty State / Welcome Screen */}
      {messages.length === 0 ? (
        <div className="flex-1 flex flex-col items-center justify-center py-16 text-center space-y-8 my-auto">
          <div className="space-y-3 max-w-xl">
            <div className="w-16 h-16 rounded-2xl overflow-hidden shadow-sm mx-auto mb-4 border border-black/10">
              <img src="/logo-icon.jpg" alt="QueryMind" className="w-full h-full object-cover" />
            </div>
            <h2 className="text-[34px] sm:text-[40px] font-semibold tracking-[-0.025em] text-[#1d1d1f] leading-[1.15]">
              Ask your database in plain English.
            </h2>
            <p className="text-[17px] text-[#7a7a7a] tracking-[-0.022em] leading-relaxed">
              Enter any query to search, filter records, or inspect statistics.
            </p>
          </div>

          {/* Quick Starter Pills */}
          <div className="w-full max-w-2xl">
            <p className="text-[12px] font-medium uppercase tracking-wider text-[#7a7a7a] mb-3">
              Suggested queries to get started
            </p>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-2.5 text-left">
              {SAMPLE_PROMPTS.map((prompt, idx) => (
                <button
                  key={idx}
                  onClick={() => onSendMessage(prompt)}
                  className="p-3.5 bg-[#ffffff] border border-[#e0e0e0] hover:border-[#0066cc] hover:bg-[#fafafc] rounded-[18px] text-[14px] text-[#1d1d1f] transition-all text-left group flex items-start justify-between shadow-[0_1px_2px_rgba(0,0,0,0.02)] active:scale-[0.98]"
                >
                  <span className="line-clamp-2 pr-2 font-normal leading-snug">
                    {prompt}
                  </span>
                  <CornerDownLeft className="w-3.5 h-3.5 text-[#7a7a7a] opacity-0 group-hover:opacity-100 group-hover:text-[#0066cc] shrink-0 mt-0.5 transition-opacity" />
                </button>
              ))}
            </div>
          </div>
        </div>
      ) : (
        /* Conversation Feed */
        <div className="flex-1 py-8 space-y-8 pb-36">
          {messages.map((message) => (
            <MessageItem key={message.id} message={message} />
          ))}

          {/* Assistant Loading State */}
          {isLoading && (
            <div className="flex items-start space-x-3 text-left">
              <div className="w-7 h-7 rounded-lg overflow-hidden border border-black/10 shrink-0 mt-0.5">
                <img src="/logo-icon.jpg" alt="QueryMind" className="w-full h-full object-cover" />
              </div>
              <div className="flex-1 space-y-2">
                <div className="bg-[#ffffff] border border-[#e0e0e0] rounded-[18px] px-5 py-4 max-w-xl text-[15px] text-[#7a7a7a] flex items-center space-x-3 shadow-[0_1px_2px_rgba(0,0,0,0.02)]">
                  <Loader2 className="w-4 h-4 animate-spin text-[#0066cc]" />
                  <span>Generating SQL & querying PostgreSQL...</span>
                </div>
              </div>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>
      )}

      {/* Fixed Bottom Input Bar (Apple Pill Style) */}
      <div className="fixed bottom-0 left-0 right-0 z-40 bg-[#f5f5f7]/85 backdrop-blur-[20px] backdrop-saturate-[180%] border-t border-[#e0e0e0]/60 pb-6 pt-3">
        <div className="max-w-[860px] mx-auto px-4 sm:px-6">
          <div className="relative flex items-center bg-[#ffffff] border border-[#e0e0e0] focus-within:border-[#0071e3] focus-within:ring-2 focus-within:ring-[#0071e3]/20 rounded-full shadow-[0_2px_12px_rgba(0,0,0,0.04)] transition-all">
            <textarea
              ref={inputRef}
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Ask anything in humanized form (e.g., 'give me the data of student of all the aiml student')..."
              rows={1}
              className="w-full py-3.5 pl-6 pr-14 bg-transparent resize-none text-[16px] text-[#1d1d1f] placeholder:text-[#7a7a7a] outline-none rounded-full max-h-32 leading-normal"
              style={{ minHeight: "48px" }}
            />
            <button
              onClick={handleSend}
              disabled={!input.trim() || isLoading}
              className={`absolute right-2 p-2 rounded-full transition-all ${
                input.trim() && !isLoading
                  ? "bg-[#0066cc] text-[#ffffff] hover:bg-[#0071e3] active:scale-95 cursor-pointer"
                  : "bg-[#e8e8ed] text-[#7a7a7a] cursor-not-allowed opacity-60"
              }`}
              title="Send message (Enter)"
            >
              <ArrowUp className="w-4 h-4" />
            </button>
          </div>
          <p className="text-[11px] text-[#7a7a7a] text-center mt-2">
            Press <kbd className="font-mono bg-[#e8e8ed] px-1 py-0.5 rounded text-[10px]">Enter</kbd> to submit · <kbd className="font-mono bg-[#e8e8ed] px-1 py-0.5 rounded text-[10px]">Shift + Enter</kbd> for new line
          </p>
        </div>
      </div>
    </div>
  );
};

/* Individual Message Row */
const MessageItem: React.FC<{ message: ChatMessage }> = ({ message }) => {
  const isUser = message.role === "user";

  if (isUser) {
    return (
      <div className="flex justify-end">
        <div className="bg-[#e8e8ed] text-[#1d1d1f] px-5 py-3 rounded-[20px] rounded-br-[4px] max-w-2xl text-[16px] tracking-[-0.015em] leading-relaxed">
          {message.text}
        </div>
      </div>
    );
  }

  // Assistant Response
  const resp = message.queryResponse;

  return (
    <div className="flex items-start space-x-3 text-left">
      {/* QueryMind Avatar */}
      <div className="w-7 h-7 rounded-lg overflow-hidden border border-black/10 shrink-0 mt-0.5">
        <img src="/logo-icon.jpg" alt="QueryMind" className="w-full h-full object-cover" />
      </div>

      <div className="flex-1 space-y-4 max-w-full overflow-hidden">
        {/* Natural Language Explanation Text */}
        <div className="text-[17px] text-[#1d1d1f] tracking-[-0.022em] leading-relaxed">
          {message.text}
        </div>

        {/* If Query Failed or Unanswerable */}
        {message.error && (
          <div className="bg-[#ffffff] border border-[#ff3b30]/30 rounded-[18px] p-4 text-[14px] text-[#ff3b30] flex items-start space-x-2">
            <AlertCircle className="w-4 h-4 shrink-0 mt-0.5" />
            <span>{message.error}</span>
          </div>
        )}

        {/* If Query Succeeded and Has Response */}
        {resp && resp.status === "SUCCESS" && (
          <div className="space-y-4">
            {/* Generated SQL Code Block (Apple Dark Tile Style) */}
            {resp.sql && <SqlBlock sql={resp.sql} executionMs={resp.execution_time_ms} rowCount={resp.row_count} />}

            {/* Results Table & Visualization Card */}
            {resp.rows && resp.rows.length > 0 ? (
              <ResultDataView resp={resp} />
            ) : (
              <div className="bg-[#ffffff] border border-[#e0e0e0] rounded-[18px] p-6 text-center text-[#7a7a7a] text-[14px]">
                Query executed successfully, but no matching rows were found in the database.
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

/* Clean Apple Dark Tile SQL Code Block */
const SqlBlock: React.FC<{ sql: string; executionMs: number; rowCount: number }> = ({
  sql,
  executionMs,
  rowCount,
}) => {
  const [copied, setCopied] = useState(false);

  const handleCopy = () => {
    navigator.clipboard.writeText(sql);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="bg-[#272729] rounded-[18px] overflow-hidden text-[#ffffff] border border-[#2a2a2c]">
      {/* Top Bar */}
      <div className="flex items-center justify-between px-4 py-2.5 bg-[#252527] border-b border-[#333333] text-[12px]">
        <div className="flex items-center space-x-2">
          <Code2 className="w-3.5 h-3.5 text-[#2997ff]" />
          <span className="font-medium text-[#cccccc]">Generated SQL</span>
          <span className="text-[#7a7a7a]">·</span>
          <span className="text-[#7a7a7a]">{rowCount} rows in {executionMs.toFixed(1)}ms</span>
        </div>
        <button
          onClick={handleCopy}
          className="flex items-center space-x-1 text-[#cccccc] hover:text-[#ffffff] transition-colors py-1 px-2 rounded-md hover:bg-[#333333] text-[12px]"
          title="Copy SQL"
        >
          {copied ? (
            <>
              <Check className="w-3 h-3 text-[#34c759]" />
              <span className="text-[#34c759]">Copied</span>
            </>
          ) : (
            <>
              <Copy className="w-3 h-3" />
              <span>Copy</span>
            </>
          )}
        </button>
      </div>

      {/* Code Text */}
      <div className="p-4 overflow-x-auto">
        <pre className="font-mono text-[13px] leading-relaxed text-[#2997ff] whitespace-pre-wrap">
          {sql}
        </pre>
      </div>
    </div>
  );
};

/* Results Data View with Table / Chart toggle */
const ResultDataView: React.FC<{ resp: QueryResponse }> = ({ resp }) => {
  const [viewMode, setViewMode] = useState<"table" | "chart">("table");
  const [currentPage, setCurrentPage] = useState(1);
  const rowsPerPage = 10;

  const totalPages = Math.ceil(resp.rows.length / rowsPerPage);
  const paginatedRows = resp.rows.slice(
    (currentPage - 1) * rowsPerPage,
    currentPage * rowsPerPage
  );

  const canChart = resp.visualization && resp.visualization.can_visualize;

  return (
    <div className="bg-[#ffffff] border border-[#e0e0e0] rounded-[18px] overflow-hidden shadow-[0_1px_3px_rgba(0,0,0,0.02)]">
      {/* Header with Title and View Switcher */}
      <div className="flex items-center justify-between px-5 py-3 border-b border-[#e0e0e0] bg-[#fafafc]">
        <div className="flex items-center space-x-2 text-[13px] text-[#1d1d1f] font-medium">
          <TableIcon className="w-4 h-4 text-[#0066cc]" />
          <span>Results</span>
          <span className="text-[#7a7a7a] font-normal">({resp.rows.length} rows)</span>
        </div>

        {canChart && (
          <div className="flex items-center bg-[#e8e8ed] p-0.5 rounded-full text-[12px]">
            <button
              onClick={() => setViewMode("table")}
              className={`flex items-center space-x-1 px-3 py-1 rounded-full transition-all ${
                viewMode === "table"
                  ? "bg-[#ffffff] text-[#1d1d1f] shadow-sm font-medium"
                  : "text-[#7a7a7a] hover:text-[#1d1d1f]"
              }`}
            >
              <TableIcon className="w-3 h-3" />
              <span>Table</span>
            </button>
            <button
              onClick={() => setViewMode("chart")}
              className={`flex items-center space-x-1 px-3 py-1 rounded-full transition-all ${
                viewMode === "chart"
                  ? "bg-[#ffffff] text-[#1d1d1f] shadow-sm font-medium"
                  : "text-[#7a7a7a] hover:text-[#1d1d1f]"
              }`}
            >
              <BarChart2 className="w-3 h-3" />
              <span>Chart</span>
            </button>
          </div>
        )}
      </div>

      {/* Table View */}
      {viewMode === "table" ? (
        <div className="overflow-x-auto">
          <table className="w-full text-left text-[14px]">
            <thead className="bg-[#f5f5f7] border-b border-[#e0e0e0] text-[11px] font-semibold text-[#7a7a7a] uppercase tracking-wider">
              <tr>
                {resp.columns.map((col) => (
                  <th key={col} className="px-4 py-2.5 whitespace-nowrap">
                    {col.replace(/_/g, " ")}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody className="divide-y divide-[#f0f0f0]">
              {paginatedRows.map((row, idx) => (
                <tr key={idx} className="hover:bg-[#fafafc] transition-colors">
                  {resp.columns.map((col) => {
                    const val = row[col];
                    return (
                      <td key={col} className="px-4 py-3 whitespace-nowrap text-[#1d1d1f]">
                        {val === null || val === undefined ? (
                          <span className="text-[#7a7a7a] italic">null</span>
                        ) : typeof val === "boolean" ? (
                          val ? "Yes" : "No"
                        ) : (
                          String(val)
                        )}
                      </td>
                    );
                  })}
                </tr>
              ))}
            </tbody>
          </table>

          {/* Pagination Controls */}
          {totalPages > 1 && (
            <div className="flex items-center justify-between px-4 py-2.5 border-t border-[#e0e0e0] bg-[#fafafc] text-[12px] text-[#7a7a7a]">
              <span>
                Showing {(currentPage - 1) * rowsPerPage + 1} to{" "}
                {Math.min(currentPage * rowsPerPage, resp.rows.length)} of {resp.rows.length}
              </span>
              <div className="flex items-center space-x-1">
                <button
                  onClick={() => setCurrentPage((p) => Math.max(1, p - 1))}
                  disabled={currentPage === 1}
                  className="p-1 rounded hover:bg-[#e8e8ed] disabled:opacity-40 transition-colors"
                >
                  <ChevronLeft className="w-4 h-4" />
                </button>
                <span className="px-2 font-medium text-[#1d1d1f]">
                  Page {currentPage} of {totalPages}
                </span>
                <button
                  onClick={() => setCurrentPage((p) => Math.min(totalPages, p + 1))}
                  disabled={currentPage === totalPages}
                  className="p-1 rounded hover:bg-[#e8e8ed] disabled:opacity-40 transition-colors"
                >
                  <ChevronRight className="w-4 h-4" />
                </button>
              </div>
            </div>
          )}
        </div>
      ) : (
        /* Minimalist Chart View */
        <div className="p-6">
          <div className="mb-4">
            <h4 className="text-[15px] font-semibold text-[#1d1d1f]">
              {resp.visualization.title}
            </h4>
            <p className="text-[13px] text-[#7a7a7a]">
              {resp.visualization.description}
            </p>
          </div>
          <div className="w-full">
            {(() => {
              const xKey = resp.visualization.x_axis_key || resp.columns[0];
              const yKey = resp.visualization.y_axis_key || resp.columns[1];
              const chartData = resp.rows.slice(0, 15).map((row) => ({
                name: String(row[xKey] ?? ""),
                value: Number(row[yKey] ?? 0),
              }));
              return <AppleBarChart data={chartData} height={240} barColor="#0066cc" />;
            })()}
          </div>
        </div>
      )}
    </div>
  );
};

