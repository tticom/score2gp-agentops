# ScoreToGP Run Record

## Repo and Branch
- **Repository**: score2gp
- **Branch**: [e.g. feature/my-feature]

## Prompt Chain
- Prompt manifest: [e.g. prompts/prompt-manifest.json or None for simple runs]
- Operative prompt: [e.g. prompts/001-initial-human-prompt.md]
- Prompt files: [e.g. prompts/001-initial-human-prompt.md, prompts/002-followup-prompt.md]

## Command(s) Run
```bash
python scripts/agent_verify.py
```

## Output Directory Path
- **Output**: `work/` or ignored subdirectory path

## Verification Status
- Refer to generated `work/agent_verify.md` report.
- Standard checks (pytest, schema export, validate-ir, and git check diff) overall status: [PASS / FAIL]

## Private-Safety & Repository Hygiene Audit
- Refer to `scripts/artifact_audit.py` status (executed as part of verification).
- Check that `git ls-files fixtures/private work` contains only `.gitkeep`: [PASS / FAIL]

## Next Required Evidence
- [Define next required evidence or implementation step]
