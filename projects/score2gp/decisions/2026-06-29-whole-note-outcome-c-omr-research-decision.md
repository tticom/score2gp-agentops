# Decision: Whole-Note Outcome C and OMR Architecture Research Spike

## Baseline Evidence
- Supervisor approved the ingestion of the candidate safe natural public fixture (Bach Minuet BWV Anh. 120 from Mutopia). Product PR #332 merged to ingest the pinned A4 PDF (`mutopia-bwv-anh-120-minuet-a-minor-a4.pdf`) as an official repository fixture.
- Product PR #333 merged into `tticom/score2gp` (merge commit `b38c0acc9c284379dcd0f82316db08c3fc6211ec`).
- PR #333 successfully added derived `staff_position_index` support for notehead-like `x_aligned_cluster_candidate` proxy records, but did not implement whole-note recognition, pitch, rhythm, ScoreIR, or GP export.
- Subsequent Architect Gate analysis found the geometric `x_aligned_cluster_candidate` proxy path unsafe for whole-note detection due to volatile PDF primitive groupings. Reviewer architecture verification confirmed the geometric path is disproven.
- An Architect diagnostic spike tested a raster connected-component heuristic (topology/aspect-ratio). The diagnostic found that while true whole-note fixtures passed, the Mutopia A4 fixture produced catastrophic false positives (>120 detections).
- False positives inherently overlapped true whole notes in aspect ratio, solidity, and fill ratio because characters like 'o', '0', 'e', 'p', and '4' share the same geometric bounding proportions and 1-hole topology.
- Reviewer architecture verification approved Outcome C, officially blocking basic rule-based raster connected-component heuristics.

## Governance Decision
The Supervisor milestone decision is as follows:
- **Whole-note recognition is not currently supported.**
- **Whole-note Developer implementation is formally blocked.**
- **`x_aligned_cluster_candidate` geometric whole-note detection is blocked.**
- **Basic raster connected-component / hole-count / aspect-ratio whole-note detection is blocked.**
- **Rule-based whole-note implementation is not authorised without a new verified architecture gate.**
- OMR/CV/model-based or semantic symbol-classification work is **not** approved for implementation yet.
- A **bounded OMR/CV Architecture Research Spike** is authorised as the next active task.

## Next Authorised Task
The next active task is an Architect-led OMR/CV Architecture Research Spike. No Developer implementation is authorised. The research must produce measurable feasibility evidence for semantic symbol classification before any implementation can be considered.
