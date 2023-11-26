import speech_recognition as sr
from pydub import AudioSegment

def transcribe_large_audio(audio_file_path, chunk_duration_ms=60000):
    recognizer = sr.Recognizer()

    # Load the audio file using pydub
    audio = AudioSegment.from_wav(audio_file_path)

    # Calculate the number of chunks based on the specified duration
    num_chunks = len(audio) // chunk_duration_ms + 1

    transcriptions = []

    for i in range(num_chunks):
        # Calculate start and end time for each chunk
        start_time = i * chunk_duration_ms
        end_time = (i + 1) * chunk_duration_ms

        # Extract the chunk
        chunk = audio[start_time:end_time]

        # Export the chunk to a temporary WAV file
        chunk.export("temp_chunk.wav", format="wav")

        # Convert each chunk to audio data
        with sr.AudioFile("temp_chunk.wav") as chunk_audio_file:
            chunk_audio_data = recognizer.record(chunk_audio_file)

        try:
            print("Transcribing chunk {}.".format(i))
            # Use Google Web Speech API for transcription
            text = recognizer.recognize_google(chunk_audio_data, language="cs-CZ")
            transcriptions.append(text)

        except sr.UnknownValueError:
            print("Speech Recognition could not understand chunk {}.".format(i))
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))

    # Print the combined transcript
    print("Transcript: {}".format(" ".join(transcriptions)))

# Example usage
transcribe_large_audio("C:/Users/actul/Documents/TEST/output_audio.wav")
