# ENZO — AI-Assisted Build Workflow

## Purpose

ENZO is designed to be assembled and learned **alongside an AI assistant**, used strictly as a *tutor and explanation layer*.

This document defines the **supported way** to use AI during ENZO assembly so that assistance remains:

- aligned  
- constrained  
- predictable  
- safe  

ENZO’s documentation, wiring, firmware, and architecture **remain the sole authority at all times**.

---

## What the AI Is For

When configured correctly, an AI assistant may be used to:

- Explain *why* ENZO is designed the way it is
- Help interpret ENZO documentation
- Reason through consequences *before* changes are made
- Assist with debugging **within ENZO’s defined boundaries**
- Act as a learning partner during each build phase

The AI is treated as an **interactive reference**, not a designer.

---

## What the AI Is NOT For

The AI must **not**:

- Choose or change architecture
- Suggest alternative wiring or power paths
- Optimise or refactor ENZO systems
- Invent features or behaviours
- Override ENZO documentation

If the AI disagrees with ENZO, **ENZO wins**.

---

## Mandatory AI Configuration

Before asking technical questions, the builder **must** configure their AI assistant using the official setup block provided in:

`ENZO_AI_SETUP.md`

This step aligns the AI with ENZO’s constraints and prevents scope creep or unsafe suggestions.

Failure to apply the setup block places the builder **outside the supported workflow**.

---

## Supported Interaction Model (Thread Setup)

ENZO uses a professional handover-style interaction model.

Before asking for help, the builder provides:

1. **CAT A — Constraints**  
   Physical laws, safety rules, and elements that cannot change.

2. **CAT B — Intent**  
   What the builder is trying to achieve or understand.

3. **Current Snapshot**  
   The current ENZO version, phase, and known-good state.

Only after this context is established does the builder move into:

- “What I’m working on today”
- “Here’s the problem”
- “Help me think through this”

This keeps AI assistance aligned, deliberate, and useful.

---

## Builder Responsibility

ENZO assumes the builder will:

- follow documented build order
- respect known-good states
- apply AI guidance as *explanation*, not instruction

Using AI outside the defined workflow is permitted, but **not supported** as part of ENZO.

---

## Summary

- ENZO functions independently of AI
- AI assistance is optional but encouraged
- Alignment is achieved through documentation, not trust
- The setup file is sufficient **when used as instructed**

ENZO teaches how to build real systems in an AI-assisted world — without surrendering authority, safety, or understanding.
