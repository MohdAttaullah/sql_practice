"use client";

import { useEffect, useState, useCallback } from "react";
import { useParams } from "next/navigation";
import dynamic from "next/dynamic";
import {
  getQuestion, executeSQL, validateSQL, getSolution,
  getQuestionProgress, toggleBookmark, saveNotes,
} from "@/lib/api";
import type { Question, ExecuteResponse, ValidateResponse, SolutionResponse, QuestionProgress } from "@/lib/types";
import {
  Play, CheckCircle, XCircle, AlertTriangle, Lightbulb,
  Code2, BookmarkPlus, Bookmark, ChevronDown, ChevronUp,
  Eye, ArrowLeft, ArrowRight, Loader2,
} from "lucide-react";
import Link from "next/link";

// Dynamic import for CodeMirror to avoid SSR issues
const CodeMirrorEditor = dynamic(() => import("@/components/SqlEditor"), { ssr: false });

export default function Workspace() {
  const params = useParams();
  const questionId = Number(params.id);

  const [question, setQuestion] = useState<Question | null>(null);
  const [sql, setSql] = useState("");
  const [execResult, setExecResult] = useState<ExecuteResponse | null>(null);
  const [validResult, setValidResult] = useState<ValidateResponse | null>(null);
  const [solution, setSolution] = useState<SolutionResponse | null>(null);
  const [progress, setProgress] = useState<QuestionProgress | null>(null);
  const [notes, setNotes] = useState("");
  const [showHint, setShowHint] = useState(false);
  const [showSolution, setShowSolution] = useState(false);
  const [showPySpark, setShowPySpark] = useState(false);
  const [showExpected, setShowExpected] = useState(false);
  const [running, setRunning] = useState(false);
  const [validating, setValidating] = useState(false);
  const [error, setError] = useState("");
  const [activeTab, setActiveTab] = useState<"output" | "expected">("output");

  useEffect(() => {
    if (!questionId) return;
    setExecResult(null);
    setValidResult(null);
    setSolution(null);
    setShowHint(false);
    setShowSolution(false);
    setShowPySpark(false);
    setError("");
    setSql("");

    getQuestion(questionId).then(setQuestion).catch(() => setError("Failed to load question"));
    getQuestionProgress(questionId).then((p) => {
      setProgress(p);
      setNotes(p.notes || "");
    }).catch(() => {});
  }, [questionId]);

  const handleRun = useCallback(async () => {
    if (!sql.trim()) return;
    setRunning(true);
    setError("");
    setValidResult(null);
    try {
      const res = await executeSQL(sql);
      setExecResult(res);
      setActiveTab("output");
    } catch (e: any) {
      setError(e.message);
      setExecResult(null);
    } finally {
      setRunning(false);
    }
  }, [sql]);

  const handleValidate = useCallback(async () => {
    if (!sql.trim() || !question) return;
    setValidating(true);
    setError("");
    try {
      const res = await validateSQL(question.id, sql);
      setValidResult(res);
      setExecResult({ columns: res.user_columns, rows: res.user_rows, row_count: res.user_row_count, truncated: false });
      setActiveTab("output");
      // Refresh progress
      getQuestionProgress(questionId).then(setProgress).catch(() => {});
    } catch (e: any) {
      setError(e.message);
    } finally {
      setValidating(false);
    }
  }, [sql, question, questionId]);

  const handleRevealSolution = async () => {
    if (!question) return;
    const sol = await getSolution(question.id);
    setSolution(sol);
    setShowSolution(true);
  };

  const handleBookmark = async () => {
    if (!progress) return;
    const newVal = !progress.is_bookmarked;
    await toggleBookmark(questionId, newVal);
    setProgress({ ...progress, is_bookmarked: newVal });
  };

  const handleSaveNotes = async () => {
    await saveNotes(questionId, notes);
  };

  if (error && !question) {
    return <div style={{ padding: "60px", textAlign: "center", color: "var(--error)" }}>{error}</div>;
  }

  if (!question) {
    return <div style={{ display: "flex", justifyContent: "center", paddingTop: "100px" }}><div className="spinner" /></div>;
  }

  return (
    <div className="animate-in">
      {/* Header */}
      <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: "20px" }}>
        <div style={{ display: "flex", alignItems: "center", gap: "16px" }}>
          <Link href="/questions" style={{ color: "var(--text-muted)", display: "flex" }}><ArrowLeft size={20} /></Link>
          <div>
            <div style={{ display: "flex", alignItems: "center", gap: "10px" }}>
              <span style={{ color: "var(--text-muted)", fontSize: "14px" }}>#{question.id}</span>
              <h1 style={{ fontSize: "22px", fontWeight: 700 }}>{question.title}</h1>
              <span className={`badge badge-${question.difficulty.toLowerCase()}`}>{question.difficulty}</span>
            </div>
            <div style={{ display: "flex", gap: "6px", marginTop: "6px" }}>
              {question.tags.filter(t => t !== "PySpark SQL").map((t) => (
                <span key={t} className="badge badge-tag">{t}</span>
              ))}
            </div>
          </div>
        </div>
        <div style={{ display: "flex", gap: "8px" }}>
          <button className="btn btn-secondary" onClick={handleBookmark} style={{ padding: "8px 12px" }}>
            {progress?.is_bookmarked ? <Bookmark size={18} fill="var(--warning)" color="var(--warning)" /> : <BookmarkPlus size={18} />}
          </button>
          {questionId > 1 && (
            <Link href={`/questions/${questionId - 1}`} className="btn btn-secondary" style={{ padding: "8px 12px" }}>
              <ArrowLeft size={16} /> Prev
            </Link>
          )}
          <Link href={`/questions/${questionId + 1}`} className="btn btn-secondary" style={{ padding: "8px 12px" }}>
            Next <ArrowRight size={16} />
          </Link>
        </div>
      </div>

      <div className="workspace">
        {/* Left: Problem + Editor */}
        <div className="workspace-panel">
          {/* Problem statement */}
          <div className="card">
            <h3 style={{ fontSize: "15px", fontWeight: 600, marginBottom: "10px", color: "var(--text-secondary)" }}>Problem</h3>
            <p style={{ fontSize: "15px", lineHeight: 1.7 }}>{question.problem_statement}</p>
            <div style={{ marginTop: "12px", fontSize: "13px", color: "var(--text-muted)" }}>
              <strong>Tables:</strong> {question.tables_used.join(", ")}
              {question.requires_order && <span style={{ marginLeft: "12px" }}>⚠️ Order matters</span>}
            </div>
          </div>

          {/* Hint */}
          <div>
            <div className="collapsible-header" onClick={() => setShowHint(!showHint)}>
              <span style={{ display: "flex", alignItems: "center", gap: "8px" }}>
                <Lightbulb size={16} color="var(--warning)" /> Hint
              </span>
              {showHint ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
            </div>
            {showHint && <div className="collapsible-content">{question.hint}</div>}
          </div>

          {/* SQL Editor */}
          <div>
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "8px" }}>
              <h3 style={{ fontSize: "15px", fontWeight: 600 }}>SQL Editor</h3>
              <div style={{ display: "flex", gap: "8px" }}>
                <button className="btn btn-primary" onClick={handleRun} disabled={running || !sql.trim()} style={{ padding: "8px 16px" }}>
                  {running ? <Loader2 size={16} className="spinner" /> : <Play size={16} />} Run
                </button>
                <button className="btn btn-success" onClick={handleValidate} disabled={validating || !sql.trim()} style={{ padding: "8px 16px" }}>
                  {validating ? <Loader2 size={16} className="spinner" /> : <CheckCircle size={16} />} Validate
                </button>
              </div>
            </div>
            <div className="editor-wrapper">
              <CodeMirrorEditor value={sql} onChange={setSql} />
            </div>
          </div>

          {/* Notes */}
          <div>
            <div className="collapsible-header" onClick={() => {}}>
              <span>📝 Notes</span>
            </div>
            <div style={{ marginTop: "8px" }}>
              <textarea className="notes-textarea" value={notes} onChange={(e) => setNotes(e.target.value)} placeholder="Write your notes here..." />
              <button className="btn btn-secondary" onClick={handleSaveNotes} style={{ marginTop: "8px", padding: "6px 14px", fontSize: "13px" }}>
                Save Notes
              </button>
            </div>
          </div>
        </div>

        {/* Right: Results + Solution */}
        <div className="workspace-panel">
          {/* Verdict banner */}
          {validResult && (
            <div className={`verdict-banner verdict-${validResult.verdict}`}>
              {validResult.verdict === "correct" && <CheckCircle size={20} />}
              {validResult.verdict === "partial" && <AlertTriangle size={20} />}
              {validResult.verdict === "incorrect" && <XCircle size={20} />}
              <div>
                <strong style={{ textTransform: "capitalize" }}>{validResult.verdict}!</strong>
                <div style={{ marginTop: "4px", fontSize: "13px", opacity: 0.9 }}>
                  {validResult.feedback.map((f, i) => <div key={i}>{f}</div>)}
                </div>
              </div>
            </div>
          )}

          {/* Error */}
          {error && (
            <div className="verdict-banner verdict-incorrect">
              <XCircle size={20} />
              <div><strong>Error</strong><div style={{ marginTop: "4px", fontSize: "13px" }}>{error}</div></div>
            </div>
          )}

          {/* Result tabs */}
          <div className="tabs">
            <button className={`tab ${activeTab === "output" ? "active" : ""}`} onClick={() => setActiveTab("output")}>
              Your Output {execResult && `(${execResult.row_count} rows)`}
            </button>
            <button className={`tab ${activeTab === "expected" ? "active" : ""}`} onClick={() => { setActiveTab("expected"); setShowExpected(true); }}>
              Expected Output
            </button>
          </div>

          {/* Result table */}
          {activeTab === "output" && execResult && (
            <div className="result-table-wrapper">
              <table className="result-table">
                <thead>
                  <tr>{execResult.columns.map((c) => <th key={c}>{c}</th>)}</tr>
                </thead>
                <tbody>
                  {execResult.rows.slice(0, 100).map((row, i) => (
                    <tr key={i}>
                      {row.map((val, j) => (
                        <td key={j} className={val === null ? "null-value" : ""}>
                          {val === null ? "NULL" : String(val)}
                        </td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>
              {execResult.row_count > 100 && (
                <div style={{ padding: "10px 14px", fontSize: "13px", color: "var(--text-muted)" }}>
                  Showing 100 of {execResult.row_count} rows
                </div>
              )}
            </div>
          )}

          {activeTab === "expected" && validResult && (
            <div className="result-table-wrapper">
              <table className="result-table">
                <thead>
                  <tr>{validResult.expected_columns.map((c) => <th key={c}>{c}</th>)}</tr>
                </thead>
                <tbody>
                  {validResult.expected_rows.slice(0, 100).map((row, i) => (
                    <tr key={i}>
                      {row.map((val, j) => (
                        <td key={j} className={val === null ? "null-value" : ""}>
                          {val === null ? "NULL" : String(val)}
                        </td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}

          {activeTab === "expected" && !validResult && (
            <div style={{ padding: "40px", textAlign: "center", color: "var(--text-muted)" }}>
              Run &quot;Validate&quot; first to see expected output
            </div>
          )}

          {!execResult && activeTab === "output" && (
            <div style={{ padding: "60px", textAlign: "center", color: "var(--text-muted)", background: "var(--bg-card)", borderRadius: "10px", border: "1px solid var(--border)" }}>
              <Play size={32} style={{ marginBottom: "12px", opacity: 0.5 }} />
              <div>Write your SQL and click Run to see results</div>
            </div>
          )}

          {/* Solution reveal */}
          <div>
            <div className="collapsible-header" onClick={() => showSolution ? setShowSolution(false) : handleRevealSolution()}>
              <span style={{ display: "flex", alignItems: "center", gap: "8px" }}>
                <Eye size={16} /> Solution SQL
              </span>
              {showSolution ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
            </div>
            {showSolution && solution && (
              <div className="collapsible-content">
                <pre style={{ fontFamily: "'JetBrains Mono', monospace", fontSize: "13px", whiteSpace: "pre-wrap", color: "var(--accent-hover)" }}>
                  {solution.solution_sql}
                </pre>
                <div style={{ marginTop: "12px", fontSize: "14px", color: "var(--text-secondary)" }}>
                  <strong>Explanation:</strong> {solution.explanation}
                </div>
              </div>
            )}
          </div>

          {/* PySpark equivalent */}
          <div>
            <div className="collapsible-header" onClick={() => { setShowPySpark(!showPySpark); if (!solution) handleRevealSolution(); }}>
              <span style={{ display: "flex", alignItems: "center", gap: "8px" }}>
                <Code2 size={16} color="#c4b5fd" /> PySpark Equivalent
              </span>
              {showPySpark ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
            </div>
            {showPySpark && solution && (
              <div className="pyspark-block">{solution.pyspark_equivalent}</div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
