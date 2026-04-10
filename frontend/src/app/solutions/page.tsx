"use client";

import { useEffect, useState } from "react";
import { getQuestions, getSolution } from "@/lib/api";
import type { QuestionSummary, SolutionResponse } from "@/lib/types";
import { Code2, ChevronDown, ChevronUp } from "lucide-react";

export default function Solutions() {
  const [questions, setQuestions] = useState<QuestionSummary[]>([]);
  const [solutions, setSolutions] = useState<Record<number, SolutionResponse>>({});
  const [expanded, setExpanded] = useState<number | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getQuestions().then((res) => setQuestions(res.questions)).catch(() => {}).finally(() => setLoading(false));
  }, []);

  const toggleSolution = async (id: number) => {
    if (expanded === id) { setExpanded(null); return; }
    if (!solutions[id]) {
      const sol = await getSolution(id);
      setSolutions((prev) => ({ ...prev, [id]: sol }));
    }
    setExpanded(id);
  };

  if (loading) return <div style={{ display: "flex", justifyContent: "center", paddingTop: "100px" }}><div className="spinner" /></div>;

  return (
    <div className="animate-in">
      <div className="section-header">
        <h1 className="section-title">Solutions & PySpark Reference</h1>
      </div>
      <p style={{ color: "var(--text-secondary)", marginBottom: "24px", fontSize: "15px" }}>
        Browse SQL solutions and their PySpark DataFrame API equivalents for all questions.
      </p>

      <div style={{ display: "flex", flexDirection: "column", gap: "8px" }}>
        {questions.map((q) => (
          <div key={q.id} style={{ borderRadius: "10px", overflow: "hidden", border: "1px solid var(--border)" }}>
            <div
              className="collapsible-header"
              onClick={() => toggleSolution(q.id)}
              style={{ borderRadius: expanded === q.id ? "10px 10px 0 0" : "10px" }}
            >
              <div style={{ display: "flex", alignItems: "center", gap: "12px" }}>
                <span style={{ color: "var(--text-muted)", fontSize: "13px", width: "30px" }}>#{q.id}</span>
                <span>{q.title}</span>
                <span className={`badge badge-${q.difficulty.toLowerCase()}`}>{q.difficulty}</span>
              </div>
              {expanded === q.id ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
            </div>
            {expanded === q.id && solutions[q.id] && (
              <div className="collapsible-content" style={{ borderRadius: "0 0 10px 10px" }}>
                <h4 style={{ fontSize: "13px", color: "var(--text-muted)", marginBottom: "8px", textTransform: "uppercase", letterSpacing: "0.05em" }}>SQL Solution</h4>
                <pre style={{ fontFamily: "'JetBrains Mono', monospace", fontSize: "13px", whiteSpace: "pre-wrap", color: "var(--accent-hover)", marginBottom: "16px", padding: "12px", background: "var(--bg-primary)", borderRadius: "6px" }}>
                  {solutions[q.id].solution_sql}
                </pre>
                <h4 style={{ fontSize: "13px", color: "var(--text-muted)", marginBottom: "8px", textTransform: "uppercase", letterSpacing: "0.05em" }}>Explanation</h4>
                <p style={{ marginBottom: "16px", fontSize: "14px", color: "var(--text-secondary)" }}>{solutions[q.id].explanation}</p>
                <h4 style={{ fontSize: "13px", color: "var(--text-muted)", marginBottom: "8px", textTransform: "uppercase", letterSpacing: "0.05em", display: "flex", alignItems: "center", gap: "6px" }}>
                  <Code2 size={14} color="#c4b5fd" /> PySpark DataFrame API
                </h4>
                <div className="pyspark-block">{solutions[q.id].pyspark_equivalent}</div>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
