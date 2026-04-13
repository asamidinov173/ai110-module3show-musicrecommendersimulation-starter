from src.recommender import Song, UserProfile, Recommender, score_song, recommend_songs


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
            artist="Test Artist",
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
    # Starter expectation: the pop, happy, high energy song should score higher
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


def test_genre_match_adds_to_score():
    """Verify that a genre match increases the score."""
    user_prefs = {"genre": "pop", "mood": "chill", "energy": 0.5, "likes_acoustic": False}
    song = {"genre": "pop", "mood": "happy", "energy": 0.5, "valence": 0.5, "acousticness": 0.1}
    score, reasons = score_song(user_prefs, song)
    assert score > 0
    assert any("genre" in r.lower() for r in reasons)


def test_mood_match_adds_to_score():
    """Verify that a mood match increases the score."""
    user_prefs = {"genre": "rock", "mood": "happy", "energy": 0.5, "likes_acoustic": False}
    song = {"genre": "pop", "mood": "happy", "energy": 0.5, "valence": 0.5, "acousticness": 0.1}
    score, reasons = score_song(user_prefs, song)
    assert any("mood" in r.lower() for r in reasons)


def test_acoustic_bonus_applied():
    """Verify acoustic bonus is added when user likes acoustic and song is acoustic."""
    user_prefs = {"genre": "jazz", "mood": "chill", "energy": 0.3, "likes_acoustic": True}
    song = {"genre": "jazz", "mood": "chill", "energy": 0.3, "valence": 0.6, "acousticness": 0.85}
    score, reasons = score_song(user_prefs, song)
    assert any("acoustic" in r.lower() for r in reasons)


def test_no_acoustic_bonus_when_user_dislikes():
    """Verify acoustic bonus is NOT added when user doesn't like acoustic."""
    user_prefs = {"genre": "pop", "mood": "happy", "energy": 0.8, "likes_acoustic": False}
    song = {"genre": "pop", "mood": "happy", "energy": 0.8, "valence": 0.9, "acousticness": 0.9}
    score, reasons = score_song(user_prefs, song)
    assert not any("acoustic match" in r.lower() for r in reasons)


def test_recommend_songs_returns_top_k():
    """Verify recommend_songs returns exactly k results."""
    songs = [
        {"genre": "pop", "mood": "happy", "energy": 0.8, "valence": 0.9, "acousticness": 0.2, "title": "A"},
        {"genre": "lofi", "mood": "chill", "energy": 0.4, "valence": 0.6, "acousticness": 0.9, "title": "B"},
        {"genre": "rock", "mood": "intense", "energy": 0.9, "valence": 0.5, "acousticness": 0.1, "title": "C"},
    ]
    user_prefs = {"genre": "pop", "mood": "happy", "energy": 0.8, "likes_acoustic": False}
    results = recommend_songs(user_prefs, songs, k=2)
    assert len(results) == 2


def test_recommend_songs_sorted_by_score():
    """Verify recommend_songs returns results in descending score order."""
    songs = [
        {"genre": "pop", "mood": "happy", "energy": 0.8, "valence": 0.9, "acousticness": 0.2, "title": "Best Match"},
        {"genre": "rock", "mood": "intense", "energy": 0.9, "valence": 0.5, "acousticness": 0.1, "title": "Poor Match"},
    ]
    user_prefs = {"genre": "pop", "mood": "happy", "energy": 0.8, "likes_acoustic": False}
    results = recommend_songs(user_prefs, songs, k=2)
    assert results[0][1] >= results[1][1]


def test_empty_song_list():
    """Verify recommender handles an empty song list gracefully."""
    user_prefs = {"genre": "pop", "mood": "happy", "energy": 0.8, "likes_acoustic": False}
    results = recommend_songs(user_prefs, [], k=5)
    assert results == []