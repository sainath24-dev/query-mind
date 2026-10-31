"use client";

import React, { useState } from "react";
import { SchemaResponse } from "../types";
import { Database, Key, ArrowRight, Table as TableIcon } from "lucide-react";

interface SchemaExplorerViewProps {
  schema: SchemaResponse;
  onQueryTable?: (tableName: string) => void;
}

export const SchemaExplorerView: React.FC<SchemaExplorerViewProps> = ({
  schema,
  onQueryTable,
}) => {
  const [selectedTableName, setSelectedTableName] = useState<string>(
    schema.tables[0]?.name || "students"
  );

  const selectedTable = schema.tables.find((t) => t.name === selectedTableName) || schema.tables[0];

  return (
    <div className="max-w-[1000px] mx-auto w-full py-8 px-4 sm:px-6 space-y-8">
      {/* Header */}
      <div className="space-y-2">
        <h2 className="text-[34px] font-semibold tracking-[-0.025em] text-[#1d1d1f] leading-tight">
          Schema Explorer
        </h2>
        <p className="text-[17px] text-[#7a7a7a] tracking-[-0.022em]">
          All {schema.tables.length} relational tables in your PostgreSQL database with columns, types, and constraints.
        </p>
      </div>

      {/* Main Content: Left table selector + Right table details card */}
      <div className="grid grid-cols-1 md:grid-cols-12 gap-6">
        {/* Left Column: Table List */}
        <div className="md:col-span-4 space-y-2">
          <p className="text-[12px] font-medium uppercase tracking-wider text-[#7a7a7a] px-1">
            Database Tables
          </p>
          <div className="space-y-1.5">
            {schema.tables.map((table) => {
              const isSelected = table.name === selectedTableName;
              return (
                <button
                  key={table.name}
                  onClick={() => setSelectedTableName(table.name)}
                  className={`w-full text-left px-4 py-3 rounded-[14px] border transition-all flex items-center justify-between group active:scale-[0.98] ${
                    isSelected
                      ? "bg-[#ffffff] border-[#0066cc] text-[#0066cc] shadow-sm font-medium"
                      : "bg-[#ffffff] border-[#e0e0e0] hover:border-[#cccccc] text-[#1d1d1f]"
                  }`}
                >
                  <div className="flex items-center space-x-2.5 truncate">
                    <TableIcon
                      className={`w-4 h-4 shrink-0 ${
                        isSelected ? "text-[#0066cc]" : "text-[#7a7a7a]"
                      }`}
                    />
                    <span className="text-[15px] truncate">{table.name}</span>
                  </div>
                  <span
                    className={`text-[12px] px-2 py-0.5 rounded-full ${
                      isSelected
                        ? "bg-[#0066cc]/10 text-[#0066cc]"
                        : "bg-[#f5f5f7] text-[#7a7a7a]"
                    }`}
                  >
                    {table.row_count.toLocaleString()}
                  </span>
                </button>
              );
            })}
          </div>
        </div>

        {/* Right Column: Table Detail Card (White Utility Card, 18px radius) */}
        <div className="md:col-span-8">
          {selectedTable && (
            <div className="bg-[#ffffff] border border-[#e0e0e0] rounded-[18px] p-6 sm:p-8 space-y-6 shadow-[0_1px_3px_rgba(0,0,0,0.02)]">
              {/* Table Top Info */}
              <div className="flex flex-wrap items-start justify-between gap-4 pb-4 border-b border-[#f0f0f0]">
                <div className="space-y-1">
                  <div className="flex items-center space-x-3">
                    <h3 className="text-[24px] font-semibold tracking-[-0.015em] text-[#1d1d1f]">
                      {selectedTable.name}
                    </h3>
                    <span className="text-[12px] font-medium bg-[#f5f5f7] text-[#7a7a7a] px-2.5 py-0.5 rounded-full border border-[#e0e0e0]">
                      {selectedTable.row_count.toLocaleString()} rows
                    </span>
                  </div>
                  <p className="text-[14px] text-[#7a7a7a] leading-relaxed">
                    {selectedTable.description || "Relational table in the academic database."}
                  </p>
                </div>

                {onQueryTable && (
                  <button
                    onClick={() => onQueryTable(selectedTable.name)}
                    className="flex items-center space-x-1.5 bg-[#0066cc] text-[#ffffff] hover:bg-[#0071e3] px-4 py-2 rounded-full text-[13px] font-normal transition-colors active:scale-95"
                  >
                    <span>Ask in Chat</span>
                  </button>
                )}
              </div>

              {/* Columns Table */}
              <div className="space-y-3">
                <h4 className="text-[13px] font-semibold uppercase tracking-wider text-[#7a7a7a]">
                  Columns ({selectedTable.columns.length})
                </h4>
                <div className="overflow-x-auto border border-[#e0e0e0] rounded-[14px]">
                  <table className="w-full text-left text-[13px]">
                    <thead className="bg-[#f5f5f7] border-b border-[#e0e0e0] text-[11px] font-semibold text-[#7a7a7a] uppercase tracking-wider">
                      <tr>
                        <th className="px-4 py-2.5">Name</th>
                        <th className="px-4 py-2.5">Type</th>
                        <th className="px-4 py-2.5">Key</th>
                        <th className="px-4 py-2.5">Description</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-[#f0f0f0]">
                      {selectedTable.columns.map((col) => (
                        <tr key={col.name} className="hover:bg-[#fafafc] transition-colors">
                          <td className="px-4 py-2.5 font-medium text-[#1d1d1f] font-mono text-[12px]">
                            {col.name}
                          </td>
                          <td className="px-4 py-2.5 text-[#7a7a7a] font-mono text-[12px]">
                            {col.data_type}
                          </td>
                          <td className="px-4 py-2.5 whitespace-nowrap">
                            {col.is_primary_key && (
                              <span className="inline-flex items-center space-x-1 bg-[#0066cc]/10 text-[#0066cc] text-[11px] px-2 py-0.5 rounded-full font-medium">
                                <Key className="w-3 h-3" />
                                <span>PK</span>
                              </span>
                            )}
                            {col.is_foreign_key && (
                              <span className="inline-flex items-center space-x-1 bg-[#8b5cf6]/10 text-[#8b5cf6] text-[11px] px-2 py-0.5 rounded-full font-medium">
                                <span>FK → {col.foreign_key_target}</span>
                              </span>
                            )}
                            {!col.is_primary_key && !col.is_foreign_key && (
                              <span className="text-[#cccccc] text-[12px]">—</span>
                            )}
                          </td>
                          <td className="px-4 py-2.5 text-[#7a7a7a] text-[12px]">
                            {col.description || "—"}
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
