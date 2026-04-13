# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name

**VibeFinder 1.0**

---

## 2. Intended Use

VibeFinder 1.0 suggests songs from a small catalog based on a user's preferred genre, mood, and energy level. It assumes the user has a single dominant taste profile — one favorite genre, one preferred mood, and a target energy level. This system is built for classroom exploration only and is not designed for real production use.

**Non-intended use:** This system should NOT be used as a real music recommendation product. It should not be used to make decisions about what content to show real users, to profile users based on their taste, or in any commercial product. The catalog is too small, the weights are not learned from real data, and the system has no safeguards against bias or unfairness.

---

## 3. How the Model Works

VibeFinder compares each song in the catalog against what the user likes and assigns it a score. Songs that match the user's favorite genre earn the most points (3 points), followed by mood matches (2 points). For energy and positivity (valence), the system rewards songs that are *close* to what the user wants — not just high or low — so a user who likes medium energy won't always get the most intense songs. There is also a small bonus for acoustic songs if the user prefers that sound. All songs are then ranked from highest to lowest score, and the top results are returned as recommendations.

---

## 4. Data

The catalog contains 18 songs stored in `data/songs.csv`. The genres represented are pop, lofi, rock, ambient, jazz, synthwave, indie pop, country, hip-hop, classical, r&b, and electronic. Moods include happy, chill, intense, relaxed, focused, moody, and energetic. 8 songs were added to the original 10-song dataset to improve diversity. The catalog still skews toward electronic and chill genres, and some genres like country and classical have only one song each.

---

## 5. Strengths

- Works well for pop and lofi users since those genres have multiple songs with varied moods
- The energy closeness scoring correctly avoids recommending the most intense tracks to calm users
- The Chill Lofi profile scored the highest (8.60) because genre, mood, and acoustic bonus all aligned — showing the system rewards well-matched profiles strongly
- Recommendations for High-Energy Pop and Deep Intense Rock both felt intuitive

---

## 6. Limitations and Bias

- The catalog only has 18 songs, so users with niche tastes (classical, country) get very limited variety
- Genre weight (3.0) dominates over mood (2.0) — in the conflicting profile test, Coffee Shop Stories ranked first because jazz + relaxed outweighed the energy mismatch, even though the user wanted high energy
- The system creates a filter bubble: the same 2-3 songs appear across multiple profiles because the catalog is small and genre-skewed
- Fixed weights treat all users equally — a user who cares more about energy than genre cannot express that preference
- Tempo and danceability are loaded from the CSV but completely ignored in scoring, wasting useful signal

---

## 7. Evaluation

Five user profiles were tested:

1. **High-Energy Pop** — Sunrise City ranked first (7.78). Results felt accurate and matched intuition.
2. **Chill Lofi** — Library Rain ranked first (8.60). The acoustic bonus pushed lofi songs to the top correctly.
3. **Deep Intense Rock** — Storm Runner ranked first (7.56). Only one rock song in the catalog, so diversity was limited.
4. **Conflicting Prefs (jazz/relaxed + high energy)** — Coffee Shop Stories won at 6.75 despite low energy (0.37 vs target 0.9). This revealed that genre + mood weight can override a large energy mismatch — a clear bias.
5. **Acoustic Lover (classical/relaxed)** — No classical genre match found. Coffee Shop Stories (jazz) was the best available option, showing the catalog gap for classical users.

The most surprising result was the conflicting profile — a user asking for jazz + relaxed + high energy got a very calm song at the top. This shows the system prioritizes categorical matches (genre, mood) over numerical closeness (energy).

Nine automated tests were written and all passed.

---

## 8. Future Work

- Add more songs across underrepresented genres (classical, country, hip-hop) to reduce bias
- Use tempo and danceability in the scoring formula
- Allow users to set custom weights (e.g., "energy matters more to me than genre")
- Add diversity logic so the top 5 results don't all come from the same genre
- Support multiple taste profiles per user (e.g., "workout mode" vs "study mode")
- Replace fixed weights with learned weights based on user feedback (likes/skips)

---

## 9. Personal Reflection

Building VibeFinder showed me that recommendation systems are not magic — they are just scoring rules with weights. The hardest part was deciding how much each feature should matter, and realizing those weights encode assumptions about all users equally. What surprised me most was the conflicting profile test — a user who wanted high energy jazz got a very calm song recommended because the genre and mood weights dominated. Real platforms like Spotify have millions of songs and use collaborative filtering to avoid this problem. This project changed how I think about recommendation apps — what feels like "the algorithm knows me" is really just a weighted score running thousands of times per second.