import os
import whisper
import time
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
        for filename in filenames:
            # Check if the file is an mp4 file
            if filename.endswith('.mp4'):
                filepath = os.path.join(dirpath, filename)
                # Get the start time
                start_time = time.time()
                result = model.transcribe(filepath, fp16=False, verbose=True)

                # Print the file name.
                print(result['segments'][0]['text'])

                # Save the text to a new file in the same directory
                text_file = (filepath[:-4] + '.txt')

                # Write the text to the text file.
                with open(text_file, 'w') as f:
                    f.write(result["text"])

                # Print the elapsed time to convert the audio file.
                print("--- %s seconds ---" % (time.time() - start_time))
