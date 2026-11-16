from src.recommender import load_songs, recommend_songs, WEIGHTS

PROFILES = {
    "High-Energy Pop": {"genre": "pop", "mood": "happy", "energy": 0.85},
    "Chill Lofi": {"genre": "lofi", "mood": "chill", "energy": 0.35},
    "Deep Intense Rock": {"genre": "rock", "mood": "intense", "energy": 0.92},
    "Edge: Sad but High Energy": {"genre": "folk", "mood": "sad", "energy": 0.90},
    "Edge: Genre Not In Catalog": {"genre": "k-pop", "mood": "happy", "energy": 0.80},
}
# Experiment: double energy, halve genre
EXPERIMENT = {"genre": 1.0, "mood": 1.0, "energy": 2.0}


def show(name, prefs, songs, weights=None, k=5):
    print(f"\n=== {name} ===  {prefs}")
    for i, (song, score, reasons) in enumerate(recommend_songs(prefs, songs, k, weights), 1):
        print(f"{i}. {song['title']} - {song['artist']} [{song['genre']}/{song['mood']}]  score={score:.2f}")
        print(f"   why: {'; '.join(reasons)}")


def main():
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")
    print(f"Weights: {WEIGHTS}")
    for name, prefs in PROFILES.items():
        show(name, prefs, songs)
    print("\n##### EXPERIMENT: genre x0.5, energy x2 #####")
    show("High-Energy Pop (experiment)", PROFILES["High-Energy Pop"], songs, EXPERIMENT)
    show("Edge: Sad but High Energy (experiment)", PROFILES["Edge: Sad but High Energy"], songs, EXPERIMENT)


if __name__ == "__main__":
    main()
