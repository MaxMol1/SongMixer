from dataclasses import dataclass
from typing import Dict, List
from collections import defaultdict
import argparse
import os
import librosa
import numpy as np

PITCHES = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']
KEYS = [PITCHES[i] + ' major' for i in range(12)] + [PITCHES[i] + ' minor' for i in range(12)]

KEY_TO_ALPHANUMERIC = {
    "B major": "1B",
    "F# major": "2B",
    "C# major": "3B", # D flat
    "G# major": "4B", # Ab flat
    "D# major": "5B", # Eb flat
    "A# major": "6B", # Bb flat
    "F major": "7B",
    "C major": "8B",
    "G major": "9B",
    "D major": "10B",
    "A major": "11B",
    "E major": "12B",
    "G# minor": "1A", # Ab flat
    "D# minor": "2A", # Eb flat
    "A# minor": "3A", # Bb flat
    "F minor": "4A",
    "C minor": "5A",
    "G minor": "6A",
    "D minor": "7A",
    "A minor": "8A",
    "E minor": "9A",
    "B minor": "10A",
    "F# minor": "11A",
    "C# minor": "12A", # Db flat
}

# use of the Krumhansl-Schmuckler key-finding algorithm
MAJOR_PROFILE = [6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88]
MINOR_PROFILE = [6.33, 2.68, 3.52, 5.38, 2.60, 3.53, 2.54, 4.75, 3.98, 2.69, 3.34, 3.17]


class SongKeyGraphBuilder():
    @dataclass
    class Node():
        song_name: str  # key
        song_key: str  # value
        songs_in_key: List[str]  # connections
    
    song_name_to_song_key: Dict[str, str] = {}
    song_key_to_song_names = defaultdict(list)
    graph: Dict[str, Node] = {}

    def __init__(self, song_dir: str) -> None:
        self.song_dir = song_dir
        self._read_song_keys()
        # self._create_graph()

    def _read_song_keys(self):
        for filename in os.listdir(self.song_dir):
            song_name = filename[:-4]  # TODO: strip the filename better
            song_path = os.path.join(self.song_dir, filename)

            # load file into chromograph
            y, sr = librosa.load(song_path)
            chromograph = librosa.feature.chroma_cqt(y=y, sr=sr, bins_per_octave=24)
            
            # dictionary relating pitch names to the associated intensity in the song
            keyfreqs = {PITCHES[i]: np.sum(chromograph[i]) for i in range(12)} 

            # find correlations between the amount of each pitch class in the time interval
            major_key_corrs = []
            minor_key_corrs = []
            for i in range(12):
                key_test = [keyfreqs.get(PITCHES[(i+m)%12]) for m in range(12)]
                major_key_corrs.append(round(np.corrcoef(MAJOR_PROFILE, key_test)[1,0], 3))
                minor_key_corrs.append(round(np.corrcoef(MINOR_PROFILE, key_test)[1,0], 3))

            # names of all major and minor keys
            key_dict = {**{KEYS[i]: major_key_corrs[i] for i in range(12)}, 
                        **{KEYS[i+12]: minor_key_corrs[i] for i in range(12)}}
            
            # this attribute represents the key determined by the algorithm
            key = max(key_dict, key=key_dict.get)
            alpha_num_key = KEY_TO_ALPHANUMERIC[key]
            # bestcorr = max(key_dict.values()) # NOTE: this is for debugging

            self.song_name_to_song_key[song_name] = alpha_num_key
            self.song_key_to_song_names[alpha_num_key].append(song_name)

    def _create_graph(self):
        for song_name, song_key in self.song_name_to_song_key.items():
            song_node = self.Node(
                song_name=song_name,
                song_key=song_key,
            )
            # TODO: generate this, how to deal with wrapparound?
            adj_keys = [-1, +1, +0, -0]
            songs_in_key = [s for k in adj_keys for s in self.key_to_songs[k]]
            for song in songs_in_key:
                self.graph[song].songs_in_key += song
            song_node.songs_in_key = songs_in_key
            self.graph[song_name] = song_node


def main():
    parser=argparse.ArgumentParser(description="test script to find longest in-key song mix")
    parser.add_argument(
        "--song_dir",
        type=str,
        help="song directory to be analyzed for longest key matching segment",
    )
    args=parser.parse_args()

    graph = SongKeyGraphBuilder(args.song_dir)
    # TODO: find path

if __name__ == "__main__":
    main()
