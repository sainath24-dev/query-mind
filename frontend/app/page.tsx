"use client";

import React, { useState, useEffect } from "react";
import { Navbar } from "../components/Navbar";
import { ChatInterface, ChatMessage } from "../components/ChatInterface";
import { SchemaExplorerView } from "../components/SchemaExplorerView";
import { ArchitectureView } from "../components/ArchitectureView";
import { DashboardView } from "../components/DashboardView";
import {
  QueryResponse,
  DashboardStats,
  SchemaResponse,
} from "../types";
import {
  executeQuery,
  fetchDashboard,
  fetchSchema,
} from "../lib/api";
import { Loader2 } from "lucide-react";

export default function Home() {
  const [activeTab, setActiveTab] = useState<"chat" | "architecture" | "schema" | "dashboard">("chat");
  const [isLoading, setIsLoading] = useState(false);

  // Conversational session ID
  const [sessionId, setSessionId] = useState<string>(() => "session_" + Math.random().toString(36).substring(2, 9));

  // Chat conversation history
  const [messages, setMessages] = useState<ChatMessage[]>([]);

  // Asynchronous Data States for Schema & Dashboard
  const [dashboardStats, setDashboardStats] = useState<DashboardStats | null>(null);
  const [schemaData, setSchemaData] = useState<SchemaResponse | null>(null);

  // Load initial dashboard & schema data in the background
  useEffect(() => {
    loadDashboard();
    loadSchema();
  }, []);

  const loadDashboard = async () => {
    try {
      const data = await fetchDashboard();
      setDashboardStats(data);
    } catch (err: any) {
      console.error("Dashboard fetch error:", err);
    }
  };

  const loadSchema = async () => {
    try {
      const data = await fetchSchema();
      setSchemaData(data);
    } catch (err: any) {
      console.error("Schema fetch error:", err);
    }
  };

  const handleSendMessage = async (question: string) => {
    if (!question.trim() || isLoading) return;

    const userMessage: ChatMessage = {
      id: "user_" + Date.now(),
      role: "user",
      text: question.trim(),
      timestamp: new Date().toLocaleTimeString(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setIsLoading(true);

    try {
      const result: QueryResponse = await executeQuery(question, sessionId);

      let assistantText = result.explanation;
      if (!assistantText) {
        if (result.row_count > 0) {
          assistantText = `Here are the results from PostgreSQL (${result.row_count} records returned in ${result.execution_time_ms.toFixed(1)}ms).`;
        } else {
          assistantText = "Query executed successfully, but returned 0 rows matching your criteria.";
        }
      }

      const assistantMessage: ChatMessage = {
        id: "assistant_" + Date.now(),
        role: "assistant",
        text: assistantText,
        queryResponse: result,
        timestamp: new Date().toLocaleTimeString(),
      };

      setMessages((prev) => [...prev, assistantMessage]);
    } catch (err: any) {
      const assistantErrorMessage: ChatMessage = {
        id: "assistant_err_" + Date.now(),
        role: "assistant",
        text: "I encountered an issue processing your natural language request.",
        error: err.message || "Failed to execute query on PostgreSQL database.",
        timestamp: new Date().toLocaleTimeString(),
      };
      setMessages((prev) => [...prev, assistantErrorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleNewChat = () => {
    setMessages([]);
    setSessionId("session_" + Math.random().toString(36).substring(2, 9));
    setActiveTab("chat");
  };

  const handleQueryFromOtherView = (question: string) => {
    setActiveTab("chat");
    handleSendMessage(question);
  };

  const handleQueryTable = (tableName: string) => {
    setActiveTab("chat");
    handleSendMessage(`Show me 10 records from ${tableName} table`);
  };

  return (
    <div className="min-h-screen flex flex-col bg-[#f5f5f7] text-[#1d1d1f]">
      {/* 2-Row Apple Navigation Bar */}
      <Navbar
        activeTab={activeTab}
        onTabChange={setActiveTab}
        onNewChat={handleNewChat}
      />

      {/* Main View Area */}
      <main className="flex-1 flex flex-col">
        {/* Tab 1: ChatGPT-style Conversational Assistant */}
        {activeTab === "chat" && (
          <ChatInterface
            messages={messages}
            onSendMessage={handleSendMessage}
            isLoading={isLoading}
          />
        )}

        {/* Tab 2: End-to-End Pipeline Architecture & How It Works */}
        {activeTab === "architecture" && (
          <ArchitectureView
            onSelectQuery={handleQueryFromOtherView}
          />
        )}

        {/* Tab 3: Ultra-Simple Schema Explorer */}
        {activeTab === "schema" && (
          schemaData ? (
            <SchemaExplorerView
              schema={schemaData}
              onQueryTable={handleQueryTable}
            />
          ) : (
            <div className="flex-1 flex flex-col items-center justify-center p-16 space-y-3 text-[#7a7a7a]">
              <Loader2 className="w-6 h-6 animate-spin text-[#0066cc]" />
              <p className="text-[14px]">Loading schema from PostgreSQL...</p>
            </div>
          )
        )}

        {/* Tab 3: Ultra-Simple Dashboard */}
        {activeTab === "dashboard" && (
          dashboardStats ? (
            <DashboardView
              stats={dashboardStats}
              onSelectQuery={handleQueryFromOtherView}
            />
          ) : (
            <div className="flex-1 flex flex-col items-center justify-center p-16 space-y-3 text-[#7a7a7a]">
              <Loader2 className="w-6 h-6 animate-spin text-[#0066cc]" />
              <p className="text-[14px]">Loading metrics from PostgreSQL...</p>
            </div>
          )
        )}
      </main>
    </div>
  );
}
