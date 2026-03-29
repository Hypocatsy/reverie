import styles from "./PlaybackControls.module.css";

export function PlaybackControls() {
  return (
    <div className={styles.controls} aria-label="Playback controls (decorative)">
      {/* Shuffle */}
      <button className={styles.iconBtn} type="button" aria-label="Shuffle" title="Just vibes, no playback">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
          <polyline points="16 3 21 3 21 8" />
          <line x1="4" y1="20" x2="21" y2="3" />
          <polyline points="21 16 21 21 16 21" />
          <line x1="15" y1="15" x2="21" y2="21" />
        </svg>
      </button>

      {/* Previous */}
      <button className={styles.iconBtn} type="button" aria-label="Previous" title="Just vibes, no playback">
        <svg width="22" height="22" viewBox="0 0 24 24" fill="currentColor">
          <polygon points="19 20 9 12 19 4 19 20" />
          <line x1="5" y1="19" x2="5" y2="5" stroke="currentColor" strokeWidth="2" strokeLinecap="round" fill="none" />
        </svg>
      </button>

      {/* Play/Pause — large filled circle */}
      <button className={styles.playBtn} type="button" aria-label="Play/Pause" title="Just vibes, no playback">
        <svg width="26" height="26" viewBox="0 0 24 24" fill="white">
          <polygon points="5 3 19 12 5 21 5 3" />
        </svg>
      </button>

      {/* Next */}
      <button className={styles.iconBtn} type="button" aria-label="Next" title="Just vibes, no playback">
        <svg width="22" height="22" viewBox="0 0 24 24" fill="currentColor">
          <polygon points="5 4 15 12 5 20 5 4" />
          <line x1="19" y1="5" x2="19" y2="19" stroke="currentColor" strokeWidth="2" strokeLinecap="round" fill="none" />
        </svg>
      </button>

      {/* Repeat */}
      <button className={styles.iconBtn} type="button" aria-label="Repeat" title="Just vibes, no playback">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
          <polyline points="17 1 21 5 17 9" />
          <path d="M3 11V9a4 4 0 0 1 4-4h14" />
          <polyline points="7 23 3 19 7 15" />
          <path d="M21 13v2a4 4 0 0 1-4 4H3" />
        </svg>
      </button>
    </div>
  );
}
