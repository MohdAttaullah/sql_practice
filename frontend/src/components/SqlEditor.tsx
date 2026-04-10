"use client";

import { useCallback } from "react";
import CodeMirror from "@uiw/react-codemirror";
import { sql } from "@codemirror/lang-sql";
import { oneDark } from "@codemirror/theme-one-dark";

interface Props {
  value: string;
  onChange: (val: string) => void;
}

export default function SqlEditor({ value, onChange }: Props) {
  const handleChange = useCallback((val: string) => {
    onChange(val);
  }, [onChange]);

  return (
    <CodeMirror
      value={value}
      height="250px"
      theme={oneDark}
      extensions={[sql()]}
      onChange={handleChange}
      placeholder="-- Write your SQL query here..."
      basicSetup={{
        lineNumbers: true,
        highlightActiveLine: true,
        bracketMatching: true,
        autocompletion: true,
        foldGutter: true,
      }}
    />
  );
}
