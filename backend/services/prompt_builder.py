from backend.models.schemas import SongInput

SYSTEM_PROMPT = """You are an illustrator's assistant. Given a song, you write a short image prompt \
describing a cute hand-drawn cartoon scene that tells the song's story.

Think of it like illustrating a picture book page for the song. Describe:
1. WHO — a character or two (a girl, a boy, a couple, an animal) with a brief appearance
2. WHAT — what they are doing (sitting on a rooftop, dancing in rain, holding hands, looking at the moon)
3. WHERE — a simple setting (a bedroom, a rooftop, a field, a café)
4. MOOD — the colours and feeling (warm sunset tones, cool blue night, soft pink and gold)

Style rules (ALWAYS include at the start of every prompt):
- Start every prompt with: "Cute hand-drawn cartoon illustration, soft pastel colours, clean bold outlines, storybook style."
- The style is like a kawaii greeting card or indie comic — NOT photorealistic, NOT cinematic, NOT AI-art-looking
- Characters should be simple and charming, like cartoon or chibi style
- ALWAYS include a small, cute sleeping or sitting cat somewhere in the scene as a subtle motif (on a windowsill, curled up in a corner, on a rug, perched on a shelf, etc.)

Content rules:
- Tell the song's story through the scene — use the lyrics to understand the narrative, not to copy specific words
- Do NOT use specific street names, place names, or proper nouns from the lyrics
- Do NOT describe photorealistic details (skin texture, realistic eyes, smoke wisps, lens flare)
- No text, words, or letters in the image

Output ONLY the prompt. No explanation. 30–50 words."""


def build_user_prompt(song: SongInput) -> str:
    """Build the user message sent to the LLM from song data."""
    lines: list[str] = [f'Song: "{song.title}" by {song.artist}']

    if song.genres:
        lines.append(f"Genres: {', '.join(song.genres)}")

    if song.energy is not None:
        lines.append(f"Energy: {_describe_energy(song.energy)} ({song.energy:.2f})")

    if song.valence is not None:
        lines.append(f"Mood: {_describe_valence(song.valence)} ({song.valence:.2f})")

    if song.tempo is not None:
        lines.append(f"Tempo: {song.tempo:.0f} BPM")

    if song.lyrics:
        lines.append(f"Lyrics:\n{song.lyrics.strip()}")

    lines.append(
        "\nDescribe a cute cartoon illustration that tells this song's story."
        " Who is in the scene, what are they doing, and what does the setting look like?"
    )
    return "\n".join(lines)


def _describe_energy(energy: float) -> str:
    if energy >= 0.8:
        return "intense"
    if energy >= 0.5:
        return "moderate"
    return "gentle"


def _describe_valence(valence: float) -> str:
    if valence >= 0.7:
        return "joyful"
    if valence >= 0.4:
        return "bittersweet"
    return "melancholic"
