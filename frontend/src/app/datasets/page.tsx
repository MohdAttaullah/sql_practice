"use client";

import { useEffect, useState } from "react";
import { getDatasets, getDatasetDetail } from "@/lib/api";
import type { TableInfo, TableDetail } from "@/lib/types";
import { Database, Table, ChevronRight, X, Rows3 } from "lucide-react";

export default function DatasetExplorer() {
  const [tables, setTables] = useState<TableInfo[]>([]);
  const [selected, setSelected] = useState<TableDetail | null>(null);
  const [loading, setLoading] = useState(true);
  const [detailLoading, setDetailLoading] = useState(false);

  useEffect(() => {
    getDatasets().then(setTables).catch(() => {}).finally(() => setLoading(false));
  }, []);

  const loadDetail = async (name: string) => {
    setDetailLoading(true);
    try {
      const detail = await getDatasetDetail(name);
      setSelected(detail);
    } catch {}
    setDetailLoading(false);
  };

  if (loading) return <div style={{ display: "flex", justifyContent: "center", paddingTop: "100px" }}><div className="spinner" /></div>;

  return (
    <div className="animate-in">
      <div className="section-header">
        <h1 className="section-title">Dataset Explorer</h1>
        <div style={{ fontSize: "14px", color: "var(--text-muted)" }}>
          {tables.length} tables available
        </div>
      </div>

      <div style={{ display: "grid", gridTemplateColumns: selected ? "1fr 2fr" : "1fr", gap: "24px" }}>
        {/* Table list */}
        <div className="datasets-grid" style={{ gridTemplateColumns: "1fr" }}>
          {tables.map((t) => (
            <div
              key={t.name}
              className="card"
              onClick={() => loadDetail(t.name)}
              style={{
                cursor: "pointer",
                borderColor: selected?.name === t.name ? "var(--accent)" : undefined,
                background: selected?.name === t.name ? "rgba(99,102,241,0.04)" : undefined,
              }}
            >
              <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between" }}>
                <div style={{ display: "flex", alignItems: "center", gap: "12px" }}>
                  <div style={{
                    width: "40px", height: "40px", borderRadius: "8px",
                    background: "rgba(99,102,241,0.1)", display: "flex",
                    alignItems: "center", justifyContent: "center",
                  }}>
                    <Table size={18} style={{ color: "var(--accent)" }} />
                  </div>
                  <div>
                    <div style={{ fontWeight: 600, fontSize: "15px" }}>{t.name}</div>
                    <div style={{ fontSize: "13px", color: "var(--text-muted)" }}>
                      {t.column_count} columns • {t.row_count} rows
                    </div>
                  </div>
                </div>
                <ChevronRight size={18} style={{ color: "var(--text-muted)" }} />
              </div>
            </div>
          ))}
        </div>

        {/* Detail panel */}
        {selected && (
          <div className="card" style={{ position: "sticky", top: "32px", alignSelf: "start" }}>
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "20px" }}>
              <h2 style={{ fontSize: "20px", fontWeight: 700, display: "flex", alignItems: "center", gap: "10px" }}>
                <Database size={20} style={{ color: "var(--accent)" }} />
                {selected.name}
              </h2>
              <button onClick={() => setSelected(null)} style={{ background: "none", border: "none", cursor: "pointer", color: "var(--text-muted)" }}>
                <X size={18} />
              </button>
            </div>

            <div style={{ marginBottom: "20px", fontSize: "14px", color: "var(--text-muted)" }}>
              {selected.row_count} rows • {selected.schema_info.length} columns
            </div>

            {/* Schema */}
            <h3 style={{ fontSize: "15px", fontWeight: 600, marginBottom: "10px" }}>Schema</h3>
            <table className="schema-table" style={{ marginBottom: "24px" }}>
              <thead>
                <tr><th>Column</th><th>Type</th><th>Nullable</th></tr>
              </thead>
              <tbody>
                {selected.schema_info.map((col) => (
                  <tr key={col.column_name}>
                    <td style={{ fontWeight: 500 }}>{col.column_name}</td>
                    <td><span className="type-badge">{col.data_type}</span></td>
                    <td style={{ color: "var(--text-muted)" }}>{col.is_nullable}</td>
                  </tr>
                ))}
              </tbody>
            </table>

            {/* Preview */}
            <h3 style={{ fontSize: "15px", fontWeight: 600, marginBottom: "10px", display: "flex", alignItems: "center", gap: "8px" }}>
              <Rows3 size={16} /> Data Preview
            </h3>
            <div className="result-table-wrapper">
              <table className="result-table">
                <thead>
                  <tr>{selected.preview_columns.map((c) => <th key={c}>{c}</th>)}</tr>
                </thead>
                <tbody>
                  {selected.preview_rows.map((row, i) => (
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
          </div>
        )}
      </div>
    </div>
  );
}
