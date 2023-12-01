import argparse

from SongKeyGraphBuilder import SongKeyGraphBuilder


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

    print(graph.items())

if __name__ == "__main__":
    main()
