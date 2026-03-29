import type { ButtonHTMLAttributes } from "react";
import styles from "./Button.module.css";

type ButtonVariant = "primary" | "ghost";

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: ButtonVariant;
  loading?: boolean;
}

export function Button({
  variant = "primary",
  loading = false,
  children,
  disabled,
  className,
  ...props
}: ButtonProps) {
  return (
    <button
      className={[styles.button, styles[variant], className].filter(Boolean).join(" ")}
      disabled={disabled || loading}
      {...props}
    >
      {loading ? <span className={styles.spinner} /> : children}
    </button>
  );
}
