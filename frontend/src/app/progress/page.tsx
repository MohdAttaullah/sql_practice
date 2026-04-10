"use client";

import { useEffect, useState } from "react";
import { getProgress, getQuestions } from "@/lib/api";
import type { ProgressSummary, QuestionSummary } from "@/lib/types";
import Link from "next/link";
import { BarChart3, CheckCircle, XCircle, AlertTriangle, Target } from "lucide-react";

export default function ProgressPage() {
  const [progress, setProgress] = useState<ProgressSummary | null>(null);
  const [questions, setQuestions] = useState<QuestionSummary[]>([]);
  const [loading, setLoading] = useState(true);
  const [filterVerdict, setFilterVerdict] = useState("");

  useEffect(() => {
    Promise.all([
      getProgress().catch(() => null),
      getQuestions().catch(() => ({ questions: [], total: 0, tags: [] })),
    ]).then(([p, q]) => {
      setProgress(p);
      setQuestions(q.questions);
      setLoading(false);
    });
  }, []);

  if (loading) return <div style={{ display: "flex", justifyContent: "center", paddingTop: "100px" }}><div className="spinner" /></div>;

  const totalQ = questions.length || 53;
  const solved = progress?.total_solved || 0;
  const attempted = progress?.total_attempted || 0;
  const vb = progress?.verdict_breakdown || { correct: 0, partial: 0, incorrect: 0 };

  // Build per-question progress map
  const progMap = new Map<number, { best_verdict: string; total_attempts: number; is_bookmarked: boolean }>();
  progress?.questions?.forEach((p) => progMap.set(p.question_id, p));

  // Build tag and difficulty stats
  const tagStats = new Map<string, { solved: number; total: number }>();
  const diffStats = new Map<string, { solved: number; total: number }>();

  questions.forEach((q) => {
    const p = progMap.get(q.id);
    const isSolved = p?.best_verdict === "correct";

    // difficulty
    const d = diffStats.get(q.difficulty) || { solved: 0, total: 0 };
    d.total++;
    if (isSolved) d.solved++;
    diffStats.set(q.difficulty, d);

    // tags
    q.tags.filter(t => t !== "PySpark SQL").forEach((t) => {
      const ts = tagStats.get(t) || { solved: 0, total: 0 };
      ts.total++;
      if (isSolved) ts.solved++;
      tagStats.set(t, ts);
    });
  });

  // Filter question list
  let filteredQuestions = questions;
  if (filterVerdict === "solved") filteredQuestions = questions.filter((q) => progMap.get(q.id)?.best_verdict === "correct");
  else if (filterVerdict === "attempted") filteredQuestions = questions.filter((q) => progMap.has(q.id) && progMap.get(q.id)!.best_verdict !== "correct");
  else if (filterVerdict === "unattempted") filteredQuestions = questions.filter((q) => !progMap.has(q.id));
  else if (filterVerdict === "bookmarked") filteredQuestions = questions.filter((q) => progMap.get(q.id)?.is_bookmarked);

  return (
    <div className="animate-in">
      <div className="section-header">
        <h1 className="section-title">Progress Tracker</h1>
      </div>

      {/* Overview stats */}
      <div className="stats-grid" style={{ marginBottom: "32px" }}>
        <div className="stat-card">
          <div className="stat-label">Solved</div>
          <div className="stat-value">{solved}/{totalQ}</div>
          <div className="progress-bar-track">
            <div className="progress-bar-fill" style={{ width: `${Math.round((solved / totalQ) * 100)}%` }} />
          </div>
        </div>
        <div className="stat-card" style={{ borderColor: "rgba(34,197,94,0.3)" }}>
          <CheckCircle size={18} style={{ color: "var(--success)" }} />
          <div className="stat-label">Correct</div>
          <div style={{ fontSize: "28px", fontWeight: 700, color: "var(--success)" }}>{vb.correct}</div>
        </div>
        <div className="stat-card" style={{ borderColor: "rgba(245,158,11,0.3)" }}>
          <AlertTriangle size={18} style={{ color: "var(--warning)" }} />
          <div className="stat-label">Partial</div>
          <div style={{ fontSize: "28px", fontWeight: 700, color: "var(--warning)" }}>{vb.partial}</div>
        </div>
        <div className="stat-card" style={{ borderColor: "rgba(239,68,68,0.3)" }}>
          <XCircle size={18} style={{ color: "var(--error)" }} />
          <div className="stat-label">Incorrect</div>
          <div style={{ fontSize: "28px", fontWeight: 700, color: "var(--error)" }}>{vb.incorrect}</div>
        </div>
      </div>

      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "24px", marginBottom: "32px" }}>
        {/* Difficulty breakdown */}
        <div className="card">
          <h3 style={{ fontSize: "16px", fontWeight: 600, marginBottom: "16px" }}>By Difficulty</h3>
          {["Easy", "Medium", "Hard"].map((d) => {
            const s = diffStats.get(d) || { solved: 0, total: 0 };
            const pct = s.total > 0 ? Math.round((s.solved / s.total) * 100) : 0;
            return (
              <div key={d} style={{ marginBottom: "14px" }}>
                <div style={{ display: "flex", justifyContent: "space-between", marginBottom: "6px", fontSize: "14px" }}>
                  <span className={`badge badge-${d.toLowerCase()}`}>{d}</span>
                  <span style={{ color: "var(--text-muted)" }}>{s.solved}/{s.total} ({pct}%)</span>
                </div>
                <div className="progress-bar-track">
                  <div className="progress-bar-fill" style={{ width: `${pct}%` }} />
                </div>
              </div>
            );
          })}
        </div>

        {/* Tag breakdown */}
        <div className="card" style={{ maxHeight: "300px", overflow: "auto" }}>
          <h3 style={{ fontSize: "16px", fontWeight: 600, marginBottom: "16px" }}>By Topic</h3>
          {Array.from(tagStats.entries()).sort((a, b) => b[1].total - a[1].total).map(([tag, s]) => {
            const pct = s.total > 0 ? Math.round((s.solved / s.total) * 100) : 0;
            return (
              <div key={tag} style={{ marginBottom: "12px" }}>
                <div style={{ display: "flex", justifyContent: "space-between", marginBottom: "4px", fontSize: "13px" }}>
                  <span>{tag}</span>
                  <span style={{ color: "var(--text-muted)" }}>{s.solved}/{s.total}</span>
                </div>
                <div className="progress-bar-track" style={{ height: "6px" }}>
                  <div className="progress-bar-fill" style={{ width: `${pct}%` }} />
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Question list with status */}
      <h3 style={{ fontSize: "18px", fontWeight: 700, marginBottom: "16px" }}>All Questions</h3>
      <div className="filter-bar">
        {["", "solved", "attempted", "unattempted", "bookmarked"].map((v) => (
          <button
            key={v}
            className={`tab ${filterVerdict === v ? "active" : ""}`}
            onClick={() => setFilterVerdict(v)}
            style={{ border: "none", background: "none", cursor: "pointer" }}
          >
            {v || "All"} {v === "" ? `(${totalQ})` : ""}
          </button>
        ))}
      </div>

      <div className="questions-grid">
        {filteredQuestions.map((q) => {
          const p = progMap.get(q.id);
          return (
            <Link key={q.id} href={`/questions/${q.id}`} className="question-card">
              <div className="qc-left">
                <div className="qc-id" style={{
                  background: p?.best_verdict === "correct" ? "rgba(34,197,94,0.12)" : p ? "rgba(245,158,11,0.12)" : undefined,
                  color: p?.best_verdict === "correct" ? "var(--success)" : p ? "var(--warning)" : "var(--text-muted)",
                }}>
                  {p?.best_verdict === "correct" ? "✓" : q.id}
                </div>
                <div>
                  <div className="qc-title">{q.title}</div>
                  <div style={{ fontSize: "12px", color: "var(--text-muted)", marginTop: "2px" }}>
                    {p ? `${p.total_attempts} attempt${p.total_attempts > 1 ? "s" : ""} • ${p.best_verdict}` : "Not attempted"}
                  </div>
                </div>
              </div>
              <span className={`badge badge-${q.difficulty.toLowerCase()}`}>{q.difficulty}</span>
            </Link>
          );
        })}
      </div>
    </div>
  );
}
