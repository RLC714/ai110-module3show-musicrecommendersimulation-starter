import csv
from dataclasses import dataclass
from typing import Dict, List, Tuple

# Algorithm recipe: points for each rule. Change these to run experiments.
WEIGHTS = {"genre": 2.0, "mood": 1.0, "energy": 1.0}


@dataclass
class Song:
    """A song and its audio attributes."""
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


@dataclass
class UserProfile:
    """A listener's taste profile."""
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool


def load_songs(csv_path: str) -> List[Dict]:
    """Read songs.csv and return dicts with numeric fields converted."""
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            row["id"] = int(row["id"])
            for key in ("energy", "tempo_bpm", "valence", "danceability", "acousticness"):
                row[key] = float(row[key])
            songs.append(row)
    return songs


def score_song(user_prefs: Dict, song: Dict, weights: Dict = None) -> Tuple[float, List[str]]:
    """Score one song against user prefs; return (score, list of reasons)."""
    w = weights or WEIGHTS
    score, reasons = 0.0, []
    if song["genre"] == user_prefs["genre"]:
        score += w["genre"]
        reasons.append(f"genre match (+{w['genre']:.1f})")
    if song["mood"] == user_prefs["mood"]:
        score += w["mood"]
        reasons.append(f"mood match (+{w['mood']:.1f})")
    closeness = 1.0 - abs(song["energy"] - user_prefs["energy"])
    pts = w["energy"] * closeness
    score += pts
    reasons.append(f"energy {song['energy']:.2f} vs target {user_prefs['energy']:.2f} (+{pts:.2f})")
    return round(score, 2), reasons


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5, weights: Dict = None):
    """Score every song and return the top k as (song, score, reasons)."""
    scored = []
    for song in songs:
        s, reasons = score_song(user_prefs, song, weights)
        scored.append((song, s, reasons))
    return sorted(scored, key=lambda t: t[1], reverse=True)[:k]


class Recommender:
    """OOP wrapper around the scoring logic."""

    def __init__(self, songs: List[Song]):
        self.songs = songs

    def _prefs(self, user: UserProfile) -> Dict:
        return {"genre": user.favorite_genre, "mood": user.favorite_mood, "energy": user.target_energy}

    def _song_dict(self, s: Song) -> Dict:
        return s.__dict__

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return the top k Song objects for a user."""
        prefs = self._prefs(user)
        ranked = sorted(self.songs, key=lambda s: score_song(prefs, self._song_dict(s))[0], reverse=True)
        return ranked[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Return a plain-text reason string for one song."""
        _, reasons = score_song(self._prefs(user), self._song_dict(song))
        return "; ".join(reasons)
