import requests
import streamlit as st

SYSTEM_PROMPT = """You are ONE, an academic research drafting assistant. Produce a structured, editable research manuscript based on the user's idea. Never invent citations, DOIs, experiments, survey results, statistics, ethics approval, or findings. If evidence or data is missing, label the relevant part as proposed work, a research plan, or a placeholder requiring evidence. Clearly state that references require verification. Use Markdown headings. Include a research integrity note at the end. Do not claim that you searched sources unless a search tool was actually used."""

def demo_research(idea):
    title = idea.strip().rstrip(".")
    paper = f"""# {title.title()}

> **Demo Mode:** This is an illustrative draft generated from the submitted idea. It is not a source-verified research paper. Replace placeholders with evidence and actual results before academic use.

## Abstract
This draft outlines a possible investigation into {title.lower()}. The study would define the research problem, review relevant scholarship, specify an appropriate methodology, and evaluate outcomes using transparent criteria. The abstract should be revised after the research design and evidence are established.

**Keywords:** research design; evidence synthesis; evaluation; reproducibility

## 1. Introduction
The proposed topic concerns {title.lower()}. A rigorous study should establish the context, explain why the problem matters, define the scope, and state the contribution supported by evidence. Add recent, verifiable sources to support claims about the current state of the field.

## 2. Problem Statement
Clearly define the practical or theoretical problem. Describe who or what is affected, the current limitations, and why existing approaches may be insufficient. Each factual claim should be supported by a traceable source.

## 3. Aim and Objectives
The overall aim is to investigate the submitted research idea using an appropriate and reproducible method.

Specific objectives:
1. Establish the research context through a documented literature search.
2. Define research questions and measurable evaluation criteria.
3. Select and justify an appropriate methodology.
4. Analyze actual evidence and report limitations transparently.

## 4. Research Questions
- What problem does the proposed approach address?
- How does it compare with relevant existing approaches?
- Which evaluation measures are appropriate for the research context?
- What limitations and risks should be considered?

## 5. Literature Review
This section requires a real search of scholarly literature. Build an evidence table containing each study's research question, method, dataset or sample, findings, limitations, and DOI or stable URL. Do not treat this demo text as a completed literature review.

## 6. Proposed Methodology
Use a method appropriate to the discipline and research question. Document data sources, inclusion criteria, variables, procedures, instruments, analysis methods, and reproducibility steps. If human participants or sensitive data are involved, determine applicable ethics and consent requirements before collection.

## 7. Evaluation Plan
Define evaluation metrics before analyzing data. Explain baselines, comparison conditions, validation procedures, uncertainty, and potential sources of bias. Do not report numerical results until actual analysis has been performed.

## 8. Expected Contribution
Potential contributions may include a documented framework, comparative analysis, implementation, dataset analysis, or evidence-based recommendations. Confirm novelty through a current literature review rather than assuming that the idea is new.

## 9. Limitations and Ethical Considerations
Discuss data availability, generalizability, measurement error, bias, reproducibility, privacy, and any domain-specific risks. Disclose AI assistance in accordance with the target venue's policies.

## 10. Conclusion
The idea provides a starting point for a research project. The final conclusion must be written after reviewing relevant literature and analyzing actual evidence; it should not claim outcomes that have not been established.

## References
No external references have been retrieved in Demo Mode. Add real sources and verify their metadata before submission.

## Research Integrity Note
This document is an illustrative scaffold, not evidence of completed experiments or a source-verified paper. Replace placeholders with verified literature, a justified method, real findings where applicable, and human-reviewed conclusions.
"""
    return paper, []

def generate_research(idea, model=None):
    api_key = st.secrets.get("OPENAI_API_KEY", "")
    base_url = st.secrets.get("OPENAI_BASE_URL", "https://api.openai.com/v1").rstrip("/")
    model = model or st.secrets.get("OPENAI_MODEL", "gpt-4.1-mini")
    if not api_key:
        raise RuntimeError("API Mode requires OPENAI_API_KEY in Streamlit secrets. Switch to Demo Mode or configure the key.")
    url = f"{base_url}/chat/completions"
    payload = {
        "model": model,
        "temperature": 0.4,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Create a detailed, editable research manuscript draft from this idea. Use appropriate academic headings, identify assumptions and missing evidence, do not fabricate sources or empirical findings, and clearly mark what needs verification.\n\nIDEA:\n{idea}"}
        ]
    }
    response = requests.post(url, headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
                             json=payload, timeout=120)
    if response.status_code >= 400:
        raise RuntimeError(f"AI provider returned HTTP {response.status_code}: {response.text[:500]}")
    data = response.json()
    content = data.get("choices", [{}])[0].get("message", {}).get("content", "")
    if not content.strip():
        raise RuntimeError("The AI provider returned an empty response.")
    return content, []
