import os
import sys
from pathlib import Path

# Optional: prefer GPU if available
try:
    import torch
except ImportError:
    torch = None

import whisper


def format_timestamp(seconds: float, always_include_hours: bool = False) -> str:
    """
    Format seconds like Whisper's console output:
      MM:SS.mmm  (if under 1 hour)
      HH:MM:SS.mmm (if >= 1 hour or always_include_hours=True)
    """
    if seconds is None:
        return "00:00.000"
    total_ms = int(round(seconds * 1000))
    hours, rem_ms = divmod(total_ms, 3600 * 1000)
    minutes, rem_ms = divmod(rem_ms, 60 * 1000)
    secs, ms = divmod(rem_ms, 1000)

    if always_include_hours or hours > 0:
        return f"{hours:02d}:{minutes:02d}:{secs:02d}.{ms:03d}"
    else:
        return f"{minutes:02d}:{secs:02d}.{ms:03d}"


def find_mp4s(root: Path):
    """Yield all .mp4 files under root (case-insensitive), sorted for stable output."""
    for dirpath, _, filenames in os.walk(root):
        filenames.sort()
        for fn in filenames:
            if fn.lower().endswith(".mp4"):
                yield Path(dirpath) / fn


def main():
    directory = input("What is the path to the directory? ").strip().strip('"').strip("'")
    if not directory:
        print("No directory provided. Exiting.")
        sys.exit(1)

    root = Path(directory)
    if not root.is_dir():
        print(f"Path is not a directory or does not exist: {root}")
        sys.exit(1)

    # Collect files first so we can report count
    mp4_files = list(find_mp4s(root))
    print("Getting the number of files to transcribe...")
    print("Number of files:", len(mp4_files))

    # Pick device via PyTorch if available
    device = "cuda" if (torch is not None and torch.cuda.is_available()) else "cpu"

    print("Loading whisper model...")
    model = whisper.load_model("medium.en", device=device)
    print(f"Whisper model loaded on {device}.")

    # fp16 only on GPU
    use_fp16 = device == "cuda"

    # Loop and transcribe
    for filepath in mp4_files:
        print(filepath.name)
        try:
            result = model.transcribe(str(filepath), fp16=use_fp16, verbose=True)
        except Exception as e:
            print(f"Error transcribing '{filepath}': {e}")
            continue

        # Output paths
        text_file_1 = filepath.with_suffix(".txt")
        text_file_2 = filepath.with_name(filepath.stem + "_timestamps.txt")

        try:
            # Full transcription
            with open(text_file_1, "w", encoding="utf-8") as f1:
                f1.write(result.get("text", ""))

            # Timestamped segments in Whisper console format
            with open(text_file_2, "w", encoding="utf-8") as f2:
                for segment in result.get("segments", []):
                    start = segment.get("start", 0.0)
                    end = segment.get("end", 0.0)
                    text = (segment.get("text") or "").strip()
                    f2.write(f"[{format_timestamp(start)} --> {format_timestamp(end)}]  {text}\n")

            print(f"Saved transcription to {text_file_1} and {text_file_2}")

        except Exception as e:
            print(f"Error writing to file for '{filepath}': {e}")


if __name__ == "__main__":
    main()
