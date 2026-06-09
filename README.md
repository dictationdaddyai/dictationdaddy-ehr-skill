# DictationDaddy EHR Report Skill

Claude Code skill for turning DictationDaddy transcripts, clinician dictation, or locally transcribed audio into EHR-ready reports.

## Install

Clone this repo into your Claude skills directory:

```bash
mkdir -p ~/.claude/skills
git clone https://github.com/rahulbansal16/dictationdaddy-ehr-skill.git ~/.claude/skills/dictationdaddy-ehr-report
```

Then use Claude Code with a prompt such as:

```text
Use the DictationDaddy EHR report skill. Format this transcript as a SOAP note:
<paste transcript>
```

## What It Does

- Cleans dictated speech into polished clinical prose.
- Formats notes as SOAP, consult notes, progress notes, procedure notes, discharge summaries, and radiology-style reports.
- Preserves uncertainty and avoids inventing clinical facts.
- Keeps output EHR-friendly for copy/paste.

## Privacy

The skill is instruction-only. It does not include code that sends patient data anywhere. Your Claude Code environment and model/provider settings control where text is processed.
