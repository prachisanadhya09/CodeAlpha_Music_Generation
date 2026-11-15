
import streamlit as st
import numpy as np
import tensorflow as tf
from music21 import stream, note, chord, tempo, instrument

st.set_page_config(page_title="AI Music Generator", page_icon="🎵")

st.title("🎵 AI Music Generation")
st.write("Generate new music using a trained LSTM model.")

@st.cache_resource
def load_model():
    model = tf.keras.models.load_model("music_model.keras")
    vocabulary = np.load("vocabulary.npy", allow_pickle=True).tolist()
    return model, vocabulary

if st.button("Generate AI Music"):
    try:
        model, vocabulary = load_model()

        sequence_length = model.input_shape[1]
        pattern = np.random.randint(
            0, len(vocabulary), size=sequence_length
        ).tolist()

        generated_notes = []

        for _ in range(64):
            prediction = model.predict(
                np.array([pattern]), verbose=0
            )[0]

            prediction = prediction / prediction.sum()
            index = np.random.choice(len(vocabulary), p=prediction)

            generated_notes.append(vocabulary[index])
            pattern = pattern[1:] + [index]

        music = stream.Stream()
        music.append(tempo.MetronomeMark(number=100))
        music.append(instrument.Piano())

        for item in generated_notes:
            if "." in item:
                music.append(chord.Chord(item.split(".")))
            else:
                music.append(note.Note(item))

        midi_path = music.write("midi", fp="generated_ai_music.mid")

        with open(midi_path, "rb") as file:
            midi_data = file.read()

        st.success("AI Music Generated Successfully!")

        st.download_button(
            "Download AI Music",
            data=midi_data,
            file_name="generated_ai_music.mid",
            mime="audio/midi"
        )

    except Exception as error:
        st.error(f"Error: {error}")

