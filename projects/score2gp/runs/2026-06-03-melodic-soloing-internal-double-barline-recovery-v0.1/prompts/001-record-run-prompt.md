Title: Record Internal Double-Barline Recovery v0.1

Context:
Product PR #165 has been merged into `tticom/score2gp`.

Product PR:
https://github.com/tticom/score2gp/pull/165

Product PR title:
Internal Double-Barline Recovery v0.1

Merge state:
- Product PR #165 is merged.
- Product branch: feature/melodic-soloing-internal-double-barline-recovery-v0.1
- Product head SHA: 15588c9933bb2064d6ceca7170bc2f29c0970f7a
- Product merge commit: 47cf92c52408e8c1f2d08400f7e8a075d14ff266

Governance context:
- Agentops PR #29, `research: melodic soloing timing and onset mapping v0.1`, is merged.
- It identified the real blocker as candidate-to-bar assignment loss caused by internal TAB double-barlines being rejected as `pdf_barline_ambiguous`.
- Product PR #165 implemented the recommended fix and reached full melodic soloing note coverage.

Goal:
Create the durable agentops run record for Internal Double-Barline Recovery v0.1.

Branch:
agent/melodic-soloing-internal-double-barline-recovery-v0.1

Required pre-flight in score2gp-agentops:

git switch main
git pull --ff-only origin main
git status --short --branch
git log --oneline --decorate --max-count=10
gh pr status

Files to add/update:
- Add run record:
  projects/score2gp/runs/2026-06-03-melodic-soloing-internal-double-barline-recovery-v0.1/RUN.md
- Add prompt manifest:
  projects/score2gp/runs/2026-06-03-melodic-soloing-internal-double-barline-recovery-v0.1/prompt-manifest.json
- Add prompt:
  projects/score2gp/runs/2026-06-03-melodic-soloing-internal-double-barline-recovery-v0.1/prompts/001-record-run-prompt.md
- Update:
  projects/score2gp/EVIDENCE_REGISTER.md

Run record must include:
- Product repo: tticom/score2gp
- Product PR: #165
- Product branch: feature/melodic-soloing-internal-double-barline-recovery-v0.1
- Product head SHA: 15588c9933bb2064d6ceca7170bc2f29c0970f7a
- Product merge commit: 47cf92c52408e8c1f2d08400f7e8a075d14ff266
- Related research PR: score2gp-agentops #29
- Public test result: 456 passed
- Private audit summary:
  - Lesson 3: 459 matched, stable
  - Lesson 4: 546 matched, stable
  - Lesson 5: 295 matched, stable
  - Lesson 6: 235 matched, stable
  - Lesson 7: 624 matched, stable
  - Melodic Soloing: 82 matched, improved from 56
- Melodic soloing bar boxes:
  - Before: 5
  - After: 8
- ScoreIR/GPIF equality:
  - ScoreIR notes: 82
  - GPIF notes: 82
- Private-safety invariant:
  - git ls-files fixtures/private work -> fixtures/private/.gitkeep

Evidence register entry:
Title:
EV-005: Melodic Soloing Internal Double-Barline Recovery

Claim:
Internal size-2 TAB double-barline clusters are now conservatively resolved by accepting one representative and marking the secondary line as `pdf_barline_double_secondary`, while larger internal clusters remain ambiguous. This recovered the missing melodic soloing bar boxes from 5 to 8 and increased matched notes from 56 to 82 without regressing Lessons 3–7.

Evidence type:
logs / diagnostic_tables / source

Status:
verified

Review decision:
approve

Next required evidence:
Run a fresh post-milestone private-safe baseline audit from product main to classify the next active blocker across all private fixtures, now that melodic soloing has reached full note coverage.

Validation:
Run in agentops:

git status --short --branch
git diff --check

Do not commit private PDFs, generated GP files, generated XML, private audit JSON, overlays, screenshots, logs, or anything under work/.

Open PR:
Create a PR in tticom/score2gp-agentops titled:

record: internal double-barline recovery run v0.1

PR body must include:
- Product PR #165
- Product merge commit 47cf92c52408e8c1f2d08400f7e8a075d14ff266
- Related research PR #29
- Public test summary
- Private-safe audit counts only
- Private-safety invariant result
- Next recommended action: fresh post-milestone active-blocker audit

Stop conditions:
Stop and report if:
- Agentops main cannot be fast-forwarded.
- Working tree is dirty before changes and the changes are not yours.
- Any private/generated artifacts would be committed.
- Product PR #165 merge state cannot be verified.
