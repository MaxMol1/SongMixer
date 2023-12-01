import argparse
from typing import Dict, List, Tuple

from song_graph_builder import SongGraphBuilder


def traverseGraph(
    graph: Dict[str, SongGraphBuilder.Node],
    song_name_to_song_key: Dict[str, str],
) -> List[Tuple[str, str]]:
    longest_path = None
    
    # run traversal from every node
    for node in graph:
        path_stack = [[node]]
        finished_paths = []
        
        while path_stack:
            path = path_stack.pop(0)
            connections = graph[path[-1]].songs_in_key
            visited = set(path)

            if all([connection in visited for connection in connections]):
                finished_paths.append(path)

            for connection in connections:
                if connection not in visited:
                    new_path = path + [connection]
                    path_stack.append(new_path)

        longest_path = max(finished_paths, key=len)

    mixed_songs = {path: song_name_to_song_key[path] for path in longest_path}
    return mixed_songs

def main():
    parser=argparse.ArgumentParser(description="test script to find longest in-key song mix")
    parser.add_argument(
        "--song_dir",
        type=str,
        help="song directory to be analyzed for longest key matching segment",
    )
    args=parser.parse_args()

    graph_builder =SongGraphBuilder(args.song_dir)
    graph = graph_builder.getGraph()
    song_name_to_song_key_map = graph_builder.getSongNameToSongKey()
    mixed_songs = traverseGraph(graph, song_name_to_song_key_map)
    
    print(
        f"""
        --------------------------------------------------------------------
        The longest order of songs that can be mixed in-key from the options  
        provided in directory: {args.song_dir},
        is the following:
        --------------------------------------------------------------------\n
        """
    )
    for song, key in mixed_songs.items():
        print(song, "->", key)

if __name__ == "__main__":
    main()
