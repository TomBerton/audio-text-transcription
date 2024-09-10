# audio-text-transcription

This repository will transcribe audio files or audio in video files to text using [Whisper](https://openai.com/research/whisper).

## Setup

1. Create a Python virtual environment with Python 3.9.

    ```shell
    python3 -m venv audio_transcribe
    ```

2. I activated the environment.

    ```shell
    source audio_transcribe/bin/activate
    ```

    * To deactivate the environment, type and run `deactivate`.

3. I installed Whisper and the required dependencies using the following steps as mentioned on the [Whisper GitHub repo](https://github.com/openai/whisper)

    * `pip install -U openai-whisper`
    * `brew install ffmpeg`
    * `pip install setuptools-rust`

## Execution

1. From the command line, run the [`audio_to_text.py`](script/audio_to_text.py) file:

    * `python audio_to_text.py`

2. You'll be prompted to provide the path to the directory containing the `.mp4`, `.mp3`, or .`wav` files.

    * `"What is the path to the directory? "`

3. Paste in the path to the directory and press enter.

4. In Python script, I have the parameter, `verbose` set to `True` (`verbose=True`) to output timestamps of the file being transcribed along with the transcription.

    ![example of a transcription](Images/audio_transcription.png)

    * The first time you run the script the model will download, which may take a few minutes.

## Pros

* There is no API key needed.
* There are few dependencies.
* Can transcribe from a language to English.

## Cons

* Cannot transcribed English to a another language.

## Comparing transcription models for speed.

* I compared the `tiny.en`, `base.en`, `small.en`, and `medium.en` models.

* The two videos that were transcribed are:
  * `Platform_and_Tools.mp4`, 9.5 MB
  * `Introduction_to_CI_CD.mp4`, 5.4 MB.

* Transcription times for each file using each model.

  | Model  | 9.5 MB  | 5.4 MB  |
  |---|---|---|
  | `tiny.en` |  11 seconds |  4 seconds |
  | `base.en`  | 18 seconds |  7 seconds |
  | `small.en`  | 51 seconds |  19 seconds |
  | `medium.en`  |  181 seconds |  165 seconds |

  * The transcribed audio files are [here](/text_files/transcribed_files/).

  * The text files that are downloaded from the edX course are [here](/text_files/original_files/).
