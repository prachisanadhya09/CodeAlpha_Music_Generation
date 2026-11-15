
import streamlit as st
from music21 import stream, note, tempo, instrument

st.set_page_config(page_title="AI Music Generator", page_icon="🎵")

st.title("🎵 AI Music Generation")
st.write("Generate a simple piano melody using Python.")

def generate_music():
    melody = stream.Stream()
    melody.append(tempo.MetronomeMark(number=100))
    melody.append(instrument.Piano())

    notes = ["C4", "D4", "E4", "G4", "A4", "G4", "E4", "D4"]

    for pitch in notes:
        n = note.Note(pitch)
        n.quarterLength = 1
        melody.append(n)

    return melody

if st.button("Generate Music"):
    melody = generate_music()
    midi_file = melody.write("midi")

    with open(midi_file, "rb") as file:
        st.download_button(
            "Download MIDI Music",
            data=file,
            file_name="generated_music.mid",
            mime="audio/midi"
        )

    st.success("Your melody is ready!")
