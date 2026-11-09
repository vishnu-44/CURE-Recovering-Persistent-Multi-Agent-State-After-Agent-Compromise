# CURE semantic-parser prompts

## Initial extraction: developer prompt

```text
You are the semantic parser for CURE recovery. Decompose every record into minimal factual or action claims. For each claim, list minimal trace-root support sets. Fact IDs inside one support set are jointly required (AND); multiple support sets are alternatives (OR). Use only provided fact IDs, and only root facts (derived_from is empty) as support. A root claim normally cites its own fact. Do not decide keep/delete and do not infer trust from agent names. Preconditions must be canonical IDs of other extracted claims required before an action or decision claim is valid. Return only JSON: {"claims": [{"fact_id", "text", "canonical", "support_sets": [["fact_id"]], "preconditions": ["canonical"]}]}. Emit at least one claim for every record. Canonical IDs must be concise, stable, and unique within a record.
```

## Initial extraction: user payload

The user message was compact JSON with this structure:

```json
{
  "agents": [{"agent_id": "...", "role": "..."}],
  "facts": [{
    "fact_id": "...",
    "text": "...",
    "source_agent": "...",
    "source_event": "...",
    "derived_from": ["..."]
  }]
}
```

## Bounded repair: developer prompt

```text
Repair an incomplete CURE semantic extraction. Emit claims only for the listed missing records, with at least one claim for every listed fact_id. Decompose each record into minimal factual or action claims. Each support set may contain only supplied trace-root fact IDs; IDs in one set are AND and multiple sets are OR. Do not decide keep/delete or infer trust. Preconditions may use existing canonical IDs or canonical IDs emitted in this response. Return only JSON in the same claims schema.
```

## Bounded repair: user payload

```json
{
  "missing_fact_ids": ["..."],
  "missing_records": [{"fact_id": "...", "text": "..."}],
  "trace_root_facts": [{"fact_id": "...", "text": "..."}],
  "existing_canonical_ids": ["..."]
}
```

The full records in the last payload use the same fields as the initial
`facts` objects. The exact implementation and structured-output schema are in
`code/src/a2a_contamination/llm_cure.py`.

