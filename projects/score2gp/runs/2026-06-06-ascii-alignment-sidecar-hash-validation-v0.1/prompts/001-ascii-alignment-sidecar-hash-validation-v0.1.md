# ASCII Alignment Sidecar Hash Validation v0.1

Harden the ASCII alignment sidecar gate by validating SHA-256 hashes for the active PDF and MusicXML files before the sidecar is allowed to pass the ASCII ScoreIR gate.

Requirements:
1. Extend the Pydantic sidecar model `AsciiMusicXmlAlignment` with SHA-256 fields: `source_pdf_hash` and `source_musicxml_hash`.
2. Implement a deterministic chunked helper `compute_sha256(path: Path) -> str` that reads bytes safely in 64KB blocks.
3. Validate active PDF and MusicXML source hashes against expected hashes at the ASCII ScoreIR gate.
4. Refuse conversion if hashes are missing, mismatched, or malformed, returning refusal code `ascii_alignment_stale_sidecar_hash`.
5. Map `ascii_alignment_stale_sidecar_hash` to CLI exit code 4.
6. Ensure legacy sidecars without hashes are refused and hashes are not silently repaired during gate validation (loaded sidecars must not be mutated).
