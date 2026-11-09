# RevocationBench OSF Code Artifact

This minimal artifact accompanies *Recovering Persistent Multi-Agent State
After Agent Compromise*. It contains only the implementation used for the
experiments and the model prompt templates.

It does **not** contain the paper, saved model outputs, experimental results,
or table-reproduction utilities.

## Contents

- `code/models.py`: records, claims, evidence, and certificate types.
- `code/workflow.py`: queue-until-empty persistent multi-agent workflow.
- `code/prompting.py`: record-level Prompting baseline and exact final prompt.
- `code/cure.py`: trace validation and deterministic claim-level revocation.
- `code/run_example.py`: runnable mixed-record recovery example.
- `prompts/workflow_agents.md`: workflow-agent developer and user prompts.
- `prompts/prompting.md`: Prompting baseline prompts, including the earlier
  template used for three initial per-agent decisions.
- `prompts/cure_semantic_parser.md`: CURE extraction and bounded-repair
  prompts.

## Environment

The reference code requires Python 3.11 or newer and has no third-party
dependencies:

```bash
python3.11 code/run_example.py
```

`requirements.txt` documents that the example uses only the standard library.
The `model_call` accepted by `prompting.recover` is intentionally provider
neutral; an adopter supplies its own model client.

## Workflow termination

This reference workflow has no turn-count ceiling. It continues processing
messages until the workflow queue is empty. It is a compact explanatory
implementation, not the historical experiment harness and not code for
reproducing the paper's numerical results.

The final Prompting template produced 333 of 336 per-agent cleanup decisions.
Three initial Gemini decisions used the earlier template, which is also
included verbatim in `prompts/prompting.md`.

No API keys, provider endpoints, billing ledgers, service logs, manuscript
files, or experimental outputs are included.
