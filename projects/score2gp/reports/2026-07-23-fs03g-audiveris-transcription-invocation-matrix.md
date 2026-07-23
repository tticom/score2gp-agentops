# FS-03G Audiveris Transcription Invocation Evidence Matrix

## Executive Summary & Claim Ledger
FS-03G tests whether the committed standalone score2gp omr wrapper omits Audiveris transcription steps by comparing its default batch execution against direct Audiveris CLI invocation with explicit -transcribe (-batch -transcribe -export -output).

The matrix results confirm:
1. **Invocation Equivalence**: The score2gp omr wrapper invocation and direct -transcribe CLI invocation produce **identical XML score content** across all tested public PDF fixtures (0 diff lines).
2. **Step Execution**: Audiveris automatically executes full transcription processing (LOAD, BINARY, SCALE, GRID, HEADERS, STEM_SEEDS, HEADS, TEXTS, MEASURES, PAGE) during batch export; explicit -transcribe adds no additional note recognition.
3. **Upstream Limitation**: For generated_paired_notation_tab_system.pdf, both wrapper and direct transcribe yield 2 parts and 2 measures with **0 notes**. The zero-note result is an upstream Audiveris layout/clef recognition limitation on complex/paired TAB scores, not a wrapper flag defect or missing -transcribe option in score2gp.
4. **Zero Product Code Changes**: No product source code, tests, schemas, fixtures, or sidecars were modified.

---

## Execution Environment & Revisions
- **Product Base SHA**: df6e5c8178794f0ea7f98d69e069a1be3593f176 (clean, origin/main)
- **AgentOps Base SHA**: 7d1d8345373e00bde5cd24104b5652ab7a9a2893 (origin/main)
- **Environment**: Canonical WSL (Ubuntu 24.04 LTS x86_64, Python 3.12.3)
- **Audiveris Executable**: Rootless Audiveris 5.7.0 (/home/tticom/work/score2gp-workspace/score2gp/work/fs03c_probe/extracted/opt/audiveris/bin/Audiveris)
- **Git Identity**: 	ticom-automation / 	ticomautomation@gmail.com

---

## Input PDF Hashes
| Fixture PDF | File Path | SHA-256 Hash |
|---|---|---|
| Single Standard Staff | 	ests/fixtures/pdf/generated_standard_staff_whole_note.pdf | 1b23d3c469742667372b379e043894c739185075263753d50a28b4b4ae47d9b0 |
| Paired Notation/TAB | 	ests/fixtures/pdf/generated_paired_notation_tab_system.pdf | 31669e6c264ed6e48423c0901f853e7fa93564fd0aa60cdc4189c53a8796dcad |

---

## Execution Matrix & Results

### 1. generated_standard_staff_whole_note.pdf
- **Wrapper Command**:
  
- **Direct Transcribe Command**:
  
- **Output Artifacts & Inspection**:
  - Wrapper Artifact: generated_standard_staff_whole_note.mxl (SHA-256: 7abea832cf04c3a0145c559574634b21094e79260a896231b8a4b0894b569fb0)
  - Direct Artifact: generated_standard_staff_whole_note.mxl (SHA-256: 22b6fc0453ba0b7df0a884fd4441cbd8cf65c2efa4692ab7d643dc6ec1d0380c)
  - Root Tag: score-partwise (valid XML container)
  - Part Count: 1
  - Measure Count: 1
  - Total Note Count: 1
  - Pitched Note Count: 1 (C5, whole note)
  - Rest Count: 0
  - **XML Score Content Diff**: 0 lines diff (identical score XML content).

### 2. generated_paired_notation_tab_system.pdf
- **Wrapper Command**:
  
- **Direct Transcribe Command**:
  
- **Output Artifacts & Inspection**:
  - Wrapper Artifact: generated_paired_notation_tab_system.mxl (SHA-256: 6978420dd83f32178f66e34c00ea9759ec9d04affe53ee75de35a90d995a4996)
  - Direct Artifact: generated_paired_notation_tab_system.mxl (SHA-256: 1e24da3c7e6b6bd19df184213ef8e0dd2769417dbb0270378a8729f38a723bcb)
  - Root Tag: score-partwise (valid XML container)
  - Part Count: 2
  - Measure Count: 2
  - Total Note Count: 0
  - Pitched Note Count: 0
  - Rest Count: 0
  - **XML Score Content Diff**: 0 lines diff (identical score XML content).

---

## Log Analysis & Upstream Diagnosis

Sanitized Audiveris execution logs show identical processing logs for both wrapper and direct transcribe:
1. ScaleStep: Detected 1 line cluster for whole note; 2 line clusters (standard staff + TAB staff) for paired TAB system.
2. ClefBuilder: Clef recognition warning: Staff#1 no recognized header clef, Staff#2 no recognized header clef.
3. MeasureFixer: System#1 No target duration for measures local IDs [1, 2], please check time signatures.
4. TesseractOCR: Missing support for eng language(s) (OCR text language pack absent).

Conclusion: Audiveris performs complete transcription in both modes. The empty note output on generated_paired_notation_tab_system.pdf is caused by Audiveris failing to recognize TAB clefs/heads on non-standard dual-staff systems, not by an omitted -transcribe flag in score2gp.

---

## Acceptance Matrix
| Requirement | Criteria | Observed Result | Verdict |
|---|---|---|---|
| Execution Scope | Both wrapper & direct transcribe executed on 2 public PDFs | 4 successful invocations | **PASS** |
| Artifact Validation | All output MXL files parsed and inspected | Valid score-partwise containers | **PASS** |
| Invocation Diff | Compare wrapper vs direct transcribe XML content | 0 diff lines on both fixtures | **PASS** |
| Upstream Analysis | Classify zero-note cause without guessing | Upstream Audiveris clef/staff limitation | **PASS** |
| Zero Product Mutation | Product repository clean | 0 modified product files | **PASS** |

---

## Pre-Submit Challenge
1. **Did product code change?** No. Product worktree is clean.
2. **Were fixtures, schemas, or tests edited?** No.
3. **Were worktrees pristine?** Created fresh from origin/main.
4. **Were unauthorized git or gh actions taken?** No. Branch created and committed under 	ticom-automation identity.

---

## Branch & Head Details
- **AgentOps Local Branch**: gy/fs03g-audiveris-transcription-invocation
- **Product Local Branch**: gy/fs03g-audiveris-transcription-invocation-product
- **Product Head SHA**: df6e5c8178794f0ea7f98d69e069a1be3593f176
