import styles from "./ProgressBar.module.css";

export function ProgressBar() {
  // Static decorative progress bar — no audio functionality
  const progressPercent = 54; // ~2:14 of a ~4:10 track

  return (
    <div className={styles.wrapper}>
      <span className={styles.time}>2:14</span>
      <div className={styles.track} role="presentation">
        <div className={styles.fill} style={{ width: `${progressPercent}%` }}>
          <div className={styles.handle} />
        </div>
      </div>
      <span className={styles.time}>-1:45</span>
    </div>
  );
}
