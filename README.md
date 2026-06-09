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

## What It Does

- Cleans dictated speech into polished clinical prose.
- Formats notes as SOAP, consult notes, progress notes, procedure notes, discharge summaries, and radiology-style reports.
- Can optionally use the authenticated DictationDaddy API flow for audio transcription when the user has configured a Firebase ID token.
- Accepts existing audio files or transcripts; it does not record microphone audio directly.
- Preserves uncertainty and avoids inventing clinical facts.
- Keeps output EHR-friendly for copy/paste.

## Audio Recording

Record audio with DictationDaddy, your OS recorder, or another trusted recorder first. Then pass the saved audio file or transcript to Claude Code. This keeps microphone permissions and recording UX inside DictationDaddy or the user's local tools, while the skill focuses on transcription handoff and EHR formatting.

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
