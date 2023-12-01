import argparse
from ast import Dict, List, Tuple
from lib2to3.pytree import Node

from SongKeyGraphBuilder import SongKeyGraphBuilder


def traverseGraph(graph: Dict[str, Node]) -> List[Tuple[str, str]]:
    pass

def main():
    parser=argparse.ArgumentParser(description="test script to find longest in-key song mix")
    parser.add_argument(
        "--song_dir",
        type=str,
        help="song directory to be analyzed for longest key matching segment",
    )
    args=parser.parse_args()

    graph_builder =SongKeyGraphBuilder(args.song_dir)
    graph = graph_builder.getGraph()
    mixed_songs = traverseGraph(graph)
    
    print(
        f"""
        --------------------------------------------------------------------
        The longest order of songs that can be mixed in-key from the options  
        provided in {args.song_dir} is the following:
        --------------------------------------------------------------------\n
        """
    )
    for song in mixed_songs:
        print(song[0], "->", song[1])

if __name__ == "__main__":
    main()
