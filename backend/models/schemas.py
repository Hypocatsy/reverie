from pydantic import BaseModel, Field
from typing import Optional


class SongInput(BaseModel):
    """Song data provided by the user, from any input method.

    Attributes:
        title: Song title.
        artist: Artist name.
        lyrics: Optional raw lyrics text.
        spotify_track_id: Optional Spotify track ID if resolved.
        energy: Spotify audio feature, 0.0–1.0.
        valence: Spotify audio feature for positivity, 0.0–1.0.
        tempo: Beats per minute from Spotify.
        genres: List of genre tags from Spotify.
    """

    title: str
    artist: str
    lyrics: Optional[str] = None
    spotify_track_id: Optional[str] = None
    energy: Optional[float] = None
    valence: Optional[float] = None
    tempo: Optional[float] = None
    genres: list[str] = Field(default_factory=list)


class GenerateRequest(BaseModel):
    """Request body for POST /api/generate.

    Attributes:
        song: Resolved song data from any input method.
    """

    song: SongInput


class GenerateResponse(BaseModel):
    """Response body for POST /api/generate.

    Attributes:
        image_url: URL of the generated image from the image provider.
        visual_prompt: The LLM-generated prompt used for image generation.
        song_title: Resolved song title for display.
        artist: Resolved artist name for display.
    """

    image_url: str
    visual_prompt: str
    song_title: str
    artist: str


class SpotifyTrackResponse(BaseModel):
    """Response body for GET /api/spotify/track.

    Attributes:
        title: Track title.
        artist: Primary artist name.
        album: Album name.
        genres: Genre tags.
        energy: Audio feature, 0.0–1.0.
        valence: Audio feature for positivity, 0.0–1.0.
        tempo: Beats per minute.
        track_id: Spotify track ID.
        fallback: True if audio features were unavailable and partial data is returned.
    """

    title: str
    artist: str
    album: str
    genres: list[str]
    energy: Optional[float] = None
    valence: Optional[float] = None
    tempo: Optional[float] = None
    track_id: str
    fallback: bool = False


class ImageRequest(BaseModel):
    """Request body for POST /api/generate/image.

    Attributes:
        visual_prompt: The LLM-generated visual prompt to use for image generation.
    """

    visual_prompt: str


class ErrorResponse(BaseModel):
    """Standard error response shape.

    Attributes:
        error: Machine-readable error code.
        message: Human-readable message, safe to display in the UI.
    """

    error: str
    message: str
