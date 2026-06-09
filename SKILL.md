---
name: dictationdaddy-ehr-report
description: Use when a clinician provides dictated speech, a DictationDaddy transcript, or an audio file and wants it converted into a polished EHR-ready clinical report, SOAP note, progress note, consult note, discharge summary, procedure note, or radiology-style report without inventing facts.
---

# DictationDaddy EHR Report

Turn clinician dictation into an EHR-ready note. Prioritize fidelity to the source over elegance.

## Inputs

Accept any of these:

- Raw dictated text pasted by the user.
- A DictationDaddy transcript.
- An existing audio file recorded by DictationDaddy, the OS, or another recorder.

If audio cannot be transcribed locally, use the authenticated DictationDaddy API path only when the user has explicitly configured credentials for it. Otherwise ask the user for the DictationDaddy transcript instead of guessing.

## Audio Capture Boundary

This skill does not silently record microphone audio. Audio capture must be user-initiated and visible. The preferred path is still DictationDaddy or the user's local recording workflow, but terminal users can use a bundled helper script when a local recorder is installed.

Supported terminal UX:

1. User authenticates through DictationDaddy and provides a short-lived Firebase ID token through `DD_FIREBASE_ID_TOKEN` or an app handoff.
2. User records with DictationDaddy, their OS, another trusted recorder, or `scripts/record_audio.py` if their machine has a supported recording command.
3. The skill sends the existing audio file to the authenticated DictationDaddy endpoint.
4. Claude Code formats the returned raw transcript into the final EHR-ready note.

Supported browser UX:

1. User runs `scripts/start_session.py`, which serves `web-recorder/` locally and opens the browser.
2. Browser records audio after explicit microphone permission.
3. Browser sends audio to DictationDaddy only after the user clicks send.
4. Browser shows the raw transcript and local history.
5. Browser copies a ready-to-paste Claude Code prompt.
6. Claude Code formats the copied transcript into the final EHR-ready note.

## Safety Rules

- Do not invent symptoms, exam findings, medications, doses, lab values, imaging results, diagnoses, dates, laterality, or follow-up plans.
- Preserve clinician uncertainty. Use phrases like "not stated", "unclear", or "[inaudible]" only when needed.
- Do not add medical advice beyond what the clinician dictated.
- Do not remove clinically important negatives, qualifiers, time course, or measurements.
- Do not store PHI, send it to external services, or call network tools unless the user explicitly asks.
- Do not ask users to paste long-lived secrets into chat. If using the DictationDaddy API, prefer environment variables or the user's existing app auth flow.
- Do not bypass or reimplement DictationDaddy validation, payment, quota, subscription, or entitlement checks. The backend remains the source of truth.
- Flag obvious contradictions or missing critical fields in a short `Clarifications` section rather than silently resolving them.
- If the user asks for the final note only, omit explanations and output only the note.

## Workflow

1. Identify the target note type from the user request or the dictation.
2. If the input is audio:
   - prefer a provided DictationDaddy transcript when available
   - do not attempt to open the microphone or record audio unless the user explicitly asks and a local recorder helper is available
   - if the user asks to use DictationDaddy auth/API, read `references/dictationdaddy-api.md`
   - otherwise use local transcription only when available
3. Treat DictationDaddy API output as raw transcript/source material unless the user explicitly requested server-side formatting. Claude Code should perform the final EHR formatting pass.
4. Clean transcription artifacts:
   - remove filler words, repeated starts, and punctuation errors
   - keep clinical meaning, sequence, and uncertainty intact
   - expand only common safe abbreviations when clarity improves
5. Structure the output for direct EHR paste.
6. Put uncertain or missing items in brackets only when needed.
7. End with `Clarifications` only if there are genuine unresolved issues.

## Default Formats

For general clinical notes, use SOAP:

```text
Subjective

Objective

Assessment

Plan
```

For consults or initial evaluations, use:

```text
Reason for Visit
History of Present Illness
Pertinent History
Exam
Assessment
Plan
```

For radiology or imaging-style dictation, use:

```text
Exam
Indication
Technique
Comparison
Findings
Impression
```

For procedure notes, use:

```text
Procedure
Indication
Consent
Technique
Findings
Complications
Disposition / Plan
```

For discharge summaries, use:

```text
Admission Diagnosis
Discharge Diagnosis
Hospital Course
Discharge Medications
Follow-Up
Discharge Instructions
```

## Output Style

- Use concise clinical prose.
- Prefer complete sentences for narrative sections and bullets for plans.
- Keep headings plain and EHR-friendly.
- Avoid markdown tables unless explicitly requested.
- Do not include marketing copy, commentary, or "here is your note" language.

## Optional Reference

- For specialty templates and examples, read `references/templates.md`.
- For authenticated DictationDaddy transcription/report flow, read `references/dictationdaddy-api.md`.
