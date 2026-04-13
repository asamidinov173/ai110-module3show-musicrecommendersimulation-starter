# 🎵 Music Recommender Simulation

## Project Summary

This project simulates how a music platform like Spotify or TikTok recommends songs to users. It uses a content-based filtering approach — meaning it compares the attributes of songs (like genre, mood, and energy) directly against a user's taste profile to generate personalized suggestions. Unlike collaborative filtering (which relies on what other users listened to), this system works entirely from the song's own features.

---

## How The System Works

Real-world recommenders like Spotify combine two main techniques. Collaborative filtering finds users with similar listening history and recommends what they liked. Content-based filtering analyzes the features of songs themselves — tempo, energy, mood — and matches them to what a user has enjoyed before. This simulation focuses on content-based filtering.

**Song features used:**
- `genre` — the musical category (pop, lofi, rock, jazz, etc.)
- `mood` — the emotional tone (happy, chill, intense, focused, etc.)
- `energy` — a 0.0–1.0 score of how energetic the song feels
- `valence` — a 0.0–1.0 score of how positive or upbeat the song is
- `tempo_bpm` — beats per minute

**UserProfile stores:**
- `favorite_genre` — the genre they prefer most
- `favorite_mood` — the mood they want to match
- `target_energy` — their preferred energy level (0.0–1.0)
- `likes_acoustic` — whether they prefer acoustic sounds

**Scoring rule:**
Each song gets a score based on how closely it matches the user's preferences:
- Genre match → +3 points
- Mood match → +2 points
- Energy closeness → up to +2 points (1 - abs difference)
- Valence closeness → up to +1 point
- Acoustic bonus → +1 point if user likes acoustic and acousticness > 0.6

**Ranking rule:**
All songs are scored individually, then sorted from highest to lowest score. The top k songs are returned as recommendations.

## Algorithm Recipe

| Feature | Points | Notes |
|---|---|---|
| Genre match | +3.0 | Strongest signal of taste |
| Mood match | +2.0 | Second strongest signal |
| Energy closeness | up to +2.0 | `2.0 * (1 - abs(song_energy - target_energy))` |
| Valence closeness | up to +1.0 | Rewards positivity match |
| Acoustic bonus | +1.0 | Only if user likes acoustic AND song acousticness > 0.6 |

## Data Flow

```mermaid
flowchart TD
    A[User Preferences\ngenre, mood, energy, likes_acoustic] --> B[Load songs.csv\n18 songs]
    B --> C{For each song...}
    C --> D[score_song\nApply Algorithm Recipe]
    D --> E[Collect scored songs\nsong, score, reasons]
    E --> F[Sort by score\ndescending]
    F --> G[Return top K\nrecommendations]
    G --> H[Display results\ntitle, score, explanation]
```

## Expected Biases

- **Genre dominance** — genre is worth 3 points vs mood's 2, so a genre match will always outweigh a perfect mood match
- **Filter bubble risk** — if a user's favorite genre dominates the catalog, they will rarely see other genres even if the mood and energy match well
- **Fixed weights** — all users are scored with the same weights regardless of their actual listening behavior
- **Missing features** — tempo and danceability are in the dataset but not used in scoring

---

## Getting Started

### Setup

1. Create a virtual environment:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the app:

   ```bash
   python -m src.main
   ```

### Running Tests

```bash
pytest
```

---

## 📸 Demo

![Recommendations Output](recommend-output-module3.png)

## Experiments You Tried

*(To be filled in after implementation)*

---

## Limitations and Risks

- Only works on a tiny 10-song catalog
- Does not understand lyrics or language
- May over-favor one genre if the catalog is imbalanced
- Treats all users with the same scoring weights regardless of listening history

---

## Reflection

Building VibeFinder taught me that recommendation systems are fundamentally just scoring rules — there is no magic, just weighted math. My biggest learning moment was the conflicting profile test, where a user asking for high-energy jazz got a very calm song recommended because genre and mood weights dominated over energy closeness. That showed me how fixed weights can override what the user actually cares about most.

AI tools helped me move fast — generating the CSV data, scaffolding the scoring function, and writing tests in minutes. But I needed to double-check the import paths (the `from recommender import` vs `from src.recommender import` bug), verify that the scoring logic actually matched my algorithm recipe, and make sure the TODO comments were preserved in the right places.

What surprised me most was how "smart" simple algorithms can feel. When Sunrise City scored 7.92 for a pop/happy/high-energy user, it felt like the system genuinely understood that user — but it was just three weighted additions. That gap between "feels intelligent" and "is actually just math" is exactly what makes AI systems both powerful and risky to deploy without careful evaluation.

If I extended this project, I would add user feedback (likes/skips) to learn weights over time, and add diversity logic so the top 5 results always span at least 3 different genres.

---

## Model Card

[**Model Card**](model_card.md)