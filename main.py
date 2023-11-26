from dataclasses import dataclass
from typing import Dict, List
from collections import defaultdict
import argparse
import os
import keyfinder  # TODO: fix this


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
        self._parse_songs_for_key()
        self._create_graph()

    def _parse_songs_for_key(self):
        for filename in os.listdir(self.song_dir):
            song_name = filename[:-4]  # TODO: strip the filename better
            key_obj = keyfinder.key(song_name)
            key = key_obj.open_key()  # NOTE: make sure this is a str
            self.song_name_to_song_key[song_name] = key
            self.song_key_to_song_names[key].append(song_name)

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
    parser.add_argument("song_dir")
    args=parser.parse_args()
    graph = SongKeyGraphBuilder(args.song_dir)
    # TODO: find path

if __name__ == "__main__":
    main()
