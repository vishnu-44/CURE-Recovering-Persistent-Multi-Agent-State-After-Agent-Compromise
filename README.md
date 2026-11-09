# CURE: Recovering Persistent Multi-Agent State After Agent Compromise

This repository accompanies the research paper **"CURE: Recovering Persistent Multi-Agent State After Agent Compromise,"** accepted at the *Workshop on Agentic AI in Offensive and Defensive Cyber Operations (AIDC 2026)*.

CURE is a provenance-based recovery approach for persistent multi-agent LLM systems. When an agent or service is compromised, its information may remain in the memories and decisions of other agents. CURE addresses this problem by combining LLM-assisted claim extraction with deterministic provenance-based recovery to identify and quarantine claims that lose sufficient support while preserving independently supported information.

## Repository Contents

The repository provides a compact reference implementation and the prompt templates associated with the research.

| File | Description |
|---|---|
| `models.py` | Data structures for records, claims, evidence, and recovery certificates |
| `workflow.py` | Queue-driven persistent multi-agent workflow |
| `prompting.py` | Record-level prompting recovery baseline |
| `cure.py` | Trace validation and deterministic claim-level recovery |
| `run_example.py` | Runnable example demonstrating recovery of mixed records |
| `cure_semantic_parser.md` | CURE claim-extraction and bounded-repair prompts |
| `prompting.md` | Prompting baseline templates |
| `workflow_agents.md` | Multi-agent workflow prompts |
| `requirements.txt` | Python dependency information |
| `ebxph-osfstorage-archive.zip` | Archived research artifact package |

## Getting Started

**Requirements:** Python 3.11 or newer.

The reference implementation uses only the Python standard library and does not require third-party packages.

Clone the repository and run the included example from the repository root:

`python3 run_example.py`

The example demonstrates how CURE uses recorded provenance and claim-level support relationships to determine which claims can remain available after source revocation.

## How CURE Works

CURE separates recovery into three stages:

1. **Claim extraction:** An LLM decomposes stored records into individual claims and proposes supporting evidence and prerequisites.
2. **Trace validation:** Proposed evidence references are checked against recorded provenance.
3. **Deterministic recovery:** Claims without sufficient surviving support or required prerequisites are quarantined, while independently supported claims can remain available.

The LLM proposes the semantic relationships; deterministic rules make the final recovery decisions.

