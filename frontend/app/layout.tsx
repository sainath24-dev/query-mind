import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "QueryMind — Natural Language Database Assistant",
  description: "Reverent, conversational natural language to PostgreSQL interface.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="bg-[#f5f5f7] text-[#1d1d1f] min-h-screen antialiased flex flex-col font-sans">
        {children}
      </body>
    </html>
  );
}
