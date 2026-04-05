# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name

**VibeFinder Remix 1.0**

---

## 2. Intended Use

This recommender is designed to suggest 3 to 5 songs from a small catalog based on a user’s taste profile. It is mainly for classroom exploration, not for real users in a production music app.

The system assumes that a user’s current taste can be represented with a few preferences such as genre, mood, energy, tempo, and acoustic style. That is useful for a simulation, but it simplifies real human taste.

---

## 3. How the Model Works

The model compares each song to a user profile and gives it a numeric score. It adds points for direct matches such as genre or mood, and it also adds similarity points when numeric features like energy, tempo, and valence are close to the user’s target values.

I added extra features beyond the starter dataset, including popularity, release decade, detailed mood tags, instrumentalness, and live feel. The recommender can use some of those features to tell the difference between songs that are all “pop” but have different textures or vibes.

After the score is calculated for every song, the system ranks the songs from highest to lowest. Then it applies a small diversity penalty so the final top results are less likely to repeat the same artist or same genre too many times.

The program also supports multiple ranking modes:
- balanced
- genre_first
- mood_first
- energy_focus

This makes it easier to compare how different scoring priorities change the final output.

---

## 4. Data

The dataset contains **20 songs** in `data/songs.csv`.

Core attributes:
- genre
- mood
- energy
- tempo_bpm
- valence
- danceability
- acousticness

Additional attributes:
- popularity
- release_decade
- detailed_mood
- instrumentalness
- live_feel

The genres include pop, lofi, rock, ambient, jazz, synthwave, indie pop, hyperpop, acoustic, classical, and edm. The data is hand-crafted and small, so it does not represent real musical diversity equally. Some genres have more songs than others, and the dataset mostly reflects the limited taste boundaries I designed into it.

---

## 5. Strengths

This system works well when the user has a clear vibe in mind. For example, the High-Energy Pop profile gets bright, upbeat songs, while the Chill Lofi profile gets calmer and more acoustic tracks.

A major strength is transparency. The model explains exactly why a song ranked well, using readable reasons such as genre match, mood match, energy similarity, or detailed mood overlap.

Another strength is that the multiple ranking modes make it easy to compare strategies. The same profile can behave differently in `balanced` mode versus `energy_focus`, which makes the recommender easier to analyze.

---

## 6. Limitations and Bias

The system has several limitations.

First, the dataset is very small. That makes the recommendations easy to inspect, but it also means the model can become repetitive and overfit to the few songs available.

Second, the recommender depends only on metadata. It does not know anything about lyrics, vocal tone, cultural context, listening history, or why a listener might want novelty instead of similarity.

Third, the weighting system can create bias. If genre is weighted too heavily, the recommender may keep returning obvious genre matches even when another song fits the emotional vibe better. This can create a small filter bubble.

The diversity penalty helps with fairness and novelty by reducing repeated artists and repeated genres in the top list, but it is still a simple rule and not a full fairness solution.

---

## 7. Evaluation

I evaluated the system by running it on four different user profiles:

1. High-Energy Pop
2. Chill Lofi
3. Deep Intense Rock
4. Festival EDM Sprint

I checked whether the top recommendations matched my intuition and whether the explanations made sense relative to the scoring rule. I also compared how recommendations changed when different ranking modes were used.

Some expected patterns appeared:
- Pop users got bright, high-valence songs.
- Lofi users got lower-energy, more acoustic or instrumental songs.
- Rock users got more aggressive, higher-energy tracks.
- EDM users benefited from the energy-focused mode.

One thing that stood out was how much a mode switch changed the outcome. When energy and tempo were emphasized, songs outside the exact genre still ranked highly if they matched the vibe.

---

## 8. Future Work

If I kept developing this project, I would improve it in these ways:

1. Add more songs and balance the genre distribution so the catalog is less biased.
2. Use more nuanced diversity logic so the recommender can encourage variety without punishing good matches too much.
3. Add a collaborative filtering layer or simple user history so the system can learn from behavior, not just song metadata.
4. Improve explanations by summarizing the strongest reasons first instead of listing every factor.

---

## 9. Personal Reflection

My biggest learning moment was seeing how a simple weighted score can still feel like a recommendation system. The code is not complicated, but once the inputs are chosen carefully, the results can look surprisingly believable.

What surprised me most was how quickly bias appears. A design choice like “genre should matter more” sounds harmless, but it can change the whole personality of the recommender. Building the project made real streaming platforms feel less mysterious, but it also made me more aware of how much human judgment is hidden inside “smart” systems.