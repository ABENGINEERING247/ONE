with right:
        st.markdown("### Export center")
        st.caption("Exports use the current saved manuscript. Save edits before downloading.")
        
        if st.button("Save before export", use_container_width=True):
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
