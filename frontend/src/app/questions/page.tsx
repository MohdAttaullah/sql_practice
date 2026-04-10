"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { getQuestions } from "@/lib/api";
import type { QuestionSummary } from "@/lib/types";
import { Search, Filter, ArrowRight, CheckCircle } from "lucide-react";

export default function QuestionBank() {
  const [questions, setQuestions] = useState<QuestionSummary[]>([]);
  const [allTags, setAllTags] = useState<string[]>([]);
  const [difficulty, setDifficulty] = useState("");
  const [tag, setTag] = useState("");
  const [search, setSearch] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const params = new URLSearchParams();
    if (difficulty) params.set("difficulty", difficulty);
    if (tag) params.set("tag", tag);
    if (search) params.set("search", search);

    setLoading(true);
    getQuestions(params.toString())
      .then((res) => {
        setQuestions(res.questions);
        if (allTags.length === 0) setAllTags(res.tags);
      })
      .catch(() => {})
      .finally(() => setLoading(false));
  }, [difficulty, tag, search]);

  return (
    <div className="animate-in">
      <div className="section-header">
        <h1 className="section-title">Question Bank</h1>
        <div style={{ fontSize: "14px", color: "var(--text-muted)" }}>
          {questions.length} questions
        </div>
      </div>

      {/* Filters */}
      <div className="filter-bar">
        <div style={{ position: "relative", flex: 1, maxWidth: "300px" }}>
          <Search size={16} style={{ position: "absolute", left: "12px", top: "50%", transform: "translateY(-50%)", color: "var(--text-muted)" }} />
          <input
            type="text"
            placeholder="Search questions..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            style={{ width: "100%", paddingLeft: "36px" }}
          />
        </div>
        <select value={difficulty} onChange={(e) => setDifficulty(e.target.value)}>
          <option value="">All Difficulties</option>
          <option value="Easy">Easy</option>
          <option value="Medium">Medium</option>
          <option value="Hard">Hard</option>
        </select>
        <select value={tag} onChange={(e) => setTag(e.target.value)}>
          <option value="">All Tags</option>
          {allTags.map((t) => (
            <option key={t} value={t}>{t}</option>
          ))}
        </select>
        {(difficulty || tag || search) && (
          <button className="btn btn-secondary" onClick={() => { setDifficulty(""); setTag(""); setSearch(""); }} style={{ padding: "8px 14px" }}>
            Clear
          </button>
        )}
      </div>

      {/* Question list */}
      {loading ? (
        <div style={{ display: "flex", justifyContent: "center", padding: "60px" }}>
          <div className="spinner" />
        </div>
      ) : (
        <div className="questions-grid">
          {questions.map((q) => (
            <Link key={q.id} href={`/questions/${q.id}`} className="question-card">
              <div className="qc-left">
                <div className="qc-id">{q.id}</div>
                <div>
                  <div className="qc-title">{q.title}</div>
                  <div className="qc-tags">
                    {q.tags.filter(t => t !== "PySpark SQL").slice(0, 4).map((t) => (
                      <span key={t} className="badge badge-tag">{t}</span>
                    ))}
                    {q.tables_used.length > 0 && (
                      <span className="badge badge-tag" style={{ color: "var(--accent)", borderColor: "var(--accent)", background: "rgba(99,102,241,0.06)" }}>
                        {q.tables_used.length} table{q.tables_used.length > 1 ? "s" : ""}
                      </span>
                    )}
                  </div>
                </div>
              </div>
              <div className="qc-right">
                <span className={`badge badge-${q.difficulty.toLowerCase()}`}>{q.difficulty}</span>
                <ArrowRight size={16} style={{ color: "var(--text-muted)" }} />
              </div>
            </Link>
          ))}
          {questions.length === 0 && (
            <div style={{ textAlign: "center", padding: "60px", color: "var(--text-muted)" }}>
              No questions match your filters.
            </div>
          )}
        </div>
      )}
    </div>
  );
}
