import streamlit as st
from pathlib import Path
from services.config import APP_NAME, APP_TAGLINE
from services.storage import init_db, create_project, list_projects, save_project, load_project
from services.research import generate_research, demo_research
from services.exporter import docx_bytes, pdf_bytes, latex_source, project_zip
from components.ui import apply_theme, render_header, render_sidebar, render_chatbot

st.set_page_config(page_title=APP_NAME, page_icon="📄", layout="wide", initial_sidebar_state="expanded")
apply_theme()
init_db()
render_header()

with st.sidebar:
    render_sidebar()
    st.divider()
    mode = st.radio("Generation mode", ["Demo Mode", "API Mode"], help="Demo mode works without credentials. API mode uses your configured provider.")
    api_provider = st.selectbox("AI provider", ["OpenAI-compatible API"], disabled=(mode == "Demo Mode"))
    model = st.text_input("Model name", value=st.secrets.get("OPENAI_MODEL", "gpt-4.1-mini") if hasattr(st, "secrets") else "gpt-4.1-mini", disabled=(mode == "Demo Mode"))
    st.caption("API keys stay server-side in Streamlit secrets.")

projects = list_projects()
with st.sidebar:
    st.subheader("Your projects")
    if projects:
        project_options = {f"{p['title']} · {p['updated_at']}": p["id"] for p in projects}
        chosen_label = st.selectbox("Open a saved project", list(project_options.keys()), label_visibility="collapsed")
        if st.button("Load selected project", use_container_width=True):
            loaded = load_project(project_options[chosen_label])
            if loaded:
                st.session_state["active_project"] = loaded
                st.rerun()
    else:
        st.caption("Your saved projects will appear here.")

if "active_project" not in st.session_state:
    st.session_state["active_project"] = {"id": None, "title": "", "idea": "", "paper": "", "sources": [], "status": "Draft"}
project = st.session_state["active_project"]

st.markdown('<div class="hero"><div class="eyebrow">AUTONOMOUS RESEARCH WORKSPACE</div><h1>Your idea.<br><span>A complete research paper.</span></h1><p>ONE turns a research idea into an editable, evidence-aware manuscript—with academic structure, citations, LaTeX, and professional exports.</p></div>', unsafe_allow_html=True)

with st.container(border=True):
    st.markdown("#### Start with just one idea")
    idea = st.text_area("Research idea", value=project.get("idea", ""), height=110,
                        placeholder="Example: Develop an AI-powered traffic collision prediction system using computer vision and intelligent transportation analytics.",
                        label_visibility="collapsed")
    col1, col2 = st.columns([1, 3])
    with col1:
        generate_clicked = st.button("✦ Generate my paper", type="primary", use_container_width=True)
    with col2:
        st.caption("ONE will plan, draft, review, and format your manuscript. You can edit every section before exporting.")

if generate_clicked:
    if len(idea.strip()) < 12:
        st.warning("Please enter a little more detail so ONE can understand your research idea.")
    else:
        with st.status("ONE is building your research manuscript…", expanded=True) as status:
            st.write("1/4 · Creating research plan")
            st.write("2/4 · Drafting structured manuscript")
            st.write("3/4 · Checking references and evidence")
            st.write("4/4 · Preparing editable outputs")
            try:
                if mode == "API Mode":
                    paper, sources = generate_research(idea, model=model)
                else:
                    paper, sources = demo_research(idea)
                title = next((line.replace("#", "").strip() for line in paper.splitlines() if line.startswith("# ")), "ONE Research Project")
                project = {"id": project.get("id"), "title": title[:160], "idea": idea, "paper": paper, "sources": sources, "status": "Generated"}
                project["id"] = create_project(project) if not project["id"] else save_project(project)
                st.session_state["active_project"] = project
                status.update(label="Research draft created", state="complete", expanded=False)
            except Exception as exc:
                status.update(label="Generation could not be completed", state="error")
                st.error(str(exc))

project = st.session_state["active_project"]
if project.get("paper"):
    st.divider()
    st.markdown("## Research workspace")
    left, right = st.columns([1.65, 1])
    
    with left:
        st.markdown("### Manuscript editor")
        new_title = st.text_input("Project title", value=project.get("title", "ONE Research Project"))
        edited = st.text_area("Edit the complete manuscript (Markdown)", value=project.get("paper", ""), height=560,
                              help="Edit the text directly. Use Markdown headings (#, ##, ###) for structure.")
        if st.button("Save manuscript changes", type="primary", key="save_manuscript_btn"):
            project["title"], project["paper"] = new_title, edited
            project["status"] = "Edited"
            save_project(project)
            st.session_state["active_project"] = project
            st.success("Manuscript saved.")
            
        with st.expander("Research sources and verification notes"):
            if project.get("sources"):
                for i, source in enumerate(project["sources"], 1):
                    st.markdown(f"**{i}. {source.get('title', 'Source')}**")
                    if source.get("url"):
                        st.markdown(f"[Open source]({source['url']})")
                    st.caption(source.get("note", ""))
            else:
                st.info("No external sources were retrieved for this draft. Add and verify sources before relying on factual claims.")
                
    with right:
        st.markdown("### Export center")
        st.caption("Exports use the current saved manuscript. Save edits before downloading.")
        
        if st.button("Save before export", use_container_width=True, key="save_before_export_btn"):
            project["title"], project["paper"] = new_title, edited
            save_project(project)
            st.session_state["active_project"] = project
            st.success("Saved.")
            
        st.divider()
        
        # --- Formatting Standard Selection ---
        st.markdown("#### Formatting options")
        format_standard = st.selectbox(
            "Select Formatting Standard",
            ["Standard / General", "IEEE Standard", "APA 7th Edition"],
            help="Choose standard styling specifications for your exports (font family, line spacing, margins, section headers)."
        )
        
        # Mapping selected standard to internal parameter
        std_key = "Standard"
        if "IEEE" in format_standard:
            std_key = "IEEE"
        elif "APA" in format_standard:
            std_key = "APA"
            
        # Display Helpful Formatting Hints
        with st.expander("ℹ️ View formatting hints & guidelines"):
            if std_key == "IEEE":
                st.info("""
                **IEEE Standard Guidelines:**
                - **Font:** 10 pt Times New Roman.
                - **Margins:** Top/Bottom: 0.75", Left/Right: 0.625".
                - **Layout:** Compact layout, single or double column compatible.
                - **Headings:** Roman numerals for main headings (I., II., etc.).
                """)
            elif std_key == "APA":
                st.info("""
                **APA 7th Edition Guidelines:**
                - **Font:** 12 pt Times New Roman (or 11 pt Calibri).
                - **Line Spacing:** Double-spaced text throughout.
                - **Margins:** 1-inch (2.54 cm) on all sides.
                - **Structure:** Title page, abstract, main text, and references.
                """)
            else:
                st.info("""
                **Standard / General Formatting:**
                - **Font:** 11 pt Calibri / Helvetica.
                - **Line Spacing:** 1.15 line spacing with 6 pt paragraph spacing.
                - **Margins:** Standard 1-inch margins.
                - **Best for:** General proposals, corporate reports, and drafts.
                """)

        st.divider()
        st.markdown("#### Downloads")
        
        current = edited
        try:
            st.download_button(
                "⬇ Download Word (.docx)", 
                data=docx_bytes(new_title, current, style_standard=std_key), 
                file_name=f"ONE_{std_key}_paper.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document", 
                use_container_width=True,
                help="Download fully styled Microsoft Word document."
            )
            st.download_button(
                "⬇ Download PDF", 
                data=pdf_bytes(new_title, current, style_standard=std_key), 
                file_name=f"ONE_{std_key}_paper.pdf",
                mime="application/pdf", 
                use_container_width=True,
                help="Download ready-to-print formatted PDF."
            )
            st.download_button(
                "⬇ Download LaTeX (.tex)", 
                data=latex_source(new_title, current, style_standard=std_key), 
                file_name=f"ONE_{std_key}_paper.tex",
                mime="application/x-tex", 
                use_container_width=True,
                help="Download LaTeX source code with appropriate document class."
            )
            st.download_button(
                "⬇ Download project ZIP", 
                data=project_zip(new_title, current, project.get("sources", []), style_standard=std_key),
                file_name="ONE_research_project.zip", 
                mime="application/zip", 
                use_container_width=True
            )
        except Exception as exc:
            st.error(f"Export error: {exc}")
            
        st.markdown("### Quality checklist")
        st.checkbox("Research question is clear", key="qc_question")
        st.checkbox("Sources and citations have been checked", key="qc_sources")
        st.checkbox("Methods and findings reflect real evidence", key="qc_evidence")
        st.checkbox("Final manuscript reviewed by a human", key="qc_review")
        st.caption("Checklist items are reminders, not a certification of research quality.")

render_chatbot(project, mode)
st.markdown('<div class="footer">ONE — AI Research Agent · Designed and developed by Engr. Bilal Mehmood<br>Generative AI · Agentic AI · Scientific Research · Intelligent Automation</div>', unsafe_allow_html=True)
