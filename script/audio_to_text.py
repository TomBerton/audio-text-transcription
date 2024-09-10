import os
import whisper
from pathlib import Path


directory = input("What is the path to the directory? ")

# Load the medium model
print("Loading whisper model...")
model = whisper.load_model("medium.en")
print("Whisper model loaded.")

# Get the number of wav files in the root folder and its sub-folders
print("Getting the number of files to transcribe...")
num_files = sum(1 for dirpath, dirnames, filenames in os.walk(directory) for filename in filenames if filename.endswith(".mp4"))
print("Number of files: ", num_files)

# Loop through all files in the directory
for dirpath, dirnames, filenames in os.walk(directory):
    # Sort the filenames alphabetically
    filenames.sort()
    for filename in filenames:
        # Check if the file is an mp4 file
        if filename.endswith('.mp4'):
            print(filename)
            filepath = os.path.join(dirpath, filename)
            # Transcribe the audio
            result = model.transcribe(filepath, fp16=False, verbose=True)

            # Define paths for two text files
            text_file_1 = filepath[:-4] + '.txt'
            text_file_2 = filepath[:-4] + '_timestamps.txt'

            try:
                # Write full transcription to text_file_1
                with open(text_file_1, 'w') as f1:
                    f1.write(result["text"])

                # Write timestamped segments to text_file_2
                with open(text_file_2, 'w') as f2:
                    for segment in result['segments']:
                        start = segment['start']
                        end = segment['end']
                        text = segment['text']
                        f2.write(f"[{start} - {end}] {text}\n")

                print(f"Saved transcription to {text_file_1} and {text_file_2}")

            except Exception as e:
                print(f"Error writing to file: {e}")
