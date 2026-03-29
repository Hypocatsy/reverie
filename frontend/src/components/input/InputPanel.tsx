import { useState } from "react";
import styles from "./InputPanel.module.css";

interface InputPanelProps {
  onSubmit: (url: string) => void;
  isLoading: boolean;
  error: string | null;
}

export function InputPanel({ onSubmit, isLoading, error }: InputPanelProps) {
  const [url, setUrl] = useState("");

  function handleSubmit() {
    const trimmed = url.trim();
    if (!trimmed) return;
    onSubmit(trimmed);
  }

  function handleKeyDown(e: React.KeyboardEvent<HTMLInputElement>) {
    if (e.key === "Enter") {
      handleSubmit();
    }
  }

  return (
    <div className={styles.wrapper}>
      <h1 className={styles.wordmark}>reverie</h1>
      <p className={styles.tagline}>what does this song look like?</p>

      <div className={styles.card}>
        <img src="/cat.png" className={styles.cat} alt="" />
        <label className={styles.label}>Spotify track link</label>
        <input
          className={styles.input}
          type="url"
          placeholder="Paste a Spotify link"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          onKeyDown={handleKeyDown}
          disabled={isLoading}
        />
        {error && <p className={styles.error}>{error}</p>}
      </div>

      <button
        className={styles.button}
        type="button"
        onClick={handleSubmit}
        disabled={isLoading}
      >
        ✦ Dream it
      </button>
    </div>
  );
}
