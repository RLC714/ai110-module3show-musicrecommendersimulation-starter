# Model Card: VibeFinder 1.0

## Model Name
VibeFinder 1.0

## Goal / Task
Suggest the top 5 songs from a small catalog that best match a listener's favorite genre, favorite mood, and target energy. Each suggestion comes with reasons.

## Data Used
- 20 songs in `data/songs.csv`: the 10 starter songs plus 10 I added to cover more genres and moods (hip-hop, EDM, country, classical, metal, R&B, folk, reggae, latin, blues).
- Attributes: genre, mood, energy, tempo_bpm, valence, danceability, acousticness (all 0.0 to 1.0 except tempo).
- 17 different genres. Most appear once. Lofi has three songs, pop has two, and rock has only one.
- Limits: tiny, hand-made, no listening history, no popularity, no lyrics. Genre and mood labels were picked by a person, so they are subjective.

## Algorithm Summary
Each song gets points: +2.0 if its genre matches, +1.0 if its mood matches, and up to +1.0 for how close its energy is to the listener's target (closer is better, in both directions). The songs are sorted by total score and the top K are shown, each with the reasons that earned its points.

## Observed Behavior / Biases
- Genre dominates. "Gym Hero" (intense pop) appears for "happy pop" users because the genre match is worth 2 points.
- A genre that is not in the catalog (k-pop) loses the biggest signal, and the system does not warn about it.
- Exact-text genre matching treats "pop" and "indie pop" as unrelated.
- Conflicting profiles (sad + high energy) are settled by genre and mood points, so the quiet folk song wins.
- Filter bubble risk: users always get their own genre first, and one artist can fill several slots (LoRoom twice in the Chill Lofi list, Neon Echo twice in the k-pop list).
- The Deep Intense Rock list has only one real rock song. Ranks 2 to 5 are energy-only matches from other genres.

## Evaluation Process
I tested five profiles: High-Energy Pop, Chill Lofi, Deep Intense Rock, and two edge cases (Sad but High Energy; a genre not in the catalog). I compared the top 5 lists with my own intuition, hand-checked scores, and ran one experiment (genre weight x0.5, energy weight x2).

- **Pop vs Lofi:** pop gets loud, fast songs; lofi gets quiet ones. Makes sense, since both genre and energy target changed.
- **Pop vs Rock:** both pull in high-energy songs; Gym Hero shows in both for different reasons (genre vs mood).
- **Lofi vs Rock:** no overlap at all, as expected.
- **Sad/High Energy vs the normal profiles:** it was the only list where energy and mood disagreed. The system chose a quiet song, because genre and mood points outweigh energy.
- **Surprise:** Gym Hero keeps showing up for happy-pop users. Plain explanation: it is labeled "pop" and has high energy, and the system gives the genre label a big bonus even when the mood is "intense," not "happy."
- **Experiment result:** more weight on energy moved Fuego Nocturno (latin, happy) above Gym Hero. It was different and, for happy users, slightly better.

## Intended Use and Non-Intended Use
**Intended:** a classroom demo of how a content-based recommender works, and for learning about scoring, ranking, and bias.
**Not intended:** real music apps, judging an artist's quality, or making decisions about real people. It has no user history and a tiny catalog.

## Ideas for Improvement
1. Use more features (valence, danceability, acousticness, tempo) and give partial credit for similar genres instead of exact match only.
2. Add a diversity penalty so one artist or genre cannot fill the top 5.
3. Warn when the user's genre is missing from the catalog, and support multiple favorite genres or moods.

## Personal Reflection
My biggest learning moment was seeing Gym Hero rank #2 for a "happy pop" profile. The math was doing exactly what I told it to do, yet the result felt wrong. A recommender can follow its rules perfectly and still give a weak answer, because the weights are my own choices.

AI helped me move fast by drafting the scoring function, suggesting weights, and proposing edge-case profiles. I still had to double-check it: I verified scores by hand (for example Sunrise City: 2.0 + 1.0 + 0.97 = 3.97) and ran the edge cases myself. The k-pop profile looked fine at first, and I only saw the missing genre signal after reading the reasons.

What surprised me is how three simple rules already feel like a real recommendation. The weaknesses only show up in lower ranks and edge cases.

Next, I would use more features, give partial credit for similar genres, and add an artist-diversity penalty.
