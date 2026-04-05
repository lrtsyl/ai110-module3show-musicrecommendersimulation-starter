from pathlib import Path

from src.recommender import Song, UserProfile, Recommender, load_songs, score_song, recommend_songs


def make_small_recommender() -> Recommender:
    songs = [
        Song(
            id=1,
            title="Test Pop Track",
            artist="Test Artist",
            genre="pop",
            mood="happy",
            energy=0.8,
            tempo_bpm=120,
            valence=0.9,
            danceability=0.8,
            acousticness=0.2,
        ),
        Song(
            id=2,
            title="Chill Lofi Loop",
            artist="Other Artist",
            genre="lofi",
            mood="chill",
            energy=0.4,
            tempo_bpm=80,
            valence=0.6,
            danceability=0.5,
            acousticness=0.9,
        ),
    ]
    return Recommender(songs)


def test_recommend_returns_songs_sorted_by_score():
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    rec = make_small_recommender()
    results = rec.recommend(user, k=2)

    assert len(results) == 2
    assert results[0].genre == "pop"
    assert results[0].mood == "happy"


def test_explain_recommendation_returns_non_empty_string():
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    rec = make_small_recommender()
    song = rec.songs[0]

    explanation = rec.explain_recommendation(user, song)
    assert isinstance(explanation, str)
    assert explanation.strip() != ""


def test_load_songs_reads_csv(tmp_path: Path):
    csv_text = (
        "id,title,artist,genre,mood,energy,tempo_bpm,valence,danceability,acousticness,popularity,release_decade,detailed_mood,instrumentalness,live_feel\n"
        "1,Song A,Artist A,pop,happy,0.8,120,0.9,0.7,0.2,80,2020,bright|uplifting,0.1,0.2\n"
    )
    csv_file = tmp_path / "songs.csv"
    csv_file.write_text(csv_text, encoding="utf-8")

    songs = load_songs(str(csv_file))

    assert len(songs) == 1
    assert songs[0]["title"] == "Song A"
    assert isinstance(songs[0]["energy"], float)


def test_functional_recommender_returns_explanations():
    songs = [
        {
            "id": 1,
            "title": "Song A",
            "artist": "Artist A",
            "genre": "pop",
            "mood": "happy",
            "energy": 0.8,
            "tempo_bpm": 120.0,
            "valence": 0.9,
            "danceability": 0.7,
            "acousticness": 0.2,
            "popularity": 80,
            "release_decade": 2020,
            "detailed_mood": "bright|uplifting",
            "instrumentalness": 0.1,
            "live_feel": 0.2,
        },
        {
            "id": 2,
            "title": "Song B",
            "artist": "Artist B",
            "genre": "rock",
            "mood": "intense",
            "energy": 0.9,
            "tempo_bpm": 140.0,
            "valence": 0.5,
            "danceability": 0.6,
            "acousticness": 0.1,
            "popularity": 75,
            "release_decade": 2010,
            "detailed_mood": "driving|aggressive",
            "instrumentalness": 0.05,
            "live_feel": 0.3,
        },
    ]
    prefs = {
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.8,
        "likes_acoustic": False,
        "ranking_mode": "balanced",
    }

    results = recommend_songs(prefs, songs, k=2)

    assert len(results) == 2
    assert results[0][0]["title"] == "Song A"
    assert isinstance(results[0][1], float)
    assert "genre match" in results[0][2]


def test_score_song_changes_across_modes():
    song = {
        "id": 1,
        "title": "Song A",
        "artist": "Artist A",
        "genre": "pop",
        "mood": "happy",
        "energy": 0.8,
        "tempo_bpm": 120.0,
        "valence": 0.9,
        "danceability": 0.7,
        "acousticness": 0.2,
        "popularity": 80,
        "release_decade": 2020,
        "detailed_mood": "bright|uplifting",
        "instrumentalness": 0.1,
        "live_feel": 0.2,
    }

    balanced_score, _ = score_song(
        {
            "favorite_genre": "pop",
            "favorite_mood": "happy",
            "target_energy": 0.8,
            "likes_acoustic": False,
            "ranking_mode": "balanced",
        },
        song,
    )

    genre_first_score, _ = score_song(
        {
            "favorite_genre": "pop",
            "favorite_mood": "happy",
            "target_energy": 0.8,
            "likes_acoustic": False,
            "ranking_mode": "genre_first",
        },
        song,
    )

    assert balanced_score != genre_first_score