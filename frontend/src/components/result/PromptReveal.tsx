import styles from "./PromptReveal.module.css";

interface PromptRevealProps {
  prompt: string;
}

export function PromptReveal({ prompt }: PromptRevealProps) {
  return <p className={styles.reveal}>"{prompt}"</p>;
}
