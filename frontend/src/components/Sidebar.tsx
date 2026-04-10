"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  LayoutDashboard,
  BookOpen,
  Database,
  CheckCircle,
  BarChart3,
  Code2,
} from "lucide-react";

const navItems = [
  { href: "/", label: "Dashboard", icon: LayoutDashboard },
  { href: "/questions", label: "Question Bank", icon: BookOpen },
  { href: "/datasets", label: "Dataset Explorer", icon: Database },
  { href: "/solutions", label: "Solutions", icon: Code2 },
  { href: "/progress", label: "Progress", icon: BarChart3 },
];

export default function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="sidebar">
      <div className="sidebar-logo">
        <div className="logo-icon">⚡</div>
        <h1>SQL Practice Lab</h1>
      </div>
      <nav className="sidebar-nav">
        {navItems.map((item) => {
          const isActive =
            item.href === "/"
              ? pathname === "/"
              : pathname.startsWith(item.href);
          const Icon = item.icon;
          return (
            <Link
              key={item.href}
              href={item.href}
              className={`nav-link ${isActive ? "active" : ""}`}
            >
              <Icon />
              {item.label}
            </Link>
          );
        })}
      </nav>
      <div style={{
        padding: "16px 20px",
        borderTop: "1px solid var(--border)",
        fontSize: "12px",
        color: "var(--text-muted)",
      }}>
        <div style={{ display: "flex", alignItems: "center", gap: "6px" }}>
          <CheckCircle size={14} />
          PySpark SQL Focus
        </div>
        <div style={{ marginTop: "4px" }}>53 Questions • 12 Datasets</div>
      </div>
    </aside>
  );
}
