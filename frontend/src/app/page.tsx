"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { getProgress, getQuestions, getRecentAttempts } from "@/lib/api";
import type { ProgressSummary, QuestionSummary } from "@/lib/types";
import {
  Target, TrendingUp, Bookmark, Clock, ArrowRight, Zap,
} from "lucide-react";

export default function Dashboard() {
  const [progress, setProgress] = useState<ProgressSummary | null>(null);
  const [questions, setQuestions] = useState<QuestionSummary[]>([]);
  const [recent, setRecent] = useState<{ question_id: number; verdict: string; attempted_at: string }[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([
      getProgress().catch(() => null),
      getQuestions().catch(() => ({ questions: [], total: 0, tags: [] })),
      getRecentAttempts().catch(() => []),
    ]).then(([p, q, r]) => {
      setProgress(p);
      setQuestions(q.questions);
      setRecent(r);
      setLoading(false);
    });
  }, []);

  if (loading) return <div style={{ display: "flex", justifyContent: "center", paddingTop: "100px" }}><div className="spinner" /></div>;

  const totalQ = questions.length || 53;
  const solved = progress?.total_solved || 0;
  const attempted = progress?.total_attempted || 0;
  const pct = totalQ > 0 ? Math.round((solved / totalQ) * 100) : 0;

  return (
    <div className="animate-in">
      {/* Hero header */}
      <div style={{ marginBottom: "32px" }}>
        <h1 style={{ fontSize: "32px", fontWeight: 800, marginBottom: "8px" }}>
          Welcome to <span style={{ background: "linear-gradient(135deg, #6366f1, #a855f7)", WebkitBackgroundClip: "text", WebkitTextFillColor: "transparent" }}>SQL Practice Lab</span>
        </h1>
        <p style={{ color: "var(--text-secondary)", fontSize: "16px" }}>
          Master Data Engineering SQL — PySpark / Spark SQL interview preparation
        </p>
      </div>

      {/* Stats */}
      <div className="stats-grid" style={{ marginBottom: "32px" }}>
        <div className="stat-card">
          <div className="stat-label">Solved</div>
          <div className="stat-value">{solved}/{totalQ}</div>
          <div className="progress-bar-track">
            <div className="progress-bar-fill" style={{ width: `${pct}%` }} />
          </div>
        </div>
        <div className="stat-card">
          <Target size={20} style={{ color: "var(--accent)" }} />
          <div className="stat-label">Attempted</div>
          <div className="stat-value">{attempted}</div>
        </div>
        <div className="stat-card">
          <TrendingUp size={20} style={{ color: "var(--success)" }} />
          <div className="stat-label">Accuracy</div>
          <div className="stat-value">{attempted > 0 ? Math.round((solved / attempted) * 100) : 0}%</div>
        </div>
        <div className="stat-card">
          <Bookmark size={20} style={{ color: "var(--warning)" }} />
          <div className="stat-label">Bookmarked</div>
          <div className="stat-value">{progress?.total_bookmarked || 0}</div>
        </div>
      </div>

      {/* Quick start + Recent */}
      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "24px" }}>
        {/* Quick Start */}
        <div className="card">
          <h2 style={{ fontSize: "18px", fontWeight: 700, marginBottom: "16px", display: "flex", alignItems: "center", gap: "8px" }}>
            <Zap size={20} style={{ color: "var(--warning)" }} /> Quick Start
          </h2>
          <div style={{ display: "flex", flexDirection: "column", gap: "10px" }}>
            {questions.slice(0, 5).map((q) => (
              <Link key={q.id} href={`/questions/${q.id}`} className="question-card" style={{ padding: "12px 16px" }}>
                <div className="qc-left">
                  <div className="qc-id">{q.id}</div>
                  <div>
                    <div className="qc-title" style={{ fontSize: "14px" }}>{q.title}</div>
                  </div>
                </div>
                <div className="qc-right">
                  <span className={`badge badge-${q.difficulty.toLowerCase()}`}>{q.difficulty}</span>
                  <ArrowRight size={16} style={{ color: "var(--text-muted)" }} />
                </div>
              </Link>
            ))}
            <Link href="/questions" className="btn btn-secondary" style={{ justifyContent: "center", marginTop: "8px" }}>
              View All {totalQ} Questions <ArrowRight size={16} />
            </Link>
          </div>
        </div>

        {/* Recent Activity */}
        <div className="card">
          <h2 style={{ fontSize: "18px", fontWeight: 700, marginBottom: "16px", display: "flex", alignItems: "center", gap: "8px" }}>
            <Clock size={20} style={{ color: "var(--accent)" }} /> Recent Activity
          </h2>
          {recent.length === 0 ? (
            <div style={{ color: "var(--text-muted)", padding: "32px", textAlign: "center" }}>
              No attempts yet. Start practicing!
            </div>
          ) : (
            <div style={{ display: "flex", flexDirection: "column", gap: "10px" }}>
              {recent.slice(0, 8).map((r) => (
                <Link key={r.id} href={`/questions/${r.question_id}`} style={{
                  display: "flex", justifyContent: "space-between", alignItems: "center",
                  padding: "10px 14px", borderRadius: "8px", background: "var(--bg-elevated)",
                  textDecoration: "none", color: "inherit", transition: "background 0.15s",
                }}>
                  <span style={{ fontSize: "14px" }}>Question #{r.question_id}</span>
                  <div style={{ display: "flex", alignItems: "center", gap: "10px" }}>
                    <span className={`badge ${r.verdict === "correct" ? "badge-easy" : r.verdict === "partial" ? "badge-medium" : "badge-hard"}`}>
                      {r.verdict}
                    </span>
                    <span style={{ fontSize: "12px", color: "var(--text-muted)" }}>
                      {new Date(r.attempted_at).toLocaleDateString()}
                    </span>
                  </div>
                </Link>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
