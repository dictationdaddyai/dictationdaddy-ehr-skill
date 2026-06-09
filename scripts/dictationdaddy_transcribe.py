#!/usr/bin/env python3
import argparse
import json
import mimetypes
import os
import sys
import time
import urllib.error
import urllib.request
import uuid
from pathlib import Path


DEFAULT_ENDPOINT = "https://api.dictationdaddy.workers.dev"


def build_multipart(fields, files):
    boundary = f"----dictationdaddy-{uuid.uuid4().hex}"
    chunks = []

    for name, value in fields.items():
        if value is None:
            continue
        chunks.append(f"--{boundary}\r\n".encode())
        chunks.append(
            f'Content-Disposition: form-data; name="{name}"\r\n\r\n'.encode()
        )
        chunks.append(str(value).encode())
        chunks.append(b"\r\n")

    for name, path in files.items():
        file_path = Path(path)
        content_type = mimetypes.guess_type(file_path.name)[0] or "application/octet-stream"
        chunks.append(f"--{boundary}\r\n".encode())
        chunks.append(
            (
                f'Content-Disposition: form-data; name="{name}"; '
                f'filename="{file_path.name}"\r\n'
            ).encode()
        )
        chunks.append(f"Content-Type: {content_type}\r\n\r\n".encode())
        chunks.append(file_path.read_bytes())
        chunks.append(b"\r\n")

    chunks.append(f"--{boundary}--\r\n".encode())
    return boundary, b"".join(chunks)


def main():
    parser = argparse.ArgumentParser(
        description="Transcribe audio through the authenticated DictationDaddy API."
    )
    parser.add_argument("audio", help="Path to an audio file")
    parser.add_argument("--endpoint", default=os.getenv("DD_API_ENDPOINT", DEFAULT_ENDPOINT))
    parser.add_argument("--token", default=os.getenv("DD_FIREBASE_ID_TOKEN"))
    parser.add_argument("--context", default="Format as an EHR-ready clinical note.")
    parser.add_argument("--language", default="en")
    parser.add_argument("--model", default="medical")
    parser.add_argument("--source", default="claude-code-skill")
    parser.add_argument("--knowledge", default="{}")
    parser.add_argument("--keywords", default="[]")
    parser.add_argument("--extra", default='{"style":"formal"}')
    args = parser.parse_args()

    audio_path = Path(args.audio)
    if not audio_path.exists():
        print(json.dumps({"success": False, "error": f"audio file not found: {audio_path}"}))
        return 2

    if not args.token:
        print(json.dumps({
            "success": False,
            "error": "DD_FIREBASE_ID_TOKEN is required for authenticated DictationDaddy API use."
        }))
        return 2

    fields = {
        "sessionId": str(int(time.time() * 1000)),
        "source": args.source,
        "model": args.model,
        "context": args.context,
        "language": args.language,
        "knowledge": args.knowledge,
        "keywords": args.keywords,
        "extra": args.extra,
    }
    boundary, body = build_multipart(fields, {"audio": audio_path})

    req = urllib.request.Request(
        args.endpoint,
        data=body,
        method="POST",
        headers={
            "Authorization": f"Bearer {args.token}",
            "Content-Type": f"multipart/form-data; boundary={boundary}",
            "Accept": "application/json",
            "User-Agent": "dictationdaddy-ehr-skill/1.0",
        },
    )

    try:
        with urllib.request.urlopen(req, timeout=120) as res:
            sys.stdout.write(res.read().decode("utf-8"))
            sys.stdout.write("\n")
            return 0
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        print(json.dumps({"success": False, "status": exc.code, "error": body}))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

