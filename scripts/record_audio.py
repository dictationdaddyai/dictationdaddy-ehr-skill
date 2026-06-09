#!/usr/bin/env python3
import argparse
import shutil
import subprocess
import sys
from pathlib import Path


def command_for(output: Path, duration: int):
    suffix = output.suffix.lower()

    if shutil.which("rec"):
        # SoX. Works on macOS/Linux when microphone permissions are granted.
        return ["rec", str(output), "trim", "0", str(duration)]

    if shutil.which("arecord"):
        # ALSA/Linux. WAV is the safest output format.
        return ["arecord", "-d", str(duration), "-f", "cd", str(output)]

    if shutil.which("ffmpeg"):
        if sys.platform == "darwin":
            # Default macOS audio input. Users may need to grant terminal mic permission.
            return [
                "ffmpeg",
                "-y",
                "-f",
                "avfoundation",
                "-i",
                ":0",
                "-t",
                str(duration),
                str(output),
            ]
        if sys.platform.startswith("linux"):
            # PulseAudio default input.
            return [
                "ffmpeg",
                "-y",
                "-f",
                "pulse",
                "-i",
                "default",
                "-t",
                str(duration),
                str(output),
            ]

    if sys.platform == "darwin" and shutil.which("afrecord"):
        # Native macOS recorder. Use CAF if caller did not choose a clear extension.
        if suffix not in {".caf", ".wav", ".aiff", ".m4a"}:
            output = output.with_suffix(".caf")
        return ["afrecord", "-d", str(duration), str(output)]

    return None


def main():
    parser = argparse.ArgumentParser(
        description="Record microphone audio locally for DictationDaddy EHR skill use."
    )
    parser.add_argument("--duration", type=int, default=60, help="Recording duration in seconds")
    parser.add_argument("--output", default="dictationdaddy-note.wav", help="Output audio path")
    args = parser.parse_args()

    if args.duration <= 0:
        print("duration must be greater than zero", file=sys.stderr)
        return 2

    output = Path(args.output).expanduser().resolve()
    output.parent.mkdir(parents=True, exist_ok=True)

    cmd = command_for(output, args.duration)
    if not cmd:
        print(
            "No supported local recorder found. Install SoX (`rec`), ALSA `arecord`, "
            "or ffmpeg, or record with DictationDaddy/your OS recorder and pass the saved file.",
            file=sys.stderr,
        )
        return 1

    print("Recording locally. Command:", " ".join(cmd), file=sys.stderr)
    print(f"Saving to: {output}", file=sys.stderr)
    completed = subprocess.run(cmd, check=False)
    if completed.returncode != 0:
        return completed.returncode
    print(str(output))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
