import type { DreamStage } from "../../hooks/useDream";
import styles from "./LoadingSection.module.css";

const STAGE_TEXT: Record<DreamStage, string> = {
  prompt: "Imagining the scene",
  image: "Painting the dream",
};

interface LoadingSectionProps {
  stage: DreamStage | null;
}

export function LoadingSection({ stage }: LoadingSectionProps) {
  return (
    <div className={styles.container}>
      <img src="/cat.png" className={styles.cat} alt="" />
      <p key={stage} className={styles.stageText}>
        {stage ? STAGE_TEXT[stage] : ""}
        <span className={styles.dots}>
          <span>.</span><span>.</span><span>.</span>
        </span>
      </p>
    </div>
  );
}
