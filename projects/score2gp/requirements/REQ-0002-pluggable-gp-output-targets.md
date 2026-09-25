# REQ-0002 — Pluggable, version-selectable Guitar Pro output

- **Status:** `RESEARCHED`. Q1–Q2 answered 2026-09-25; Q3–Q4 open. Not prioritised and not promoted.
- **Owner:** maintainer (`tticom`)
- **Recorded:** 2026-09-25, from maintainer direction in an implementation session
- **Extends:** [REQ-0001](REQ-0001-native-faithful-pdf-to-gp.md) obligation U13 ("Additional explicitly supported Guitar Pro versions")
- **Decision record:** ADR-008 in [`ARCHITECTURE_DECISIONS.md`](../ARCHITECTURE_DECISIONS.md) (Proposed)
- **Evidence baseline:** product `main` at `71535f381584615a96667d026ef5a579c4c356d5`; private fixtures `main` at `da39f2a`, plus the GP 8.1.4 reference added 2026-09-25

## 1. Requirement

Score2GP must produce Guitar Pro output in whichever file version the customer
selects. The versions in scope are **Guitar Pro 5, 6, 7 and 8**. **Delivery
starts with the newest (GP8, then GP7).** GP5 and GP6 are provided for by the
architecture (injectable targets) and delivered when demand justifies them.

Each version is an **output target**: an independently installable module
behind one stable, versioned interface. Adding, removing or upgrading a target,
including future Guitar Pro versions, must not require changes to recognition,
resolution, the canonical musical document, or any other target.

Maintainer direction (2026-09-25), verbatim:

> "if this is to be a commercial product, it will need to be able to produce whatever version of gp file the customer requires."
>
> "Output versions 5 to 8 and new versions must be bolt-on."
>
> "it has to be an injectable module to cope with current and future file type versions, so ultimately this feature needs to be rearchitected."
>
> "If the converter is an injectable, we can focus on the file output version in isolation. gp5 might be still in use and might also be a target that's not requested often. I'd go with newer versions at this stage and plan for older versions by architecture. i.e. injectability."

## 2. Rationale

- **Commercial reach.** Customers run different Guitar Pro versions. A product that writes only one version excludes customers on older installs and tools that consume older formats.
- **Longevity.** Guitar Pro has changed container or encoding at least three times (binary GP3–5, `.gpx` GP6, ZIP GP7/8), and GP8 extended GPIF again. A bolt-on target is the difference between adding a module and rewriting the writer.
- **Accuracy.** A single writer with post-hoc version patches (today's design, §5) produces files that claim a version they are not. Per-target modules with per-target evidence make each claim checkable.

## 3. Definitions

| Term | Meaning |
|---|---|
| Output target | One registry entry that writes exactly one Guitar Pro file format version (for example `gp8`, `gp7`), with its own ID, capability matrix, profile and acceptance evidence |
| Target family | A shared writer implementation used by several targets with the same encoding: **binary** (GP3–GP5), **GPIF in BCFZ/BCFS** (GP6 `.gpx`), **GPIF in ZIP** (GP7/GP8 `.gp`). A family is code reuse, not a registry entry |
| Target profile | The version-specific facts a target supplies to its family writer (version stamps, container facts, feature set, limits), derived from real Guitar Pro-authored files |
| Capability matrix | Per-target declaration of which canonical features are represented **exactly**, **degraded** (with a declared, reported loss) or **refused** |
| Degradation | A reported, located, policy-permitted loss of a feature the target cannot represent. Never silent |

## 4. Research findings

### 4.1 Format families

| Version | Extension | Container | Score encoding | Source |
|---|---|---|---|---|
| GP3, GP4, GP5 | `.gp3` `.gp4` `.gp5` | One binary stream | Proprietary binary. Arobas once published GP4 documentation; the rest was reverse-engineered | [alphaTab: Guitar Pro 3–5](https://alphatab.net/docs/formats/guitar-pro-3-5) |
| GP6 | `.gpx` | Proprietary **BCFZ** (compressed) / **BCFS** (file system); not a ZIP | GPIF XML (`score.gpif`), plus `misc.xml` and `BinaryStylesheet` | [alphaTab: Guitar Pro 6](https://alphatab.net/docs/formats/guitar-pro-6) |
| GP7 | `.gp` | ZIP; `Content/score.gpif` | GPIF | Programme plan §19; product writer |
| GP8 | `.gp` | Same ZIP; may carry extra members such as audio | GPIF, extended for new features | [alphaTab: Guitar Pro 8](https://alphatab.net/docs/formats/guitar-pro-8): "the same as Guitar Pro 7 but with potentially additional files in the zip (e.g. for audio tracks) and with an extended `score.gpif`" |

alphaTab lists three GP8-only features: audio tracks, password-locked files and numbered notation.

### 4.2 Verified locally (private corpus, 2026-09-25; counts and markers only)

- `Can't Find My Way Home (open chord shenanigans).gp`: `GPVersion` 8.1.4, `VERSION` member `7.0`, an embedded MP3 asset (`Content/Assets/*.mp3`), 21 MasterBars, one track.
- `Lesson-3.gp` through `Lesson-7.gp`: `GPVersion` 8.1.0, `VERSION` member `7.0`.
- `Ex 2 Hands Up.gp` (added 2026-09-25): **GP7-authored**. `GPVersion` 7, `GPRevision` 12025, `VERSION` member `7.0`, 11 MasterBars.
- `Ex 2 Hands Up.gpx` (added 2026-09-25): **GP6-authored**.
  - BCFZ-compressed BCFS container holding `score.gpif`, `misc.xml`, `BinaryStylesheet`, `PartConfiguration` and `LayoutConfiguration`.
  - `GPRevision` 11686 and **no `GPVersion` element**; 11 MasterBars.
  - Decoded read-only with the algorithm alphaTab documents in `GpxFileSystem.ts`; as in alphaTab, the compressed stream may end before its declared length.
- **Same piece, two versions, different encoding of the same repeats.** Both files have one repeat start (count 4) and alternate endings 1–4. The three repeat-end bars have count **4** in GP7 and **2** in GP6. Raw attributes are therefore not version-neutral. Comparison must use a normalized projection (the resulting play order), and each target profile must encode repeats the way its version does. The PDF must adjudicate the intended meaning.
- No GP5-authored reference exists yet.
- Neither file family contains the tags the current adapter injects (`TargetCompliancy`, `VersionLayout`, `StyleCollections`/`ModernDefault`, `LegacyLayout`).
- GP8 keeps `VERSION` = `7.0`. The current adapter writes `8.0` for GP8.

### 4.3 Open-source implementations (candidate validators or writers)

| Project | Formats | Write support | Licence | Note |
|---|---|---|---|---|
| [alphaTab](https://github.com/CoderLine/alphaTab) | Reads GP3–5, GPX, GP7/8, MusicXML | Exports GP7 and alphaTex only ([exporter guide](https://alphatab.net/docs/guides/exporter)) | MPL-2.0 | Candidate **independent reader**, never the sole oracle (programme plan §19) |
| [PyGuitarPro](https://github.com/Perlence/PyGuitarPro) | GP3, GP4, GP5 | Read and write | LGPL-3.0-only | Python port of alphaTab/TuxGuitar lineage. Candidate GP5 writer or reader, subject to licensing (Q2) |
| [TuxGuitar](https://github.com/helge17/tuxguitar) | GP3–5 and others | Yes (not verified in this research) | Not verified in this research | Possible cross-check |

No Arobas specification, writer SDK or headless validator exists for any version (programme plan §19).
Acceptance for every target therefore needs real application round trips in that version, plus an independent reader.

### 4.4 Conclusions

1. **GP7 and GP8 are one family.** They share a container and an encoding and differ by profile (version stamps, feature set). They are **two targets** (`gp7`, `gp8`) that share one GPIF-ZIP family writer, each with its own profile, capability matrix and acceptance. Separate writer implementations would duplicate the family.
2. **GP6 reuses GPIF but needs its own container writer** (BCFZ/BCFS). No open-source GPX writer was identified. alphaTab reads GPX only.
3. **GP5 is a separate binary family**, sharing no code with GPIF. It is a new writer plus an independent reader, from reverse-engineered knowledge or an LGPL dependency.
4. **Expressiveness differs by version.** The exact limits per version (voices per bar, string counts, techniques, audio, and so on) are **not yet verified**. OUT-00 must establish them from real Guitar Pro-authored files and documentation before any capability matrix is claimed.
5. **Acceptance depends on access to each application version** (Q1). GP5 and GP6 are discontinued products.

## 5. Current state and impact

| Area | Location | Finding | Impact |
|---|---|---|---|
| Version adapter | `src/score2gp/version_adapter.py` | Post-processes GP7-style GPIF into "GP6"/"GP8". Injects tags absent from real files; writes `VERSION` 8.0 for GP8 (real: 7.0); emits "GP6" as a ZIP (real GP6 is BCFZ/BCFS `.gpx`); an unknown target silently becomes GP7; invalid XML is passed through unchanged | **Live false-output risk.** The CLI can emit a file presented as GP6/GP8 that is not one. Contained by OUT-01; replaced by OUT-02 |
| Version stamp | `src/score2gp/gpif.py:374-376` | Hard-codes `GPVersion` 8.1.0 and a fixed `GPRevision` for every target | Must come from the selected target profile |
| Test-conditional writer | `src/score2gp/gpif.py:149` | A different serializer runs when pytest is loaded | Target acceptance tests would not exercise production output. Prerequisite fix (NPG-06A / FND-01) |
| Package assembly | `src/score2gp/gp_package.py:29,97-138` | `target_version` threaded through template overlay and `VERSION` member | Becomes the GPIF-ZIP family's container stage |
| Entry points | `src/score2gp/cli.py:144` (`--target`), `src/score2gp/batch.py:44` (`target_version`) | Free-text target with silent fallback | Becomes a registry lookup that refuses unknown or uninstalled targets |
| Canonical model limits | `src/score2gp/ir.py:99,268,516-528`; `gpif.py:833` | Values are clamped (strings 1–12, frets 0–36, voices 1–8, meter 1–64) | Target limits belong in the target capability check (refuse or declare degradation), not in silent canonical clamps. Prerequisite fix (FND-02) |
| Tests | `tests/test_target_version_adapters.py` | Asserts the invented tags and a ZIP "GP6" | Encodes fiction as expected behaviour. Remove in OUT-01 |
| Independent reader | `scripts/native_slice_reference.py` | GPIF only; fails closed on unknown features. On the GP 8.1.4 reference it refuses on chord diagrams, grace notes, ties, vibrato, accents, hammer-on/pull-off, slides, bends, mute and a tuplet | Per-target readers are required; the GPIF reader must grow feature support before it can check GP8-authored references with those features |
| Prior art | `tticom/score2gp-exporter` (one commit, 2026-08-03) | Scaffold with `registry.py` | Not used. Confirms the registry idea; not a delivery vehicle |

## 6. Functional requirements

- **FR-1 Target selection.** The caller selects a target by stable ID (for example `gp5`, `gp6`, `gp7`, `gp8`) through `ConversionOptions.target` (programme plan §14) and the CLI/API adapters. The default target is versioned product policy and is reported.
- **FR-2 Fail closed on selection.** An unknown, uninstalled or incompatible target is refused before recognition runs. The refusal lists the installed targets.
- **FR-3 Target interface.** Each target provides:
  - identity (ID, family, written format version, file extension, interface version);
  - its capability matrix;
  - `compile(canonical document, target options) -> package + report`;
  - structural validation of its own output (programme Levels 1–3).
- **FR-4 Bolt-on registration.** Targets are discovered through a registry. A target shipped in a separate installable package registers without any change to core code. First-party targets use the same mechanism.
- **FR-5 Capability negotiation.** Before writing, the features used by the canonical document are checked against the target's matrix. Each unsupported feature is refused (strict default) or degraded under an explicit policy, and every degradation is reported with its source location. Silent omission or clamping is forbidden.
- **FR-6 Canonical independence.** The canonical document carries no target-specific data, and targets infer no musical semantics (programme invariant 5).
- **FR-7 Determinism.** The same canonical document, options and target version produce identical normalized semantics.
- **FR-8 Provenance.** The conversion report records the target ID, target module version, format version written, profile evidence version, and the capability-check outcome.
- **FR-9 Evidence-derived profiles.** Every version stamp and container fact a target writes is traceable to a real Guitar Pro-authored file or a documented source recorded in its profile.

## 7. Non-functional requirements

- **NFR-1 Isolation.** Adding, removing or upgrading one target leaves every other target's output unchanged (per-target golden semantics).
- **NFR-2 Independent verification per target.** Each target has an independent reader that shares no code with its writer.
- **NFR-3 Licensing.** Each target declares its dependencies' licences. A licence incompatible with the commercial distribution model blocks that target from release (see Q2).
- **NFR-4 Safe loading.** Targets load only from installed packages through the registry, never from arbitrary paths. Readers disable external entity resolution.
- **NFR-5 Interface versioning.** The target interface is versioned. The registry refuses a target built for an incompatible interface version.

## 8. Acceptance criteria

Requirement-level criteria:

1. **Bolt-on proof.** A test target shipped as a separate package registers and converts with no core change. Removing it changes no other target's output.
2. **Selection refusal.** Unknown and uninstalled targets are refused before recognition. A negative control shows the test fails if the check is disabled.
3. **No fabricated versions.** No target writes a version stamp, tag or container fact without recorded profile evidence (FR-9). An audit test fails on any unsourced literal.

Per-target criteria, for every supported target T:

4. At least one Guitar Pro-authored reference file and one blank-score file in version T exist in the private corpus, with hashes (extends NPG-00C).
5. T's independent reader parses T's output. Normalized semantics match the canonical document apart from declared degradations.
6. The Guitar Pro application in version T opens, plays, saves and reopens the output without a repair prompt or semantic loss beyond declared degradations. A check that was not run is `NOT_EVALUATED`, never a pass.
7. Every capability-matrix entry is tested. A document using a refused feature is refused under strict policy, with a negative control.

## 9. Scope

- **In scope, first delivery:** the target interface and registry; capability negotiation; the GPIF-ZIP family writer; the `gp8` target with its reader and acceptance. The `gp7` target is built on the same family but is **released only when criterion 6 can be met in a real Guitar Pro 7 application** (see §12, Q1).
- **In scope by architecture, later delivery:** GP6 (`.gpx`) and GP5 targets, as bolt-on modules proven possible by the interface's bolt-on criterion.
- **Out of scope for now:** GP3/GP4 targets (addable later as bolt-ons); reading these formats as conversion input; non-Guitar-Pro targets such as MusicXML or Sibelius. The interface should not preclude them (multimodal roadmap, Phase 3).

## 10. Dependencies and sequencing

- **Prerequisites:**
  - remove the pytest-conditional serializer (NPG-06A);
  - replace canonical clamps with rejection (FND-02);
  - a canonical musical document with an explicit measure/voice/beat hierarchy (NPG-04B), which the target interface consumes.
- **Evidence:** blank-file and reference-file capture per version (NPG-00C, extended to GP5/GP6/GP7). An independent GPIF reader with broader feature coverage (FND-03).
- **Acceptance harness:** Guitar Pro application round trip per version (NPG-06D, extended per target).
- **Priority:** the maintainer will plan delivery as priority rises. Exception: **OUT-01 containment is recommended early**, because the current adapter can emit mislabelled files today.

## 11. Proposed tasks (recorded in the task authority's backlog; not promoted)

| ID | Goal | Depends on | Exit evidence |
|---|---|---|---|
| OUT-00 | Evidence and research: capture GP5/GP6/GP7/GP8-authored reference and blank files; derive per-version feature limits; licensing review; confirm application access | none | Evidence record with hashes; draft capability matrix per version; answers to Q1–Q2 |
| OUT-01 | Containment: `--target` accepts only evidence-backed targets (the current GPIF-ZIP output) and refuses others; remove invented tags and their tests; stop unsourced version stamps | none | Negative tests: GP6/GP8 selection refuses; audit finds no invented tag |
| OUT-02 | Target interface and registry (ADR-008); move the current GPIF-ZIP writer behind it as the family writer for the first target with semantic parity; registry discovery; bolt-on test target | NPG-06A, FND-02, NPG-04B | Criteria 1–3 |
| OUT-03 | Capability matrix, negotiation and degradation report | OUT-02, OUT-00 | Criterion 7 for the first target |
| OUT-04 | `gp8` target (GP8 profile of the GPIF-ZIP family) | OUT-03, OUT-00 | Criteria 4–7 for GP8 |
| OUT-05 | `gp7` target (GP7 profile of the GPIF-ZIP family) | OUT-04, GP7-authored evidence, access to a Guitar Pro 7 application | Criteria 4–7 for GP7 |
| OUT-06 | *Deferred by maintainer decision:* GP5 binary target and independent reader | OUT-03, Q2 | Criteria 4–7 for GP5 |
| OUT-07 | *Deferred by maintainer decision:* GP6 `.gpx` target (BCFZ/BCFS container plus GP6 GPIF profile) and reader | OUT-03 | Criteria 4–7 for GP6 |

## 12. Open questions for the maintainer

Maintainer answers (2026-09-25):
- **Q1:** only Guitar Pro 8 is available. GP8 acceptance is possible now. Opening or re-saving a GP7 file in GP8 is **not** a GP7 round trip and does not satisfy criterion 6 for `gp7`. The `gp7` target may be built and tested against GP7-authored references (`Ex 2 Hands Up.gp`), but it is not released until a Guitar Pro 7 application is available. That follows the maintainer's no-new-spend constraint without weakening acceptance. GP5/GP6 application acceptance is deferred with those targets.
- **Q2:** licensing must be as narrow as possible, so copyleft dependencies are unwanted in the product. See [REQ-0003](REQ-0003-dependency-licence-compatibility.md).
- **Q3–Q5:** still open. GP3/GP4 stay out of scope and could be added later as bolt-ons.

1. **Application access:** do you have licensed Guitar Pro 5, 6 and 7 installs (or can obtain them) for per-version acceptance? Without them, criteria 4 and 6 cannot be met for those versions.
2. **Licensing posture:** may a commercial Score2GP depend on LGPL-3.0 code (PyGuitarPro) for a writer, or on MPL-2.0 code (alphaTab) as a validator? This decides whether GP5 is built in-house.
3. **Default target** when the caller does not specify one.
4. **Third-party targets:** is the plugin interface public (partners may add targets), or first-party only? This decides how strictly the interface must be versioned and documented.
5. **GP3/GP4:** permanently out, or a later bolt-on?

## 13. Risks

| Risk | Countermeasure |
|---|---|
| Formats are proprietary and reverse-engineered | Profiles only from real Guitar Pro-authored files; application round trip is mandatory per target |
| Licence contamination (LGPL/MPL) in a commercial product | Q2 decision before OUT-06; NFR-3 |
| Discontinued applications (GP5/GP6) cannot be tested | Q1; a target without application acceptance is not released |
| Version-specific encoding of the same musical meaning (for example, repeat counts in GP6 vs GP7) | Per-target profiles from real files; oracle compares normalized semantics (play order), never raw attributes |
| Capability-matrix scope grows with each version | Matrix entries derive from the canonical feature list; unknown features refuse by default |
| Mislabelled output from the current adapter | OUT-01 early |
