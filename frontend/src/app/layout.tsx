import type { Metadata } from "next";
import "./globals.css";
import Sidebar from "@/components/Sidebar";

export const metadata: Metadata = {
  title: "SQL Practice Lab — Data Engineer Interview Prep",
  description: "Interactive SQL practice platform for Data Engineers preparing for PySpark and Spark SQL interviews. 50+ real-world questions with instant validation.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <head>
        <link
          href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap"
          rel="stylesheet"
        />
      </head>
      <body>
        <Sidebar />
        <main className="main-content">{children}</main>
      </body>
    </html>
  );
}
