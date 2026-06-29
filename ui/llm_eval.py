import streamlit as st
import pandas as pd

import database as db
from ui.ui_utils import (topbar,card, current_rfp, metric)

# =========================================================================== #
#  PAGE: AI Evaluation
# =========================================================================== #
def page_llm_eval():
    topbar("AI Evaluation", "Check performance of LLM calls.", show_rfp=True)
    rfp = current_rfp()
    evaluation = db.get_evaluation_metrics(rfp["id"]) if rfp else None

    if evaluation:
        overall_score = (
            evaluation["proposal_completeness"]
            + evaluation["average_confidence"]
            + evaluation["context_coverage"]
            + evaluation["pricing_freshness"]
        ) / 4
    left, middle, right = st.columns([1,2,1])

    with left:

        st.metric(
            "Overall AI Quality Score",
            f"{overall_score*100:.1f}%"
        )

    cols = st.columns(4)

    metric(
        cols[0],
        "ic-green",
        "✅",
        "Completeness",
        f"{evaluation['proposal_completeness']*100:.0f}%",
        "Proposal"
    )

    metric(
        cols[1],
        "ic-blue",
        "📚",
        "Context",
        f"{evaluation['context_coverage']*100:.0f}%",
        "Grounded"
    )

    metric(
        cols[2],
        "ic-purple",
        "🎯",
        "Confidence",
        f"{evaluation['average_confidence']:.2f}",
        "LLM"
    )

    metric(
        cols[3],
        "ic-red",
        "⚠️",
        "Flags",
        str(evaluation["hallucination_flags"]),
        "Review"
    )

    with card("AI Quality Indicators"):
        st.write("Proposal Completeness")
        st.progress(evaluation["proposal_completeness"])

        st.write("Average Confidence")
        st.progress(evaluation["average_confidence"])

        st.write("Context Coverage")
        st.progress(evaluation["context_coverage"])

        st.write("Pricing Freshness")
        st.progress(evaluation["pricing_freshness"])

    st.divider()

    st.subheader("🧠 Advanced RAG Evaluation")

    cols = st.columns(4)

    metric(
        cols[0],
        "ic-blue",
        "📖",
        "Faithfulness",
        f"{evaluation['faithfulness']*100:.1f}%",
        "Grounded"
    )

    metric(
        cols[1],
        "ic-green",
        "🎯",
        "Answer Relevancy",
        f"{evaluation['answer_relevancy']*100:.1f}%",
        "Relevant"
    )

    metric(
        cols[2],
        "ic-purple",
        "📚",
        "Context Precision",
        f"{evaluation['context_precision']*100:.1f}%",
        "Retrieved"
    )

    metric(
        cols[3],
        "ic-amber",
        "🔍",
        "Context Recall",
        f"{evaluation['context_recall']*100:.1f}%",
        "Coverage"
    )

    cols = st.columns(3)

    metric(
        cols[0],
        "ic-blue",
        "🏆",
        "MRR@K",
        f"{evaluation['mrr']:.2f}",
        "Ranking"
    )

    metric(
        cols[1],
        "ic-green",
        "🎯",
        "Hit Rate@K",
        f"{evaluation['hit_rate']*100:.0f}%",
        "Success"
    )

    metric(
        cols[2],
        "ic-red",
        "🧩",
        "Chunk Overlap",
        f"{evaluation['chunk_overlap']*100:.1f}%",
        "Lower is Better"
    )

    with card("Advanced Evaluation Indicators"):

        st.write("Faithfulness")
        st.progress(evaluation["faithfulness"])

        st.write("Answer Relevancy")
        st.progress(evaluation["answer_relevancy"])

        st.write("Context Precision")
        st.progress(evaluation["context_precision"])

        st.write("Context Recall")
        st.progress(evaluation["context_recall"])
    
    stats = pd.DataFrame({
    "Metric":[
        "Pipeline Runtime",
        "LLM Calls",
        "Knowledge Base Documents",
        "Pricing Items",
        "MRR@K",
        "Hit Rate@K",
        "Chunk Overlap"
    ],

    "Value":[
        f"{evaluation['runtime_seconds']} sec",
        evaluation["llm_calls"],
        evaluation["knowledge_documents"],
        evaluation["pricing_items"],
        f"{evaluation['mrr']:.2f}",
        f"{evaluation['hit_rate']:.2f}",
        f"{evaluation['chunk_overlap']:.2f}",
    ]
    })

    st.dataframe(
        stats,
        use_container_width=True,
        hide_index=True
    )
