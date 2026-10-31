"use client";

import React from "react";
import { MessageSquare, Database, BarChart3, Plus } from "lucide-react";

interface NavbarProps {
  activeTab: "chat" | "schema" | "dashboard";
  onTabChange: (tab: "chat" | "schema" | "dashboard") => void;
  onNewChat: () => void;
}

export const Navbar: React.FC<NavbarProps> = ({
  activeTab,
  onTabChange,
  onNewChat,
}) => {
  return (
    <header className="sticky top-0 z-50 w-full select-none">
      {/* 1. Global Nav: Ultra-thin black bar (44px) with custom Logo */}
      <div className="bg-[#000000] text-[#ffffff] h-[44px] flex items-center justify-between px-6 text-[12px] tracking-[-0.01em]">
        <div className="flex items-center space-x-3">
          <button
            onClick={() => onTabChange("chat")}
            className="flex items-center space-x-2.5 hover:opacity-90 transition-opacity"
          >
            <img
              src="/logo-icon.jpg"
              alt="QueryMind"
              className="w-6 h-6 rounded-[5px] object-cover border border-white/10"
            />
            <span className="font-semibold tracking-tight text-[14px] text-white">
              QueryMind
            </span>
          </button>
        </div>

        {/* Quiet engine status */}
        <div className="text-[12px] text-[#86868b]">
          PostgreSQL Engine
        </div>
      </div>

      {/* 2. Frosted Sub-Nav: 52px frosted parchment strip */}
      <div className="bg-[#f5f5f7]/85 backdrop-blur-[20px] backdrop-saturate-[180%] border-b border-[#e0e0e0] h-[52px] flex items-center justify-between px-6">
        {/* Left: View Title */}
        <div className="flex items-center space-x-2">
          <h1 className="text-[20px] font-semibold tracking-[-0.015em] text-[#1d1d1f]">
            {activeTab === "chat" && "Chat"}
            {activeTab === "schema" && "Schema"}
            {activeTab === "dashboard" && "Dashboard"}
          </h1>
        </div>

        {/* Center: Clean View Switcher */}
        <nav className="flex items-center bg-[#e8e8ed] p-1 rounded-full text-[13px]">
          <button
            onClick={() => onTabChange("chat")}
            className={`flex items-center space-x-1.5 px-4 py-1.5 rounded-full font-normal transition-all duration-150 ${
              activeTab === "chat"
                ? "bg-[#ffffff] text-[#1d1d1f] shadow-[0_1px_3px_rgba(0,0,0,0.08)] font-medium"
                : "text-[#7a7a7a] hover:text-[#1d1d1f]"
            }`}
          >
            <MessageSquare className="w-3.5 h-3.5" />
            <span>Chat</span>
          </button>

          <button
            onClick={() => onTabChange("schema")}
            className={`flex items-center space-x-1.5 px-4 py-1.5 rounded-full font-normal transition-all duration-150 ${
              activeTab === "schema"
                ? "bg-[#ffffff] text-[#1d1d1f] shadow-[0_1px_3px_rgba(0,0,0,0.08)] font-medium"
                : "text-[#7a7a7a] hover:text-[#1d1d1f]"
            }`}
          >
            <Database className="w-3.5 h-3.5" />
            <span>Schema</span>
          </button>

          <button
            onClick={() => onTabChange("dashboard")}
            className={`flex items-center space-x-1.5 px-4 py-1.5 rounded-full font-normal transition-all duration-150 ${
              activeTab === "dashboard"
                ? "bg-[#ffffff] text-[#1d1d1f] shadow-[0_1px_3px_rgba(0,0,0,0.08)] font-medium"
                : "text-[#7a7a7a] hover:text-[#1d1d1f]"
            }`}
          >
            <BarChart3 className="w-3.5 h-3.5" />
            <span>Dashboard</span>
          </button>
        </nav>

        {/* Right: + New Chat Primary CTA */}
        <div className="flex items-center">
          <button
            onClick={onNewChat}
            className="flex items-center space-x-1.5 bg-[#0066cc] text-[#ffffff] hover:bg-[#0071e3] px-4 py-1.5 rounded-full text-[13px] font-normal transition-colors active:scale-95 duration-150 shadow-none outline-none focus:ring-2 focus:ring-[#0071e3] focus:ring-offset-1"
          >
            <Plus className="w-4 h-4" />
            <span>New Chat</span>
          </button>
        </div>
      </div>
    </header>
  );
};
