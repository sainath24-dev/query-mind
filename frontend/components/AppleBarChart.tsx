"use client";

import React, { useState } from "react";

export interface BarChartDataPoint {
  name: string;
  value: number;
  [key: string]: any;
}

interface AppleBarChartProps {
  data: BarChartDataPoint[];
  height?: number;
  barColor?: string;
}

export const AppleBarChart: React.FC<AppleBarChartProps> = ({
  data,
  height = 240,
  barColor = "#0066cc",
}) => {
  const [hoveredIndex, setHoveredIndex] = useState<number | null>(null);

  if (!data || data.length === 0) {
    return (
      <div className="flex items-center justify-center h-48 text-[#7a7a7a] text-[14px]">
        No data available to display
      </div>
    );
  }

  const maxValue = Math.max(...data.map((d) => d.value), 1);
  const chartHeight = height;
  const paddingBottom = 40;
  const paddingTop = 20;
  const usableHeight = chartHeight - paddingBottom - paddingTop;

  return (
    <div className="w-full select-none">
      {/* Chart Canvas */}
      <div className="relative w-full" style={{ height: `${chartHeight}px` }}>
        {/* Subtle Horizontal Grid lines */}
        <div className="absolute inset-0 flex flex-col justify-between pointer-events-none" style={{ height: `${chartHeight - paddingBottom}px`, paddingTop: `${paddingTop}px` }}>
          <div className="border-b border-[#f0f0f0] w-full" />
          <div className="border-b border-[#f0f0f0] w-full" />
          <div className="border-b border-[#f0f0f0] w-full" />
        </div>

        {/* Bars Container */}
        <div className="absolute inset-x-0 bottom-[40px] top-[20px] flex items-end justify-around gap-2 px-4">
          {data.map((item, index) => {
            const barHeightPct = Math.min(100, Math.max(4, (item.value / maxValue) * 100));
            const isHovered = hoveredIndex === index;

            return (
              <div
                key={index}
                className="relative flex-1 flex flex-col items-center h-full justify-end group cursor-pointer"
                onMouseEnter={() => setHoveredIndex(index)}
                onMouseLeave={() => setHoveredIndex(null)}
              >
                {/* Tooltip on hover */}
                {isHovered && (
                  <div className="absolute -top-10 z-20 bg-[#1d1d1f] text-white text-[12px] font-medium px-2.5 py-1 rounded-[6px] shadow-lg whitespace-nowrap animate-in fade-in zoom-in-95 pointer-events-none">
                    <span className="font-semibold">{item.name}:</span> {item.value.toLocaleString()}
                  </div>
                )}

                {/* The Bar */}
                <div
                  className="w-full max-w-[48px] rounded-t-[6px] transition-all duration-200"
                  style={{
                    height: `${barHeightPct}%`,
                    backgroundColor: isHovered ? "#0071e3" : barColor,
                    transform: isHovered ? "scaleY(1.02)" : "scaleY(1)",
                    transformOrigin: "bottom",
                  }}
                />

                {/* X-Axis Label */}
                <div className="absolute -bottom-8 left-1/2 -translate-x-1/2 w-full text-center">
                  <span className={`block truncate text-[11px] font-medium transition-colors ${isHovered ? "text-[#0066cc]" : "text-[#7a7a7a]"}`}>
                    {item.name}
                  </span>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
};

