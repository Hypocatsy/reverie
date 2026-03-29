import styles from "./FloatingParticles.module.css";

const PARTICLES = [
  { char: "✦", x: 7,  y: 12, size: 10, delay: 0,    dur: 4.2 },
  { char: "☽", x: 88, y: 8,  size: 14, delay: 1.1,  dur: 5.0 },
  { char: "✦", x: 22, y: 72, size: 8,  delay: 2.4,  dur: 3.8 },
  { char: "✧", x: 78, y: 55, size: 11, delay: 0.6,  dur: 4.5 },
  { char: "☽", x: 15, y: 40, size: 12, delay: 3.2,  dur: 5.3 },
  { char: "✦", x: 92, y: 35, size: 9,  delay: 1.8,  dur: 4.0 },
  { char: "✧", x: 50, y: 5,  size: 7,  delay: 0.3,  dur: 3.6 },
  { char: "✦", x: 65, y: 85, size: 10, delay: 2.0,  dur: 4.8 },
  { char: "☽", x: 35, y: 90, size: 11, delay: 1.5,  dur: 5.1 },
  { char: "✧", x: 5,  y: 60, size: 8,  delay: 3.8,  dur: 3.9 },
  { char: "✦", x: 72, y: 20, size: 6,  delay: 0.9,  dur: 4.3 },
  { char: "✧", x: 42, y: 48, size: 9,  delay: 2.7,  dur: 4.6 },
] as const;

export function FloatingParticles() {
  return (
    <div className={styles.container} aria-hidden="true">
      {PARTICLES.map((p, i) => (
        <span
          key={i}
          className={styles.particle}
          style={{
            left: `${p.x}%`,
            top: `${p.y}%`,
            fontSize: `${p.size}px`,
            animationDelay: `${p.delay}s`,
            animationDuration: `${p.dur}s`,
          }}
        >
          {p.char}
        </span>
      ))}
    </div>
  );
}
