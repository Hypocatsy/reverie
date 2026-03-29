import type { TextareaHTMLAttributes } from "react";
import styles from "./Textarea.module.css";

interface TextareaProps extends TextareaHTMLAttributes<HTMLTextAreaElement> {
  label?: string;
}

export function Textarea({ label, id, ...props }: TextareaProps) {
  return (
    <div className={styles.wrapper}>
      {label && <label htmlFor={id} className={styles.label}>{label}</label>}
      <textarea id={id} className={styles.textarea} {...props} />
    </div>
  );
}
