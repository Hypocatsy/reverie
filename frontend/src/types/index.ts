export interface SongInput {
  title: string;
  artist: string;
  spotify_track_id?: string;
  energy?: number;
  valence?: number;
  tempo?: number;
  genres?: string[];
}

export interface SpotifyTrackResponse {
  title: string;
  artist: string;
  album: string;
  genres: string[];
  energy?: number;
  valence?: number;
  tempo?: number;
  track_id: string;
  fallback: boolean;
}
