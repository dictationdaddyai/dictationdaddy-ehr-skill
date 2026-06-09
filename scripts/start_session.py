#!/usr/bin/env python3
import argparse
import functools
import http.server
import socketserver
import sys
import threading
import webbrowser
from pathlib import Path


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        return


def main():
    parser = argparse.ArgumentParser(
        description="Start the local DictationDaddy EHR browser recorder session."
    )
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument("--no-open", action="store_true", help="Do not open the browser")
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    handler = functools.partial(QuietHandler, directory=str(root))

    with socketserver.TCPServer(("127.0.0.1", args.port), handler) as httpd:
        url = f"http://127.0.0.1:{args.port}/web-recorder/"
        print(url)
        print("Press Ctrl+C to stop the local recorder session.", file=sys.stderr)
        if not args.no_open:
            threading.Timer(0.25, lambda: webbrowser.open(url)).start()
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nStopped.", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
