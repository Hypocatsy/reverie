import styles from "./TrackInfo.module.css";

interface TrackInfoProps {
  songTitle: string;
  artist: string;
}

export function TrackInfo({ songTitle, artist }: TrackInfoProps) {
  return (
    <div className={styles.row}>
      <div className={styles.text}>
        <div className={styles.title}>{songTitle}</div>
        <div className={styles.artist}>{artist}</div>
      </div>
    </div>
  );
}
