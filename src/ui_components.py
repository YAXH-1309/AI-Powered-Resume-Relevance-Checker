import streamlit as st

def display_analysis_results(results):
    """Renders the analysis results in a professional dashboard format."""
    
    if "raw" in results:
        st.error("There was an issue parsing the AI's response.")
        st.code(results["raw"])
        return

    st.subheader("Relevance Analysis Dashboard")

    # Top Row: Score and Verdict
    col1, col2 = st.columns(2)
    with col1:
        score = results.get("relevance_score", 0)
        st.metric(label="Relevance Score", value=f"{score}%")
        st.progress(score)
    with col2:
        verdict = results.get("fit_verdict", "N/A")
        st.metric(label="Fit Verdict", value=verdict)

    # Summary
    st.subheader("Candidate Summary")
    st.write(results.get("summary", "No summary provided."))

    # Details in Expanders
    with st.expander("📝 Personalized Feedback for Student"):
        st.success(results.get("feedback", "No feedback provided."))
    
    with st.expander("❌ Missing Skills & Experience"):
        missing_elements = results.get("missing_elements", [])
        if missing_elements:
            for item in missing_elements:
                st.warning(f"- {item}")
        else:
            st.info("No significant gaps identified.")