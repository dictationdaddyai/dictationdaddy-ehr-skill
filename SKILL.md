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
- An audio file, only if the local environment has transcription tooling available.

If audio cannot be transcribed locally, ask the user for the DictationDaddy transcript instead of guessing.

## Safety Rules

- Do not invent symptoms, exam findings, medications, doses, lab values, imaging results, diagnoses, dates, laterality, or follow-up plans.
- Preserve clinician uncertainty. Use phrases like "not stated", "unclear", or "[inaudible]" only when needed.
- Do not add medical advice beyond what the clinician dictated.
- Do not remove clinically important negatives, qualifiers, time course, or measurements.
- Do not store PHI, send it to external services, or call network tools unless the user explicitly asks.
- Flag obvious contradictions or missing critical fields in a short `Clarifications` section rather than silently resolving them.
- If the user asks for the final note only, omit explanations and output only the note.

## Workflow

1. Identify the target note type from the user request or the dictation.
2. Clean transcription artifacts:
   - remove filler words, repeated starts, and punctuation errors
   - keep clinical meaning, sequence, and uncertainty intact
   - expand only common safe abbreviations when clarity improves
3. Structure the output for direct EHR paste.
4. Put uncertain or missing items in brackets only when needed.
5. End with `Clarifications` only if there are genuine unresolved issues.

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

For specialty templates and examples, read `references/templates.md`.

