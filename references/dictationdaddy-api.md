# DictationDaddy Authenticated API Flow

Use this only when the user explicitly asks to send audio through DictationDaddy or has configured DictationDaddy credentials in the local environment.

## Claude Code Terminal Flow

The practical Claude Code terminal flow is:

```bash
export DD_FIREBASE_ID_TOKEN="short-lived-firebase-id-token"

python ~/.claude/skills/dictationdaddy-ehr-report/scripts/record_audio.py \
  --duration 90 \
  --output ./visit-note.wav

python ~/.claude/skills/dictationdaddy-ehr-report/scripts/dictationdaddy_transcribe.py ./visit-note.wav
```

Then ask Claude Code:

```text
Use the DictationDaddy EHR report skill. Format the returned transcript as a SOAP note.
```

The recording helper is intentionally local and user-initiated. It should print the command it is using and save an audio file; it should not upload anything by itself.

## Local Browser Session

For users who want recording and history in a browser, use the bundled static page:

```bash
cd ~/.claude/skills/dictationdaddy-ehr-report
python3 -m http.server 8765
```

Open `http://localhost:8765/web-recorder/`.

The page:

- records audio through `navigator.mediaDevices.getUserMedia`
- requires the user to paste or provide a short-lived Firebase ID token
- sends audio to `https://api.dictationdaddy.workers.dev` only after `Send to DictationDaddy`
- displays the raw returned transcript
- stores local transcript history in browser `localStorage`

Use the returned transcript as source material for the Claude Code EHR formatting pass.

## Recording Model

The skill usually expects an audio file that already exists. If the user wants terminal recording, use the helper only when the user explicitly asks.

Recommended capture paths:

- DictationDaddy app records the audio and provides the transcript or file.
- The user records with their OS recorder and passes the saved file path.
- Another trusted local recorder creates a `.webm`, `.wav`, `.mp3`, `.m4a`, or similar file.
- The user runs `scripts/record_audio.py`, which delegates to a local recording command such as `sox`/`rec`, `arecord`, or `ffmpeg`.

After recording, this skill can upload that file to the authenticated DictationDaddy endpoint and then format the returned raw transcript.

## Production Endpoint

DictationDaddy desktop currently sends audio to:

```text
https://api.dictationdaddy.workers.dev
```

Authentication follows the app flow:

- Get the user's Firebase ID token from their authenticated DictationDaddy session.
- Send it as `Authorization: Bearer <firebase-id-token>`.
- Tokens are short-lived; refresh from Firebase rather than storing them permanently.

Do not ask the user to paste long-lived secrets. Prefer an environment variable such as `DD_FIREBASE_ID_TOKEN` or an app-provided auth handoff.

## Validation, Payment, and Entitlements

Do not reimplement payment, license, subscription, quota, or entitlement logic inside this skill.

The skill is a thin client:

1. Use the user's existing DictationDaddy authentication state.
2. Send the request to the DictationDaddy endpoint.
3. Let the backend validate Firebase auth, subscription/payment status, usage limits, team membership, BYOK/LTD settings, and any server-side policy.
4. If the backend rejects the request, surface the error clearly and ask the user to resolve it in DictationDaddy.

This keeps billing/security behavior consistent with the main app and avoids a second source of truth in Claude Code.

## Multipart Fields

Send a `POST` multipart form request with:

- `audio`: binary audio file that has already been recorded
- `sessionId`: unique client-side session id
- `source`: use `claude-code-skill`
- `model`: one of `medical`, `enhanced`, `standard`, `instant`, or `ultra`; default to `medical` for EHR use
- `context`: request raw transcription by default; do not ask the API to produce the final EHR note unless the user explicitly wants server-side formatting
- `language`: default `en`
- `knowledge`: optional JSON object
- `keywords`: optional JSON array
- `extra`: optional JSON object, for example `{ "style": "formal" }`

The response contains `result`, and may include `html`, `lastDocId`, `audioUrl`, `promptLogs`, `metrics`, and metadata. Treat `result` as the raw transcript/source draft, then use Claude Code and this skill to produce the final EHR-ready report.

## Helper Script

To transcribe an existing audio file:

```bash
DD_FIREBASE_ID_TOKEN="$TOKEN" \
python scripts/dictationdaddy_transcribe.py ./audio.webm \
  --context "Transcribe this audio as accurately as possible. Preserve dictated wording and uncertainty. Do not format as a final note." \
  --model medical
```

The script prints JSON. Use the `result` field as the transcript/source draft, then apply the main skill's EHR safety and formatting pass before final output.

To record first, if local recording tools are installed:

```bash
python scripts/record_audio.py --duration 90 --output ./visit-note.wav
```

Then pass the output file to `dictationdaddy_transcribe.py`.

## Failure Handling

- `401`: token missing, expired, or invalid. Ask the user to authenticate through DictationDaddy again.
- `400`: missing audio or invalid model. Check multipart fields.
- Payment, quota, subscription, or entitlement error: do not bypass it; tell the user to open DictationDaddy and resolve billing/subscription/access there.
- Network failure: do not retry indefinitely; tell the user the upload failed and ask for the transcript.
