import styles from "./Toast.module.css";

type ToastVariant = "error" | "info";

interface ToastProps {
  message: string;
  variant?: ToastVariant;
  onDismiss?: () => void;
}

export function Toast({ message, variant = "error", onDismiss }: ToastProps) {
  return (
    <div className={[styles.toast, styles[variant]].join(" ")} role="alert">
      <span className={styles.message}>{message}</span>
      {onDismiss && (
        <button className={styles.dismiss} onClick={onDismiss} aria-label="Dismiss">
          ×
        </button>
      )}
    </div>
  );
}
