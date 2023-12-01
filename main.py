from dataclasses import dataclass
from typing import Dict, List
from collections import defaultdict
import argparse
import os
import librosa
import numpy as np

from constants import *


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
        self._create_graph()

    def _read_song_keys(self) -> None:
        for filename in os.listdir(self.song_dir):
            song_name = filename[:-4]  # TODO: strip the filename better (can't assume .mp3 extension e.g. ds_store)
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

            # NOTE: this is for debugging
            # bestcorr = max(key_dict.values())

            self.song_name_to_song_key[song_name] = alpha_num_key
            self.song_key_to_song_names[alpha_num_key].append(song_name)

    def _get_adjacent_keys(key: str) -> List[str]:
        maj, mi = int(key[:-1]), key[-1]
        maj_down = str((maj-1)%12) if maj != 1 else "12"
        maj_up = str((maj+1)%12) if maj != 11 else "12"
        mi_change = 'B' if mi == 'A' else 'A'
        return [key, str(maj)+mi_change, maj_down+mi, maj_up+mi]

    def _create_in_key_connections(self) -> None:
        for song_name, song_key in self.song_name_to_song_key.items():
            songs_in_key = [s for k in _get_adjacent_keys(song_key) for s in self.song_key_to_song_names[k]]
            songs_in_key.remove(song_name)
            for song in songs_in_key:
                if song_name not in self.graph[song].songs_in_key:
                    self.graph[song].songs_in_key.extend(song_name)
            self.graph[song_name].songs_in_key = songs_in_key

    def _create_graph(self) -> None:
        for song_name, song_key in self.song_name_to_song_key.items():
            self.graph[song_name] = self.Node(
                song_name=song_name,
                song_key=song_key,
                songs_in_key=[],
            )
        self._create_in_key_connections()


def main():
    parser=argparse.ArgumentParser(description="test script to find longest in-key song mix")
    parser.add_argument(
        "--song_dir",
        type=str,
        help="song directory to be analyzed for longest key matching segment",
    )
    args=parser.parse_args()

    graph = SongKeyGraphBuilder(args.song_dir)

if __name__ == "__main__":
    main()
