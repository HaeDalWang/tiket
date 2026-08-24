# PoC Cross-Project Handoff

Use this directory when a ticket requires implementation or experimentation in another project. The ticket repository owns the customer question and decision history; the PoC repository owns code and executable experiments.

## Ownership boundary

| Location | Owns |
|---|---|
| `tiket` | Customer question, constraints, hypothesis, acceptance criteria, reply, and decision history |
| PoC project | Code, dependencies, tests, experiment logs, and reproducible environment |
| Returned result | Verified commit, commands, observed results, limitations, and reply-safe conclusion |

Do not copy an entire PoC repository into the ticket. Do not rely on a session transcript as the handoff artifact.

## Status flow

`requested → running → blocked | completed → adopted | rejected`

## Procedure

1. Create a request from `템플릿/PoC_의뢰서.md`.
2. Link it from the ticket frontmatter or `조사·실측` section.
3. Perform the experiment in the designated project and branch/worktree.
4. Create a result from `템플릿/PoC_결과서.md`.
5. Verify the returned repository, branch, commit, command, and output.
6. Append the verified conclusion and limitations to the ticket.
7. Draft the customer reply only from the verified result, not from the PoC agent's summary.

## Required safety

- A PoC must not run against customer production unless a separate human-approved procedure explicitly authorizes it.
- Do not move credentials or customer secrets between projects.
- Use synthetic or sanitized data by default.
- A successful PoC proves only the tested environment and conditions; record transfer limitations.
- Agents do not merge or deploy PoC code unless the user explicitly requests it.
