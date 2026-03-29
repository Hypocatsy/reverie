import { useRef, useEffect } from "react";
import { useDream } from "./hooks/useDream";
import { InputPanel } from "./components/input/InputPanel";
import { LoadingSection } from "./components/loading/LoadingSection";
import { PlayerView } from "./components/player/PlayerView";
import { FloatingParticles } from "./components/common/FloatingParticles";
import styles from "./App.module.css";

export default function App() {
  const dream = useDream();
  const containerRef = useRef<HTMLDivElement>(null);

  const isDreaming = dream.status === "dreaming";
  const isSuccess = dream.status === "success";
  const isError = dream.status === "error";

  function scrollTo(index: number) {
    containerRef.current?.scrollTo({
      top: index * window.innerHeight,
      behavior: "smooth",
    });
  }

  useEffect(() => {
    if (isDreaming) scrollTo(1);
    if (isSuccess) scrollTo(1);
    if (isError) scrollTo(0);
  }, [dream.status]);

  function handleReset() {
    dream.reset();
    scrollTo(0);
  }

  return (
    <>
      <FloatingParticles />
      <div className={styles.container} ref={containerRef}>

        {/* Section 1 — Entry (always) */}
        <section className={styles.section}>
          <div className={styles.inner}>
            <InputPanel
              onSubmit={dream.dream}
              isLoading={isDreaming}
              error={isError ? dream.error : null}
            />
          </div>
        </section>

        {/* Section 2 — Loading (only while dreaming, unmounts on completion) */}
        {isDreaming && (
          <section className={styles.section}>
            <div className={styles.inner}>
              <LoadingSection stage={dream.stage} />
            </div>
          </section>
        )}

        {/* Section 3 — Player (only on success) */}
        {isSuccess && dream.result && (
          <section className={styles.section}>
            <div className={styles.inner}>
              <PlayerView result={dream.result} onReset={handleReset} />
            </div>
          </section>
        )}

      </div>
    </>
  );
}
