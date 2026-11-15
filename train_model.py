
import os
import glob
import numpy as np
import tensorflow as tf
from music21 import converter, note, chord

# Folder containing MIDI training files
DATA_FOLDER = "midi_data"
SEQUENCE_LENGTH = 8

def extract_notes():
    notes = []

    files = glob.glob(os.path.join(DATA_FOLDER, "*.mid"))
    files += glob.glob(os.path.join(DATA_FOLDER, "*.midi"))

    if not files:
        raise FileNotFoundError(
            "No MIDI files found. Add MIDI files to the midi_data folder."
        )

    for file in files:
        try:
            midi = converter.parse(file)

            for element in midi.flatten().notes:
                if isinstance(element, note.Note):
                    notes.append(str(element.pitch))

                elif isinstance(element, chord.Chord):
                    notes.append(
                        ".".join(str(p) for p in element.pitches)
                    )

        except Exception as error:
            print("Could not read:", file, error)

    return notes


def train_model():
    notes = extract_notes()

    if len(notes) <= SEQUENCE_LENGTH:
        raise ValueError("Not enough notes in MIDI dataset.")

    vocabulary = sorted(set(notes))
    note_to_int = {n: i for i, n in enumerate(vocabulary)}

    sequences = []
    targets = []

    for i in range(len(notes) - SEQUENCE_LENGTH):
        sequences.append([
            note_to_int[n]
            for n in notes[i:i + SEQUENCE_LENGTH]
        ])
        targets.append(note_to_int[notes[i + SEQUENCE_LENGTH]])

    X = np.array(sequences)
    y = np.array(targets)

    model = tf.keras.Sequential([
        tf.keras.layers.Input(shape=(SEQUENCE_LENGTH,)),
        tf.keras.layers.Embedding(len(vocabulary), 64),
        tf.keras.layers.LSTM(128),
        tf.keras.layers.Dense(len(vocabulary), activation="softmax")
    ])

    model.compile(
        optimizer="adam",
        loss="sparse_categorical_crossentropy"
    )

    model.fit(X, y, epochs=20, batch_size=32)

    model.save("music_model.keras")
    np.save("vocabulary.npy", np.array(vocabulary))

    print("LSTM model trained and saved successfully!")


if __name__ == "__main__":
    train_model()
