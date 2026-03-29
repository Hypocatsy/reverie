const IMG_PAD = 36;           // cream padding around the image
const IMG_SIZE = 1024;        // AI image native size
const CARD_W = IMG_SIZE + IMG_PAD * 2;          // 1096
const STRIP_H = 396;          // info strip height
const CARD_H = IMG_PAD + IMG_SIZE + STRIP_H;    // 1456
const RADIUS = 40;
const TEXT_PAD = 60;

const CREAM = "#F5F2EA";
const INK = "#3D3244";
const CTA = "#6B5B8B";
const SURFACE = "#6B5B8B";

/**
 * Draw a collectible illustration card to canvas and trigger a PNG download.
 */
export async function downloadCard(
  imageUrl: string,
  songTitle: string,
  artist: string,
): Promise<void> {
  // Load image
  const img = new Image();
  img.crossOrigin = "anonymous";
  img.src = imageUrl;
  await new Promise<void>((resolve, reject) => {
    img.onload = () => resolve();
    img.onerror = reject;
  });

  // Ensure fonts are ready
  await document.fonts.ready;

  const canvas = document.createElement("canvas");
  canvas.width = CARD_W;
  canvas.height = CARD_H;
  const ctx = canvas.getContext("2d");
  if (!ctx) return;

  // Clip to rounded rect
  ctx.beginPath();
  ctx.roundRect(0, 0, CARD_W, CARD_H, RADIUS);
  ctx.clip();

  // --- Cream background (fills entire card) ---
  ctx.fillStyle = CREAM;
  ctx.fillRect(0, 0, CARD_W, CARD_H);

  // --- AI image (inset with padding, rounded corners, center-cropped) ---
  const imgX = IMG_PAD;
  const imgY = IMG_PAD;
  const imgR = 20; // inner image corner radius
  ctx.save();
  ctx.beginPath();
  ctx.roundRect(imgX, imgY, IMG_SIZE, IMG_SIZE, imgR);
  ctx.clip();

  // Center-crop: scale to cover the square, then center
  const srcW = img.naturalWidth;
  const srcH = img.naturalHeight;
  const scale = Math.max(IMG_SIZE / srcW, IMG_SIZE / srcH);
  const drawW = srcW * scale;
  const drawH = srcH * scale;
  const drawX = imgX + (IMG_SIZE - drawW) / 2;
  const drawY = imgY + (IMG_SIZE - drawH) / 2;
  ctx.drawImage(img, drawX, drawY, drawW, drawH);

  ctx.restore();

  // --- Text positions (relative to strip) ---
  const stripTop = IMG_PAD + IMG_SIZE;
  const stripMid = stripTop + STRIP_H / 2;

  // --- Song title ---
  ctx.textAlign = "center";
  ctx.textBaseline = "middle";
  ctx.fillStyle = INK;
  ctx.globalAlpha = 1;

  let titleSize = 42;
  ctx.font = `500 ${titleSize}px "Playfair Display", Georgia, serif`;
  while (ctx.measureText(songTitle).width > CARD_W - TEXT_PAD * 2 && titleSize > 20) {
    titleSize -= 2;
    ctx.font = `500 ${titleSize}px "Playfair Display", Georgia, serif`;
  }
  ctx.fillText(songTitle, CARD_W / 2, stripMid - 70);

  // --- Artist ---
  ctx.globalAlpha = 0.7;
  let artistSize = 28;
  ctx.font = `300 ${artistSize}px "Inter", system-ui, sans-serif`;
  while (ctx.measureText(artist).width > CARD_W - TEXT_PAD * 2 && artistSize > 14) {
    artistSize -= 2;
    ctx.font = `300 ${artistSize}px "Inter", system-ui, sans-serif`;
  }
  ctx.fillText(artist, CARD_W / 2, stripMid - 10);

  // --- Decorative flourish ---
  ctx.globalAlpha = 0.4;
  ctx.strokeStyle = SURFACE;
  ctx.fillStyle = SURFACE;
  ctx.lineWidth = 1;

  const fy = stripMid + 80;
  const cx = CARD_W / 2;

  // Left line
  ctx.beginPath();
  ctx.moveTo(cx - 80, fy);
  ctx.lineTo(cx - 10, fy);
  ctx.stroke();

  // Right line
  ctx.beginPath();
  ctx.moveTo(cx + 10, fy);
  ctx.lineTo(cx + 80, fy);
  ctx.stroke();

  // Center diamond
  ctx.beginPath();
  ctx.moveTo(cx, fy - 5);
  ctx.lineTo(cx + 5, fy);
  ctx.lineTo(cx, fy + 5);
  ctx.lineTo(cx - 5, fy);
  ctx.closePath();
  ctx.fill();

  // --- Wordmark ---
  ctx.globalAlpha = 1;
  ctx.fillStyle = CTA;
  ctx.font = `italic 300 20px "Playfair Display", Georgia, serif`;
  ctx.fillText("reverie", CARD_W / 2, stripMid + 150);

  // --- Border ---
  ctx.globalAlpha = 1;
  ctx.beginPath();
  ctx.roundRect(1.5, 1.5, CARD_W - 3, CARD_H - 3, RADIUS - 1);
  ctx.strokeStyle = "rgba(107,91,139,0.5)";
  ctx.lineWidth = 3;
  ctx.stroke();

  // --- Download ---
  canvas.toBlob((blob) => {
    if (!blob) return;
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `reverie-${songTitle.replace(/\s+/g, "-").toLowerCase()}.png`;
    a.click();
    URL.revokeObjectURL(url);
  }, "image/png");
}
