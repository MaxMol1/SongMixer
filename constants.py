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

# used by the Krumhansl-Schmuckler key-finding algorithm
MAJOR_PROFILE = [6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88]
MINOR_PROFILE = [6.33, 2.68, 3.52, 5.38, 2.60, 3.53, 2.54, 4.75, 3.98, 2.69, 3.34, 3.17]
