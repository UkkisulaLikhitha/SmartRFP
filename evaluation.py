from statistics import mean
import llm

CONFIDENCE_MAP = {
    "high": 1.0,
    "medium": 0.7,
    "low": 0.4,
}

EXPECTED_SECTIONS = {
    "Executive Summary",
    "Company Overview",
    "Understanding of Requirements",
    "Proposed Technical Solution",
    "Implementation Plan",
    "Security",
    "Deliverables",
    "Timeline",
    "Pricing",
    "Conclusion",
}


def evaluate_pipeline(
    requirements,
    sections,
    pricing_lines,
    runtime_seconds,
    rag_agent=None,
):
    """
    Compute deterministic evaluation metrics.
    """

    # ---------------- Completeness ----------------
    generated = {s["section_title"] for s in sections}

    proposal_completeness = round(
        len(generated & EXPECTED_SECTIONS) /
        len(EXPECTED_SECTIONS),
        2,
    )

    # ---------------- Confidence ----------------
    confidence_scores = [
        CONFIDENCE_MAP.get(
            s.get("confidence", "").lower(),
            0.4,
        )
        for s in sections
    ]

    average_confidence = round(
        mean(confidence_scores),
        2,
    ) if confidence_scores else 0

    # ---------------- Flags ----------------
    hallucination_flags = sum(
        1
        for s in sections
        if s.get("flag_type")
    )

    # ---------------- Context Coverage ----------------
    grounded = sum(
        1
        for s in sections
        if s.get("source")
        and s["source"] != "Synthesised"
    )

    context_coverage = round(
        grounded / len(sections),
        2,
    ) if sections else 0

    # ---------------- Pricing ----------------
    if pricing_lines:
        fresh = sum(
            1
            for p in pricing_lines
            if not p["stale"]
        )

        pricing_freshness = round(
            fresh / len(pricing_lines),
            2,
        )
    else:
        pricing_freshness = 0

    # ---------------- Additional Metrics ----------------
    kb_documents = len(rag_agent.docs) if rag_agent else 0

    pricing_items = len(pricing_lines)

    llm_demo_mode = llm.used_demo()

    llm_calls = 5          # Executive, Overview, Technical, Security, Conclusion

    return {

        "requirements": len(requirements),

        "sections_generated": len(sections),

        "proposal_completeness": proposal_completeness,

        "average_confidence": average_confidence,

        "context_coverage": context_coverage,

        "hallucination_flags": hallucination_flags,

        "pricing_freshness": pricing_freshness,

        "runtime_seconds": round(runtime_seconds, 2),

        "knowledge_documents": kb_documents,

        "pricing_items": pricing_items,

        "llm_calls": llm_calls,

        "demo_mode": llm_demo_mode,
    }