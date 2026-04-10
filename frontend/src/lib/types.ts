/**
 * TypeScript interfaces for the SQL Practice Platform.
 */

export type Difficulty = "Easy" | "Medium" | "Hard";
export type Verdict = "correct" | "partial" | "incorrect";

export interface QuestionSummary {
  id: number;
  title: string;
  difficulty: Difficulty;
  tags: string[];
  tables_used: string[];
}

export interface Question extends QuestionSummary {
  problem_statement: string;
  hint: string;
  explanation: string;
  solution_sql: string;
  pyspark_equivalent: string;
  expected_output_columns: string[];
  expected_row_count: number;
  requires_order: boolean;
}

export interface QuestionListResponse {
  questions: QuestionSummary[];
  total: number;
  tags: string[];
}

export interface ExecuteResponse {
  columns: string[];
  rows: (string | number | boolean | null)[][];
  row_count: number;
  truncated: boolean;
}

export interface ValidateResponse {
  verdict: Verdict;
  feedback: string[];
  user_columns: string[];
  user_rows: (string | number | boolean | null)[][];
  user_row_count: number;
  expected_columns: string[];
  expected_rows: (string | number | boolean | null)[][];
  expected_row_count: number;
}

export interface TableInfo {
  name: string;
  row_count: number;
  column_count: number;
}

export interface TableSchema {
  column_name: string;
  data_type: string;
  is_nullable: string;
}

export interface TableDetail {
  name: string;
  row_count: number;
  schema_info: TableSchema[];
  preview_columns: string[];
  preview_rows: (string | number | boolean | null)[][];
}

export interface ProgressSummary {
  total_attempted: number;
  total_solved: number;
  total_bookmarked: number;
  verdict_breakdown: { correct: number; partial: number; incorrect: number };
  questions: QuestionProgress[];
}

export interface QuestionProgress {
  question_id: number;
  total_attempts: number;
  best_verdict: string;
  is_solved: boolean;
  is_bookmarked: boolean;
  notes: string | null;
  last_attempted_at: string | null;
}

export interface SolutionResponse {
  question_id: number;
  solution_sql: string;
  pyspark_equivalent: string;
  explanation: string;
}
