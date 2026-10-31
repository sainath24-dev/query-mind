"use client";

import React from "react";
import { DashboardStats } from "../types";
import { Users, Building2, Award, CalendarCheck, ArrowRight } from "lucide-react";
import { AppleBarChart } from "./AppleBarChart";

interface DashboardViewProps {
  stats: DashboardStats;
  onSelectQuery?: (question: string) => void;
}

export const DashboardView: React.FC<DashboardViewProps> = ({ stats, onSelectQuery }) => {
  const chartData = (stats.department_distribution || []).map((d) => ({
    name: d.department_code,
    value: d.student_count,
  }));

  return (
    <div className="max-w-[1000px] mx-auto w-full py-8 px-4 sm:px-6 space-y-8">
      {/* Header */}
      <div className="space-y-2">
        <h2 className="text-[34px] font-semibold tracking-[-0.025em] text-[#1d1d1f] leading-tight">
          Database Overview
        </h2>
        <p className="text-[17px] text-[#7a7a7a] tracking-[-0.022em]">
          High-level academic statistics computed directly from PostgreSQL records.
        </p>
      </div>

      {/* 4 Clean Metric Cards (Apple Utility Cards, 18px radius) */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        {/* Total Students */}
        <div className="bg-[#ffffff] border border-[#e0e0e0] rounded-[18px] p-6 space-y-2 shadow-[0_1px_3px_rgba(0,0,0,0.02)]">
          <div className="flex items-center justify-between text-[#7a7a7a]">
            <span className="text-[13px] font-medium uppercase tracking-wider">Students</span>
            <Users className="w-4 h-4 text-[#0066cc]" />
          </div>
          <p className="text-[32px] font-semibold text-[#1d1d1f] tracking-tight">
            {stats.total_students.toLocaleString()}
          </p>
          <p className="text-[12px] text-[#7a7a7a]">Enrolled across all depts</p>
        </div>

        {/* Total Departments */}
        <div className="bg-[#ffffff] border border-[#e0e0e0] rounded-[18px] p-6 space-y-2 shadow-[0_1px_3px_rgba(0,0,0,0.02)]">
          <div className="flex items-center justify-between text-[#7a7a7a]">
            <span className="text-[13px] font-medium uppercase tracking-wider">Departments</span>
            <Building2 className="w-4 h-4 text-[#0066cc]" />
          </div>
          <p className="text-[32px] font-semibold text-[#1d1d1f] tracking-tight">
            {stats.total_departments.toLocaleString()}
          </p>
          <p className="text-[12px] text-[#7a7a7a]">Engineering disciplines</p>
        </div>

        {/* Average CGPA */}
        <div className="bg-[#ffffff] border border-[#e0e0e0] rounded-[18px] p-6 space-y-2 shadow-[0_1px_3px_rgba(0,0,0,0.02)]">
          <div className="flex items-center justify-between text-[#7a7a7a]">
            <span className="text-[13px] font-medium uppercase tracking-wider">Avg CGPA</span>
            <Award className="w-4 h-4 text-[#0066cc]" />
          </div>
          <p className="text-[32px] font-semibold text-[#1d1d1f] tracking-tight">
            {stats.average_cgpa.toFixed(2)}
          </p>
          <p className="text-[12px] text-[#7a7a7a]">Out of 10.0 scale</p>
        </div>

        {/* Average Attendance */}
        <div className="bg-[#ffffff] border border-[#e0e0e0] rounded-[18px] p-6 space-y-2 shadow-[0_1px_3px_rgba(0,0,0,0.02)]">
          <div className="flex items-center justify-between text-[#7a7a7a]">
            <span className="text-[13px] font-medium uppercase tracking-wider">Attendance</span>
            <CalendarCheck className="w-4 h-4 text-[#0066cc]" />
          </div>
          <p className="text-[32px] font-semibold text-[#1d1d1f] tracking-tight">
            {stats.average_attendance.toFixed(1)}%
          </p>
          <p className="text-[12px] text-[#7a7a7a]">Class participation rate</p>
        </div>
      </div>

      {/* 1 Clean Minimalist Chart (White Card, 18px radius) */}
      {chartData.length > 0 && (
        <div className="bg-[#ffffff] border border-[#e0e0e0] rounded-[18px] p-6 sm:p-8 space-y-4 shadow-[0_1px_3px_rgba(0,0,0,0.02)]">
          <div>
            <h3 className="text-[21px] font-semibold tracking-[-0.015em] text-[#1d1d1f]">
              Student Distribution by Department
            </h3>
            <p className="text-[14px] text-[#7a7a7a] mt-0.5">
              Enrolled students across academic branches.
            </p>
          </div>

          <div className="w-full pt-4">
            <AppleBarChart data={chartData} height={260} barColor="#0066cc" />
          </div>
        </div>
      )}

      {/* Quick Action Queries */}
      {onSelectQuery && (
        <div className="space-y-3 pt-2">
          <p className="text-[12px] font-medium uppercase tracking-wider text-[#7a7a7a]">
            Explore via Chat
          </p>
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-2.5">
            {[
              "Show top 5 departments by average CGPA",
              "Find all students with attendance below 75%",
              "List all subjects offered in Semester 5",
            ].map((q, idx) => (
              <button
                key={idx}
                onClick={() => onSelectQuery(q)}
                className="p-3.5 bg-[#ffffff] border border-[#e0e0e0] hover:border-[#0066cc] rounded-[18px] text-[13px] text-[#1d1d1f] text-left transition-all flex items-center justify-between group active:scale-[0.98]"
              >
                <span className="truncate pr-2">{q}</span>
                <ArrowRight className="w-3.5 h-3.5 text-[#7a7a7a] group-hover:text-[#0066cc] group-hover:translate-x-0.5 transition-all shrink-0" />
              </button>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};
