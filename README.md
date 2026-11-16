# Music Recommender Simulation: VibeFinder 1.0

A small content-based music recommender. It scores 20 songs against a listener's taste profile, ranks them, and explains every recommendation.

## How The System Works

**Real-world recommenders.** Apps like Spotify and YouTube mix two ideas. *Collaborative filtering* uses other users' behavior (likes, skips, playlists, listening history): "people like you also liked this." *Content-based filtering* uses the song's own attributes (genre, mood, tempo, energy). Real systems combine both, plus huge amounts of behavior data, and run at massive scale.

**My version** is content-based only. It separates three things:
- **Input data:** the song catalog (`data/songs.csv`) with attributes for each song.
- **User preferences:** a taste profile dictionary (favorite genre, favorite mood, target energy).
- **Ranking:** a *scoring rule* judges one song; a *ranking rule* sorts all scored songs and keeps the top K.

**Song features:** id, title, artist, genre, mood, energy, tempo_bpm, valence, danceability, acousticness (20 songs).

**UserProfile features:** favorite_genre, favorite_mood, target_energy (0.0 to 1.0). The class also has `likes_acoustic`, which the scorer does not use yet.

### Algorithm Recipe
For each song:
1. **+2.0** if genre matches the user's favorite genre.
2. **+1.0** if mood matches the user's favorite mood.
3. **+0 to 1.0** for energy closeness: `1.0 - abs(song_energy - target_energy)`. Closer to the target earns more points, so being too high and too low are both penalized.

The scoring function returns the score plus a list of reasons. `recommend_songs` scores every song and sorts from highest to lowest.

```
User Prefs  ->  Loop over every song in CSV (score_song)  ->  Sort by score  ->  Top K + reasons
```

### Biases I expected
- Genre is worth the most points, so the system may ignore great songs that match the mood and energy but not the genre.
- Genre is an exact text match, so "pop" and "indie pop" count as totally different.
- With 20 songs, most genres have only one or two songs, so lists run out of good matches quickly.

## Run it
```
python -m src.main
```

## Sample Recommendation Output
Full terminal output (5 profiles, plus one weight experiment):

```text
Loaded songs: 20
Weights: {'genre': 2.0, 'mood': 1.0, 'energy': 1.0}

=== High-Energy Pop ===  {'genre': 'pop', 'mood': 'happy', 'energy': 0.85}
1. Sunrise City - Neon Echo [pop/happy]  score=3.97
   why: genre match (+2.0); mood match (+1.0); energy 0.82 vs target 0.85 (+0.97)
2. Gym Hero - Max Pulse [pop/intense]  score=2.92
   why: genre match (+2.0); energy 0.93 vs target 0.85 (+0.92)
3. Fuego Nocturno - Luz Marin [latin/happy]  score=2.00
   why: mood match (+1.0); energy 0.85 vs target 0.85 (+1.00)
4. Rooftop Lights - Indigo Parade [indie pop/happy]  score=1.91
   why: mood match (+1.0); energy 0.76 vs target 0.85 (+0.91)
5. Block Party - Ray Dillon [hip-hop/confident]  score=0.95
   why: energy 0.80 vs target 0.85 (+0.95)

=== Chill Lofi ===  {'genre': 'lofi', 'mood': 'chill', 'energy': 0.35}
1. Library Rain - Paper Lanterns [lofi/chill]  score=4.00
   why: genre match (+2.0); mood match (+1.0); energy 0.35 vs target 0.35 (+1.00)
2. Midnight Coding - LoRoom [lofi/chill]  score=3.93
   why: genre match (+2.0); mood match (+1.0); energy 0.42 vs target 0.35 (+0.93)
3. Focus Flow - LoRoom [lofi/focused]  score=2.95
   why: genre match (+2.0); energy 0.40 vs target 0.35 (+0.95)
4. Spacewalk Thoughts - Orbit Bloom [ambient/chill]  score=1.93
   why: mood match (+1.0); energy 0.28 vs target 0.35 (+0.93)
5. Coffee Shop Stories - Slow Stereo [jazz/relaxed]  score=0.98
   why: energy 0.37 vs target 0.35 (+0.98)

=== Deep Intense Rock ===  {'genre': 'rock', 'mood': 'intense', 'energy': 0.92}
1. Storm Runner - Voltline [rock/intense]  score=3.99
   why: genre match (+2.0); mood match (+1.0); energy 0.91 vs target 0.92 (+0.99)
2. Gym Hero - Max Pulse [pop/intense]  score=1.99
   why: mood match (+1.0); energy 0.93 vs target 0.92 (+0.99)
3. Bass Cathedral - Voltage [edm/euphoric]  score=0.96
   why: energy 0.96 vs target 0.92 (+0.96)
4. Wall of Fury - Black Anvil [metal/aggressive]  score=0.94
   why: energy 0.98 vs target 0.92 (+0.94)
5. Fuego Nocturno - Luz Marin [latin/happy]  score=0.93
   why: energy 0.85 vs target 0.92 (+0.93)

=== Edge: Sad but High Energy ===  {'genre': 'folk', 'mood': 'sad', 'energy': 0.9}
1. Campfire Letters - Pine and Sparrow [folk/sad]  score=3.38
   why: genre match (+2.0); mood match (+1.0); energy 0.28 vs target 0.90 (+0.38)
2. Slow Burn Blues - Delta Mae [blues/sad]  score=1.48
   why: mood match (+1.0); energy 0.38 vs target 0.90 (+0.48)
3. Storm Runner - Voltline [rock/intense]  score=0.99
   why: energy 0.91 vs target 0.90 (+0.99)
4. Gym Hero - Max Pulse [pop/intense]  score=0.97
   why: energy 0.93 vs target 0.90 (+0.97)
5. Fuego Nocturno - Luz Marin [latin/happy]  score=0.95
   why: energy 0.85 vs target 0.90 (+0.95)

=== Edge: Genre Not In Catalog ===  {'genre': 'k-pop', 'mood': 'happy', 'energy': 0.8}
1. Sunrise City - Neon Echo [pop/happy]  score=1.98
   why: mood match (+1.0); energy 0.82 vs target 0.80 (+0.98)
2. Rooftop Lights - Indigo Parade [indie pop/happy]  score=1.96
   why: mood match (+1.0); energy 0.76 vs target 0.80 (+0.96)
3. Fuego Nocturno - Luz Marin [latin/happy]  score=1.95
   why: mood match (+1.0); energy 0.85 vs target 0.80 (+0.95)
4. Block Party - Ray Dillon [hip-hop/confident]  score=1.00
   why: energy 0.80 vs target 0.80 (+1.00)
5. Night Drive Loop - Neon Echo [synthwave/moody]  score=0.95
   why: energy 0.75 vs target 0.80 (+0.95)

##### EXPERIMENT: genre x0.5, energy x2 #####

=== High-Energy Pop (experiment) ===  {'genre': 'pop', 'mood': 'happy', 'energy': 0.85}
1. Sunrise City - Neon Echo [pop/happy]  score=3.94
   why: genre match (+1.0); mood match (+1.0); energy 0.82 vs target 0.85 (+1.94)
2. Fuego Nocturno - Luz Marin [latin/happy]  score=3.00
   why: mood match (+1.0); energy 0.85 vs target 0.85 (+2.00)
3. Gym Hero - Max Pulse [pop/intense]  score=2.84
   why: genre match (+1.0); energy 0.93 vs target 0.85 (+1.84)
4. Rooftop Lights - Indigo Parade [indie pop/happy]  score=2.82
   why: mood match (+1.0); energy 0.76 vs target 0.85 (+1.82)
5. Block Party - Ray Dillon [hip-hop/confident]  score=1.90
   why: energy 0.80 vs target 0.85 (+1.90)

=== Edge: Sad but High Energy (experiment) ===  {'genre': 'folk', 'mood': 'sad', 'energy': 0.9}
1. Campfire Letters - Pine and Sparrow [folk/sad]  score=2.76
   why: genre match (+1.0); mood match (+1.0); energy 0.28 vs target 0.90 (+0.76)
2. Storm Runner - Voltline [rock/intense]  score=1.98
   why: energy 0.91 vs target 0.90 (+1.98)
3. Slow Burn Blues - Delta Mae [blues/sad]  score=1.96
   why: mood match (+1.0); energy 0.38 vs target 0.90 (+0.96)
4. Gym Hero - Max Pulse [pop/intense]  score=1.94
   why: energy 0.93 vs target 0.90 (+1.94)
5. Fuego Nocturno - Luz Marin [latin/happy]  score=1.90
   why: energy 0.85 vs target 0.90 (+1.90)
```

## Explanations (from the output above)
- **Sunrise City** for High-Energy Pop (#1, 3.97): genre is pop (+2.0), mood is happy (+1.0), and its energy 0.82 is very close to the 0.85 target (+0.97).
- **Storm Runner** for Deep Intense Rock (#1, 3.99): it matches rock, intense, and energy 0.91 vs 0.92. It is the only song that matches all three.
- **Gym Hero** for High-Energy Pop (#2, 2.92): it is pop (+2.0) with high energy (+0.92), but its mood is "intense," not "happy," so it gets no mood points. It ranks this high only because the genre bonus is so big.
- **Fuego Nocturno** for High-Energy Pop (#3, 2.00): no genre match, but happy mood (+1.0) and energy exactly 0.85 (+1.00).
- **Library Rain** for Chill Lofi (#1, 4.00): lofi (+2.0), chill (+1.0), energy exactly 0.35 (+1.00), a perfect score.

## Profile Comparisons
- **High-Energy Pop vs Chill Lofi:** pop picks are loud and fast (energy 0.76 to 0.93). Lofi picks are quiet (0.28 to 0.42). Genre and energy target both changed, so the whole list flipped. This makes sense.
- **High-Energy Pop vs Deep Intense Rock:** both want high energy, so Gym Hero appears in both lists. It earns its spot through genre for Pop and through the "intense" mood for Rock. Rock's ranks 3 to 5 (Bass Cathedral, Wall of Fury, Fuego Nocturno) match on energy only, because the catalog has just one rock song.
- **Chill Lofi vs Deep Intense Rock:** no overlap at all. Lofi stays near energy 0.3 to 0.4, Rock stays near 0.9 or higher. This is the expected result.
- **Sad but High Energy (edge case):** the profile contradicts itself. The quiet folk song "Campfire Letters" (energy 0.28) wins because genre + mood give it 3.0 points, which outweighs a poor energy score. The loud songs only fill the lower spots. The system let genre win the conflict.
- **Genre Not In Catalog (k-pop):** nobody gets genre points, so mood and energy decide. The results still look reasonable (happy, high energy) but the system silently lost its strongest signal. Note that Neon Echo shows up twice in the top 5.

## Experiment: Weight Shift (genre x0.5, energy x2)
For High-Energy Pop, **Fuego Nocturno** (latin, happy) jumped above **Gym Hero** (pop, intense), and **Rooftop Lights** moved almost level with Gym Hero (2.82 vs 2.84). For the Sad/High Energy profile, the loud rock song Storm Runner moved from #3 to #2, and Gym Hero stayed in the list. The results were different, and for the happy-pop user they were also *better*, because the intense workout song stopped beating a genuinely happy song. For the contradictory profile it is a mixed result: energy is respected more, but the quiet folk song still wins. So the change made the pop list more accurate and made the edge case only slightly less odd.

## Limitations and Bias
The system over-rewards genre. Gym Hero is an intense workout track, yet it ranks #2 for a "happy pop" listener only because its genre label is pop. Genres are exact text matches, so "indie pop" earns nothing for a "pop" fan even though the songs sound similar. The catalog has only 20 songs, and most genres have one or two songs, so every list falls back to energy-only matches by rank 3 to 5. Energy is also the only numeric feature in the score, so a loud sad song and a loud happy song look the same to the scorer.

## Reflection
My biggest learning moment was seeing Gym Hero rank #2 for a "happy pop" profile. The math was working exactly as I designed it, yet the result felt wrong. That showed me that a recommender can follow its rules perfectly and still give a weak answer, because the rules (a big genre bonus) were my choice. Changing the weights in the experiment made the list better, but it also showed me that every weight is an opinion.

AI helped me move fast. It drafted the scoring function, helped me think about the weights, and suggested edge-case profiles like "sad but high energy." But I had to double-check it. I verified the scores by hand for a few songs (for example, Sunrise City: 2.0 + 1.0 + 0.97 = 3.97) and I ran the edge cases myself to see what the system actually did, instead of trusting that it worked. The k-pop profile was a good example: the output looked fine, but I only saw the missing genre signal after I read the reasons.

What surprised me is that three simple rules (genre, mood, energy closeness) already feel like a real recommendation. The top result for each normal profile looked right to me. The weakness only shows up in the lower spots and in edge cases, which is probably true for real systems too.

Next, I would use valence, danceability, and acousticness in the score, give partial credit for similar genres like pop and indie pop, and add an artist-diversity penalty so the same artist can't fill several slots.
