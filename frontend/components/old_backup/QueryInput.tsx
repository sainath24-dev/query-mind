"use client";

import React, { useState } from "react";
import { Search, Sparkles, CornerDownLeft, Loader2, RefreshCw, MessageSquare } from "lucide-react";

interface QueryInputProps {
  onSearch: (question: string) => void;
  isLoading: boolean;
  previousQuestion?: string | null;
  onResetSession?: () => void;
}

const EXAMPLE_QUERIES = [
  "Show the top 10 students by CGPA.",
  "How many students are enrolled in each department?",
  "Which students have attendance below 75%?",
  "Show all AIML students who scored above 80 in Machine Learning.",
  "Which department has the highest average CGPA?",
  "Compare average marks between CSE and AIML.",
  "Show students who failed more than two subjects.",
  "Which faculty teaches the most students?",
  "What is the average salary of employees?",
  "Delete all students."
];

export const QueryInput: React.FC<QueryInputProps> = ({
  onSearch,
  isLoading,
  previousQuestion,
  onResetSession,
}) => {
  const [question, setQuestion] = useState("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!question.trim() || isLoading) return;
    onSearch(question.trim());
  };

  const handleSelectExample = (example: string) => {
    setQuestion(example);
    onSearch(example);
  };

  return (
    <div className="w-full bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-xl">
      {/* Session Context Banner if previous question exists */}
      {previousQuestion && (
        <div className="mb-4 flex items-center justify-between px-3.5 py-2 rounded-lg bg-blue-950/40 border border-blue-800/40 text-xs text-blue-300">
          <div className="flex items-center space-x-2">
            <MessageSquare className="w-4 h-4 text-blue-400" />
            <span>Conversational Memory Active. Previous: <strong>"{previousQuestion}"</strong></span>
          </div>
          <div className="flex items-center space-x-2">
            <span className="text-slate-400">Try follow-up: "Only show top 5" or "Show their attendance"</span>
            {onResetSession && (
              <button
                type="button"
                onClick={onResetSession}
                className="text-xs px-2 py-0.5 rounded bg-slate-800 hover:bg-slate-700 text-slate-300 transition-colors"
              >
                Reset Context
              </button>
            )}
          </div>
        </div>
      )}

      {/* Main Input Form */}
      <form onSubmit={handleSubmit} className="relative">
        <div className="relative flex items-center">
          <div className="absolute left-4 text-slate-400">
            <Search className="w-5 h-5" />
          </div>
          <input
            id="query-input"
            type="text"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            placeholder="Ask your relational database anything in plain English... (e.g. 'Show top 10 AIML students by CGPA')"
            disabled={isLoading}
            className="w-full pl-12 pr-32 py-3.5 bg-slate-950 border border-slate-800 rounded-lg text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-blue-500/50 focus:border-blue-500 transition-all font-sans text-base"
          />
          <button
            id="query-submit-btn"
            type="submit"
            disabled={isLoading || !question.trim()}
            className="absolute right-2 px-4 py-2 bg-blue-600 hover:bg-blue-500 disabled:bg-slate-800 disabled:text-slate-500 text-white rounded-md text-sm font-medium transition-colors flex items-center space-x-1.5 shadow-sm"
          >
            {isLoading ? (
              <>
                <Loader2 className="w-4 h-4 animate-spin" />
                <span>Running...</span>
              </>
            ) : (
              <>
                <span>Run Query</span>
                <CornerDownLeft className="w-3.5 h-3.5 opacity-70" />
              </>
            )}
          </button>
        </div>
      </form>

      {/* Suggestion Chips */}
      <div className="mt-4">
        <div className="flex items-center space-x-1.5 text-xs text-slate-400 mb-2">
          <Sparkles className="w-3.5 h-3.5 text-amber-400" />
          <span>Recommended Benchmark Queries:</span>
        </div>
        <div className="flex flex-wrap gap-2">
          {EXAMPLE_QUERIES.map((example, idx) => (
            <button
              key={idx}
              id={`suggestion-chip-${idx}`}
              type="button"
              onClick={() => handleSelectExample(example)}
              className="text-xs px-2.5 py-1.5 rounded-md bg-slate-950 hover:bg-slate-800 border border-slate-800 hover:border-slate-700 text-slate-300 transition-all text-left"
            >
              {example}
            </button>
          ))}
        </div>
      </div>
    </div>
  );
};
