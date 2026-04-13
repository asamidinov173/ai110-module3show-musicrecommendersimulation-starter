"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.
You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""
from src.recommender import load_songs, recommend_songs


def print_recommendations(profile_name: str, user_prefs: dict, songs: list, k: int = 5):
    """Print top k recommendations for a given user profile."""
    print(f"\n{'=' * 50}")
    print(f"  Profile: {profile_name}")
    print(f"{'=' * 50}")
    recommendations = recommend_songs(user_prefs, songs, k=k)
    for i, rec in enumerate(recommendations, 1):
        song, score, explanation = rec
        print(f"{i}. {song['title']} - Score: {score:.2f}")
        print(f"   Because: {explanation}")
        print()


def main() -> None:
    songs = load_songs("data/songs.csv")

    # Profile 1: High-Energy Pop
    print_recommendations(
        "High-Energy Pop",
        {"genre": "pop", "mood": "happy", "energy": 0.9, "likes_acoustic": False},
        songs
    )

    # Profile 2: Chill Lofi
    print_recommendations(
        "Chill Lofi",
        {"genre": "lofi", "mood": "chill", "energy": 0.3, "likes_acoustic": True},
        songs
    )

    # Profile 3: Deep Intense Rock
    print_recommendations(
        "Deep Intense Rock",
        {"genre": "rock", "mood": "intense", "energy": 0.9, "likes_acoustic": False},
        songs
    )

    # Profile 4: Edge case — high energy but relaxed mood (conflicting)
    print_recommendations(
        "Conflicting Prefs (high energy + relaxed mood)",
        {"genre": "jazz", "mood": "relaxed", "energy": 0.9, "likes_acoustic": False},
        songs
    )

    # Profile 5: Acoustic lover
    print_recommendations(
        "Acoustic Lover",
        {"genre": "classical", "mood": "relaxed", "energy": 0.2, "likes_acoustic": True},
        songs
    )


if __name__ == "__main__":
    main()