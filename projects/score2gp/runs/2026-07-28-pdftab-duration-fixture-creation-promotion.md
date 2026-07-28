# PDF-Tab Duration Fixture Creation Promotion

## Verified predecessor

- AgentOps PR #386 merged at `700214c3224478adfe2c5c4a6105875da4fcb279`.
- The permanent `go` and `got` dispatchers are active on `origin/main`.
- Audit report `projects/score2gp/runs/2026-07-27-pdf-tab-duration-evidence-adequacy-audit.md` returned `PUBLIC_FIXTURE_GAP`.
- Product main remains at `d70d559152c5aa357a7d2eb38e65b09f288bb08f`.

## Selection evidence

The audit proved that current public PDF-tab fixtures (`generated_scorelike_tab.pdf` and `generated_uneven_spacing_tab.pdf`) lack visual duration notation (stems, beams, or flags). Standard-staff flag/beam diagnostics exist, but no public PDF-tab fixture connects those duration candidates to a PDF-only tab assembly path.

Promoting product implementation now would risk treating green standard-notation tests as proof of PDF-tab duration readiness. Creating a deterministic public synthetic fixture (`generated_pdf_tab_duration.pdf`) with drawn stems/beams/flags and an embedded duration oracle closes this evidence gap before any product implementation is authorized.

## Authorisation

Prompt 0019 (`projects/score2gp/prompts/next/0019-generate-public-pdf-tab-duration-fixture.md`) authorises:
- creating a synthetic PDF-tab duration fixture generator script and generated PDF fixture in `score2gp`;
- adding unit/fixture tests to verify candidate duration geometry detection;
- writing a durable run report in `score2gp-agentops`.

Product source code in `src/score2gp/` remains read-only. No private inputs, reference GP leakage, automatic merge, or product implementation changes are authorised.

## Skills

The task uses workflow skills locked at `0d6d84879eff0d352b444fdeceb3bb7a098e0c47`.
