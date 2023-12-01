# SongMixer

This is a practical little tool for finding the longest order of songs that can
be mixed harmoniously (mixed in-key) from a directory of mp3 files.

The key of a song is extracted using the Krumhansl-Schmuckler key-finding
algorithm, and the script  then finds the "optimal" set list using a 
breadth first traversal on a graph built from the songs and their in-key
connections.

## Limitations

In some cases, the Krumhansl-Schmuckler algorithm results may not be accurate/consistent
with other key finding algorithms, such as those used by popular DJ software like Rekordbox.
