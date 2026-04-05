from typing import List

from src.recommender import load_songs, recommend_songs

# Set to None to use each profile's built-in mode.
# Or force one mode for all profiles:
# "balanced", "genre_first", "mood_first", "energy_focus"
FORCE_MODE = None


PROFILES = {
    "High-Energy Pop": {
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.85,
        "target_tempo_bpm": 124,
        "target_valence": 0.82,
        "likes_acoustic": False,
        "favorite_detailed_mood": "uplifting|bright|summer",
        "preferred_decade": 2020,
        "wants_instrumental": False,
        "ranking_mode": "balanced",
    },
    "Chill Lofi": {
        "favorite_genre": "lofi",
        "favorite_mood": "chill",
        "target_energy": 0.35,
        "target_tempo_bpm": 78,
        "target_valence": 0.58,
        "likes_acoustic": True,
        "favorite_detailed_mood": "study|calm|cozy",
        "preferred_decade": 2020,
        "wants_instrumental": True,
        "ranking_mode": "mood_first",
    },
    "Deep Intense Rock": {
        "favorite_genre": "rock",
        "favorite_mood": "intense",
        "target_energy": 0.90,
        "target_tempo_bpm": 145,
        "target_valence": 0.45,
        "likes_acoustic": False,
        "favorite_detailed_mood": "aggressive|epic|driving",
        "preferred_decade": 2010,
        "wants_instrumental": False,
        "ranking_mode": "genre_first",
    },
    "Festival EDM Sprint": {
        "favorite_genre": "edm",
        "favorite_mood": "energetic",
        "target_energy": 0.97,
        "target_tempo_bpm": 150,
        "target_valence": 0.72,
        "likes_acoustic": False,
        "favorite_detailed_mood": "festival|hype|night",
        "preferred_decade": 2020,
        "wants_instrumental": False,
        "ranking_mode": "energy_focus",
    },
}


def wrap_text(text: str, width: int) -> List[str]:
    words = text.split()
    lines: List[str] = []
    current = ""

    for word in words:
        candidate = word if not current else f"{current} {word}"
        if len(candidate) <= width:
            current = candidate
        else:
            lines.append(current)
            current = word

    if current:
        lines.append(current)

    return lines or [""]


def print_table(rows: List[List[str]], headers: List[str]) -> None:
    all_rows = [headers] + rows
    widths = [max(len(str(row[i])) for row in all_rows) for i in range(len(headers))]
    border = "+" + "+".join("-" * (w + 2) for w in widths) + "+"

    print(border)
    print("| " + " | ".join(str(headers[i]).ljust(widths[i]) for i in range(len(headers))) + " |")
    print(border)

    for row in rows:
        wrapped_cells = [wrap_text(str(cell), widths[i]) for i, cell in enumerate(row)]
        max_lines = max(len(cell_lines) for cell_lines in wrapped_cells)

        for line_index in range(max_lines):
            print(
                "| "
                + " | ".join(
                    wrapped_cells[i][line_index].ljust(widths[i]) if line_index < len(wrapped_cells[i]) else "".ljust(widths[i])
                    for i in range(len(headers))
                )
                + " |"
            )
        print(border)


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    for profile_name, prefs in PROFILES.items():
        active_prefs = prefs.copy()
        if FORCE_MODE is not None:
            active_prefs["ranking_mode"] = FORCE_MODE

        recommendations = recommend_songs(active_prefs, songs, k=5, use_diversity=True)

        print("\n" + "=" * 110)
        print(f"PROFILE: {profile_name}")
        print(f"RANKING MODE: {active_prefs['ranking_mode']}")
        print("=" * 110)

        rows: List[List[str]] = []
        for rank, (song, score, explanation) in enumerate(recommendations, start=1):
            short_explanation = ", ".join(explanation.split(", ")[:3])
            rows.append(
                [
                    str(rank),
                    song["title"],
                    song["artist"],
                    f"{song['genre']} / {song['mood']}",
                    f"{score:.2f}",
                    short_explanation,
                ]
            )

        print_table(rows, ["#", "Title", "Artist", "Vibe", "Score", "Top Reasons"])


if __name__ == "__main__":
    main()