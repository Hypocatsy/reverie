import { TrackInfo } from "./TrackInfo";
import { ProgressBar } from "./ProgressBar";
import { PlaybackControls } from "./PlaybackControls";
import { PromptReveal } from "../result/PromptReveal";
import { downloadCard } from "../../utils/downloadCard";
import type { DreamResult } from "../../hooks/useDream";
import styles from "./PlayerView.module.css";

interface PlayerViewProps {
  result: DreamResult;
  onReset: () => void;
}

export function PlayerView({ result, onReset }: PlayerViewProps) {
  return (
    <div className={styles.view}>
      {/* Album art */}
      <div className={styles.albumArtWrapper}>
        <img
          src={result.image_url}
          alt={`${result.song_title} by ${result.artist}`}
          className={styles.albumArt}
        />
        <div className={styles.albumOverlay}>
          <div className={styles.overlayTitle}>{result.song_title}</div>
          <div className={styles.overlayArtist}>{result.artist}</div>
        </div>
      </div>

      {/* Track info */}
      <TrackInfo
        songTitle={result.song_title}
        artist={result.artist}
      />

      {/* Progress bar */}
      <ProgressBar />

      {/* Playback controls */}
      <PlaybackControls />

      {/* Prompt reveal */}
      <PromptReveal prompt={result.visual_prompt} />

      {/* Action buttons */}
      <div className={styles.actions}>
        <button
          className={styles.actionBtn}
          type="button"
          onClick={() => downloadCard(result.image_url, result.song_title, result.artist)}
        >
          Download card
        </button>
        <button className={styles.actionBtn} type="button" onClick={onReset}>
          Try another song
        </button>
      </div>
    </div>
  );
}
