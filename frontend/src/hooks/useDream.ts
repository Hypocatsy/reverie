import { useState, useCallback } from "react";
import { resolveSpotifyTrack, generatePrompt, generateImageFromPrompt } from "../api/client";
import type { SongInput } from "../types";

export type DreamStage = "prompt" | "image";
export type DreamStatus = "idle" | "dreaming" | "success" | "error";

export interface DreamResult {
  image_url: string;
  visual_prompt: string;
  song_title: string;
  artist: string;
}

export interface DreamState {
  status: DreamStatus;
  stage: DreamStage | null;
  result: DreamResult | null;
  error: string | null;
  dream: (spotifyUrl: string) => Promise<void>;
  reset: () => void;
}

export function useDream(): DreamState {
  const [status, setStatus] = useState<DreamStatus>("idle");
  const [stage, setStage] = useState<DreamStage | null>(null);
  const [result, setResult] = useState<DreamResult | null>(null);
  const [error, setError] = useState<string | null>(null);

  const dream = useCallback(async (url: string) => {
    setStatus("dreaming");
    setStage("prompt");
    setError(null);
    setResult(null);

    // Step 1: resolve Spotify track
    let song: SongInput;
    try {
      const track = await resolveSpotifyTrack(url);
      song = {
        title: track.title,
        artist: track.artist,
        spotify_track_id: track.track_id,
        energy: track.energy,
        valence: track.valence,
        tempo: track.tempo,
        genres: track.genres,
      };
    } catch {
      setStatus("error");
      setError("Couldn't find that track. Check the link and try again.");
      return;
    }

    // Step 2: fetch lyrics + generate visual prompt
    let visual_prompt: string;
    let song_title: string;
    let artist: string;
    try {
      const promptResult = await generatePrompt(song);
      visual_prompt = promptResult.visual_prompt;
      song_title = promptResult.song_title;
      artist = promptResult.artist;
    } catch {
      setStatus("error");
      setError("Something went wrong while imagining the scene.");
      return;
    }

    // Step 3: generate image
    setStage("image");
    try {
      const imageResult = await generateImageFromPrompt(visual_prompt);
      setResult({ image_url: imageResult.image_url, visual_prompt, song_title, artist });
      setStatus("success");
    } catch {
      setStatus("error");
      setError("The dream couldn't be painted. Try again.");
    }
  }, []);

  const reset = useCallback(() => {
    setStatus("idle");
    setStage(null);
    setResult(null);
    setError(null);
  }, []);

  return { status, stage, result, error, dream, reset };
}
