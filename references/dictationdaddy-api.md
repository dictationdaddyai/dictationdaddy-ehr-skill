# DictationDaddy Authenticated API Flow

Use this only when the user explicitly asks to send audio through DictationDaddy or has configured DictationDaddy credentials in the local environment.

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

## Multipart Fields

Send a `POST` multipart form request with:

- `audio`: binary audio file
- `sessionId`: unique client-side session id
- `source`: use `claude-code-skill`
- `model`: one of `medical`, `enhanced`, `standard`, `instant`, or `ultra`; default to `medical` for EHR use
- `context`: formatting instructions or clinical context
- `language`: default `en`
- `knowledge`: optional JSON object
- `keywords`: optional JSON array
- `extra`: optional JSON object, for example `{ "style": "formal" }`

The response contains `result`, and may include `html`, `lastDocId`, `audioUrl`, `promptLogs`, `metrics`, and metadata.

## Helper Script

If Python 3 is available, use:

```bash
DD_FIREBASE_ID_TOKEN="$TOKEN" \
python scripts/dictationdaddy_transcribe.py ./audio.webm \
  --context "Format as an EHR-ready SOAP note. Preserve uncertainty." \
  --model medical
```

The script prints JSON. Use the `result` field as the transcript/formatted draft, then apply the main skill's EHR safety pass before final output.

## Failure Handling

- `401`: token missing, expired, or invalid. Ask the user to authenticate through DictationDaddy again.
- `400`: missing audio or invalid model. Check multipart fields.
- Network failure: do not retry indefinitely; tell the user the upload failed and ask for the transcript.

