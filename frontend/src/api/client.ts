import type { SongInput, SpotifyTrackResponse } from "../types";

// Always use relative URLs — Vite proxies /api to the backend in dev,
// and on Railway both frontend and backend share the same origin.

export async function resolveSpotifyTrack(url: string): Promise<SpotifyTrackResponse> {
  const res = await fetch(`/api/spotify/track?url=${encodeURIComponent(url)}`);

  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(
      err.detail ?? "Reverie couldn't find that song — tell me about it instead?"
    );
  }

  return res.json();
}

export async function generatePrompt(
  song: SongInput,
): Promise<{ visual_prompt: string; song_title: string; artist: string }> {
  const res = await fetch("/api/generate/prompt", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ song }),
  });

  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail ?? "Something went wrong. Please try again.");
  }

  return res.json();
}

export async function generateImageFromPrompt(
  visual_prompt: string,
): Promise<{ image_url: string }> {
  const res = await fetch("/api/generate/image", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ visual_prompt }),
  });

  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail ?? "Something went wrong. Please try again.");
  }

  return res.json();
}
