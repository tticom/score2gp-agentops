# ScoreToGP Handoffs

Durable agent handoffs for ScoreToGP live in this directory.

Use this directory for branch handoff state, current PR context, verification summaries, and next-step notes that need to survive beyond a single conversation. Do not copy long-form handoff state back into the `score2gp` product repository.

Use the `durable-handoff` skill pinned by
`projects/score2gp/SKILLS_LOCK.md`. Record full product, governance, and skills
revisions; distinguish independently verified evidence from author-reported
evidence; and state the exact next authorised action.

Use the generic `handoff` skill only for a temporary conversation bridge. It
does not replace this durable project evidence.
