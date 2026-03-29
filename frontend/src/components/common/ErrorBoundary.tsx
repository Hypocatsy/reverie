import { Component, type ReactNode } from "react";

interface ErrorBoundaryProps {
  children: ReactNode;
}

interface ErrorBoundaryState {
  hasError: boolean;
}

export class ErrorBoundary extends Component<ErrorBoundaryProps, ErrorBoundaryState> {
  constructor(props: ErrorBoundaryProps) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError(): ErrorBoundaryState {
    return { hasError: true };
  }

  render() {
    if (this.state.hasError) {
      return (
        <div
          style={{
            height: "100vh",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            backgroundColor: "var(--color-bg)",
          }}
        >
          <p
            style={{
              fontStyle: "italic",
              color: "var(--color-text-muted)",
              textAlign: "center",
              padding: "0 1.5rem",
            }}
          >
            Something went wrong. Refresh to try again.
          </p>
        </div>
      );
    }

    return this.props.children;
  }
}
