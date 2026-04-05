from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
import csv


@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float
    popularity: int = 50
    release_decade: int = 2020
    detailed_mood: str = ""
    instrumentalness: float = 0.0
    live_feel: float = 0.0


@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool
    target_tempo_bpm: Optional[float] = None
    target_valence: Optional[float] = None
    preferred_decade: Optional[int] = None
    favorite_detailed_mood: Optional[str] = None
    wants_instrumental: Optional[bool] = None
    ranking_mode: str = "balanced"


def _song_to_dict(song: Song) -> Dict:
    return song.__dict__.copy()


def _user_to_dict(user: UserProfile) -> Dict:
    return user.__dict__.copy()


def _get_pref(user_prefs: Dict, *keys, default=None):
    for key in keys:
        if key in user_prefs and user_prefs[key] is not None:
            return user_prefs[key]
    return default


def _closeness_points(song_value: float, target_value: float, max_points: float, scale: float = 1.0) -> float:
    gap = abs(float(song_value) - float(target_value))
    similarity = max(0.0, 1.0 - gap / scale)
    return similarity * max_points


def _get_mode_weights(mode: str) -> Dict[str, float]:
    mode = (mode or "balanced").lower()

    presets = {
        "balanced": {
            "genre": 2.0,
            "mood": 1.5,
            "energy": 2.0,
            "tempo": 1.0,
            "valence": 1.0,
            "acoustic": 0.75,
            "detailed_mood": 0.75,
            "instrumental": 0.50,
            "decade": 0.50,
        },
        "genre_first": {
            "genre": 3.0,
            "mood": 1.0,
            "energy": 1.5,
            "tempo": 0.75,
            "valence": 0.75,
            "acoustic": 0.50,
            "detailed_mood": 0.50,
            "instrumental": 0.25,
            "decade": 0.25,
        },
        "mood_first": {
            "genre": 1.25,
            "mood": 2.5,
            "energy": 1.75,
            "tempo": 0.75,
            "valence": 1.25,
            "acoustic": 0.50,
            "detailed_mood": 1.0,
            "instrumental": 0.50,
            "decade": 0.25,
        },
        "energy_focus": {
            "genre": 1.0,
            "mood": 1.0,
            "energy": 3.0,
            "tempo": 1.5,
            "valence": 0.75,
            "acoustic": 0.50,
            "detailed_mood": 0.50,
            "instrumental": 0.25,
            "decade": 0.25,
        },
    }

    return presets.get(mode, presets["balanced"])


def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    songs: List[Dict] = []

    int_fields = {"id", "popularity", "release_decade"}
    float_fields = {
        "energy",
        "tempo_bpm",
        "valence",
        "danceability",
        "acousticness",
        "instrumentalness",
        "live_feel",
    }

    with open(csv_path, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            cleaned: Dict = {}
            for key, value in row.items():
                value = (value or "").strip()
                if key in int_fields:
                    cleaned[key] = int(value)
                elif key in float_fields:
                    cleaned[key] = float(value)
                else:
                    cleaned[key] = value
            songs.append(cleaned)

    return songs


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences.
    Required by recommend_songs() and src/main.py
    """
    mode = _get_pref(user_prefs, "ranking_mode", default="balanced")
    weights = _get_mode_weights(mode)

    score = 0.0
    reasons: List[str] = []

    genre_pref = _get_pref(user_prefs, "favorite_genre", "genre")
    mood_pref = _get_pref(user_prefs, "favorite_mood", "mood")
    energy_pref = _get_pref(user_prefs, "target_energy", "energy")
    tempo_pref = _get_pref(user_prefs, "target_tempo_bpm", "tempo_bpm")
    valence_pref = _get_pref(user_prefs, "target_valence", "valence")
    acoustic_pref = _get_pref(user_prefs, "likes_acoustic", default=None)
    detailed_mood_pref = _get_pref(user_prefs, "favorite_detailed_mood", default=None)
    wants_instrumental = _get_pref(user_prefs, "wants_instrumental", default=None)
    decade_pref = _get_pref(user_prefs, "preferred_decade", default=None)

    if genre_pref and song["genre"].lower() == str(genre_pref).lower():
        score += weights["genre"]
        reasons.append(f"genre match (+{weights['genre']:.2f})")

    if mood_pref and song["mood"].lower() == str(mood_pref).lower():
        score += weights["mood"]
        reasons.append(f"mood match (+{weights['mood']:.2f})")

    if energy_pref is not None:
        energy_points = _closeness_points(song["energy"], energy_pref, weights["energy"], scale=1.0)
        score += energy_points
        reasons.append(f"energy similarity (+{energy_points:.2f})")

    if tempo_pref is not None:
        tempo_points = _closeness_points(song["tempo_bpm"], tempo_pref, weights["tempo"], scale=80.0)
        score += tempo_points
        reasons.append(f"tempo similarity (+{tempo_points:.2f})")

    if valence_pref is not None:
        valence_points = _closeness_points(song["valence"], valence_pref, weights["valence"], scale=1.0)
        score += valence_points
        reasons.append(f"valence similarity (+{valence_points:.2f})")

    if acoustic_pref is True:
        acoustic_points = song["acousticness"] * weights["acoustic"]
        score += acoustic_points
        reasons.append(f"acoustic preference (+{acoustic_points:.2f})")
    elif acoustic_pref is False:
        acoustic_points = (1.0 - song["acousticness"]) * weights["acoustic"]
        score += acoustic_points
        reasons.append(f"less-acoustic preference (+{acoustic_points:.2f})")

    if detailed_mood_pref:
        song_tags = {
            part.strip().lower()
            for part in str(song.get("detailed_mood", "")).split("|")
            if part.strip()
        }
        user_tags = {
            part.strip().lower()
            for part in str(detailed_mood_pref).split("|")
            if part.strip()
        }
        overlap = len(song_tags & user_tags)
        if overlap:
            detailed_points = min(overlap, 2) / 2 * weights["detailed_mood"]
            score += detailed_points
            reasons.append(f"detailed mood overlap (+{detailed_points:.2f})")

    if wants_instrumental is True:
        instrumental_points = song.get("instrumentalness", 0.0) * weights["instrumental"]
        score += instrumental_points
        reasons.append(f"instrumental preference (+{instrumental_points:.2f})")
    elif wants_instrumental is False:
        vocal_points = (1.0 - song.get("instrumentalness", 0.0)) * weights["instrumental"]
        score += vocal_points
        reasons.append(f"vocal preference (+{vocal_points:.2f})")

    if decade_pref is not None:
        gap = abs(int(song.get("release_decade", 0)) - int(decade_pref))
        decade_points = max(0.0, 1.0 - gap / 30.0) * weights["decade"]
        score += decade_points
        reasons.append(f"era similarity (+{decade_points:.2f})")

    return round(score, 2), reasons


def _apply_diversity_penalty(song: Dict, selected: List[Dict]) -> Tuple[float, List[str]]:
    """
    Penalizes repetition so the top results are not all from the same artist or genre.
    Stretch feature: diversity / fairness logic
    """
    penalty = 0.0
    reasons: List[str] = []

    if any(existing["artist"].lower() == song["artist"].lower() for existing in selected):
        penalty += 0.80
        reasons.append("artist diversity penalty (-0.80)")

    if any(existing["genre"].lower() == song["genre"].lower() for existing in selected):
        penalty += 0.35
        reasons.append("genre diversity penalty (-0.35)")

    return penalty, reasons


def recommend_songs(
    user_prefs: Dict,
    songs: List[Dict],
    k: int = 5,
    use_diversity: bool = True,
) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py

    Returns:
        List of (song_dict, final_score, explanation)
    """
    base_scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        base_scored.append(
            {
                "song": song,
                "base_score": score,
                "reasons": reasons,
            }
        )

    base_scored.sort(key=lambda item: item["base_score"], reverse=True)

    selected: List[Tuple[Dict, float, str]] = []
    selected_songs: List[Dict] = []
    remaining = base_scored[:]

    while remaining and len(selected) < k:
        best_index = 0
        best_adjusted_score = None
        best_explanation = ""

        for idx, item in enumerate(remaining):
            adjusted_score = item["base_score"]
            reasons = item["reasons"][:]

            if use_diversity:
                penalty, penalty_reasons = _apply_diversity_penalty(item["song"], selected_songs)
                adjusted_score -= penalty
                reasons.extend(penalty_reasons)

            explanation = ", ".join(reasons)

            if best_adjusted_score is None or adjusted_score > best_adjusted_score:
                best_adjusted_score = adjusted_score
                best_index = idx
                best_explanation = explanation

        chosen = remaining.pop(best_index)
        final_score = round(best_adjusted_score if best_adjusted_score is not None else chosen["base_score"], 2)

        selected.append((chosen["song"], final_score, best_explanation))
        selected_songs.append(chosen["song"])

    return selected


class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        song_dicts = [_song_to_dict(song) for song in self.songs]
        ranked = recommend_songs(_user_to_dict(user), song_dicts, k=k, use_diversity=False)
        id_to_song = {song.id: song for song in self.songs}
        return [id_to_song[result[0]["id"]] for result in ranked]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        score, reasons = score_song(_user_to_dict(user), _song_to_dict(song))
        if not reasons:
            return f"{song.title} scored {score:.2f} from overall similarity."
        return f"{song.title} scored {score:.2f} because " + ", ".join(reasons) + "."