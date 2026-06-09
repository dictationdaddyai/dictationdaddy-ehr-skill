# DictationDaddy EHR Report Skill

Claude Code skill for turning DictationDaddy transcripts, clinician dictation, or locally transcribed audio into EHR-ready reports.

## Install

Clone this repo into your Claude skills directory:

```bash
mkdir -p ~/.claude/skills
git clone https://github.com/dictationdaddyai/dictationdaddy-ehr-skill.git ~/.claude/skills/dictationdaddy-ehr-report
```

Then use Claude Code with a prompt such as:

```text
Use the DictationDaddy EHR report skill. Format this transcript as a SOAP note:
<paste transcript>
```

## Ideal Radiologist Flow

From first principles, a radiologist should not need to think about files, endpoints, or formatting prompts. The shortest terminal workflow is:

```bash
cd ~/.claude/skills/dictationdaddy-ehr-report
python scripts/start_session.py
```

That opens a local browser recorder. The user:

1. Pastes a short-lived DictationDaddy/Firebase token or uses a future app handoff.
2. Clicks `Start recording`.
3. Dictates the report.
4. Clicks `Send to DictationDaddy`.
5. Clicks `Copy Claude prompt`.
6. Pastes into Claude Code.

Claude Code then returns the final EHR-ready radiology report.

## What It Does

- Cleans dictated speech into polished clinical prose.
- Formats notes as SOAP, consult notes, progress notes, procedure notes, discharge summaries, and radiology-style reports.
- Can optionally use the authenticated DictationDaddy API flow for audio transcription when the user has configured a Firebase ID token.
- Accepts existing audio files or transcripts, with an optional user-initiated terminal recording helper.
- Preserves uncertainty and avoids inventing clinical facts.
- Keeps output EHR-friendly for copy/paste.

## Audio Recording

Record audio with DictationDaddy, your OS recorder, another trusted recorder, or the optional terminal helper:

```bash
python ~/.claude/skills/dictationdaddy-ehr-report/scripts/record_audio.py \
  --duration 90 \
  --output ./visit-note.wav
```

Then transcribe through DictationDaddy:

```bash
export DD_FIREBASE_ID_TOKEN="..."
python ~/.claude/skills/dictationdaddy-ehr-report/scripts/dictationdaddy_transcribe.py ./visit-note.wav
```

The helper records locally only. It does not upload audio; upload happens only when the authenticated transcription script is run.

## Browser Recorder

For a friendlier local session, open the bundled browser recorder:

```bash
cd ~/.claude/skills/dictationdaddy-ehr-report
python scripts/start_session.py
```

Or manually serve it:

```bash
python3 -m http.server 8765
```

Then open `http://localhost:8765/web-recorder/`.

The page records with browser microphone permission, sends audio to the authenticated DictationDaddy endpoint, shows the returned raw transcript, keeps local transcript history in browser `localStorage`, and can copy a ready-to-paste Claude Code prompt. It does not send anything until the user clicks `Send to DictationDaddy`.

## Optional DictationDaddy API Use

For audio files, users can authenticate through DictationDaddy and provide a short-lived Firebase ID token through the local environment:

```bash
export DD_FIREBASE_ID_TOKEN="..."
python ~/.claude/skills/dictationdaddy-ehr-report/scripts/dictationdaddy_transcribe.py ./audio.webm \
  --context "Transcribe this audio as accurately as possible. Preserve dictated wording and uncertainty. Do not format as a final note."
```

The skill should treat the returned `result` as raw transcript/source material, then run the final clinical formatting pass inside Claude Code.

Payment, subscription, quota, and entitlement validation stays in the DictationDaddy backend. This skill does not bypass or reimplement billing/access logic; it surfaces backend errors and asks the user to resolve access in DictationDaddy.

## Privacy

By default, the skill is instruction-only. The optional helper script sends audio to the authenticated DictationDaddy API only when you run it with `DD_FIREBASE_ID_TOKEN`. Your Claude Code environment, model/provider settings, and DictationDaddy account determine where text and audio are processed.
