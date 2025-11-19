import streamlit as st
import tempfile
import os

# UI setup
st.set_page_config(page_title="FinQuery", layout="wide")
st.title("FinQuery — AI Financial PDF Analyzer")
st.write("Upload a financial PDF report and get summary, competitors, revenue charts and Q&A.")

# Try to import your analyzer function
try:
    from finquery.analyzer import analyze_pdf
except Exception as e:
    st.error("Could not import analyze_pdf from finquery/analyzer.py. Please check the function name.")
    st.stop()

# Upload PDF
uploaded = st.file_uploader("Upload PDF", type=["pdf"])

if uploaded:
    with st.spinner("Analyzing PDF..."):
        temp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
        temp.write(uploaded.getvalue())
        temp.close()

        try:
            result = analyze_pdf(temp.name)
        except Exception as e:
            st.error(f"Analyzer error: {e}")
            st.stop()

    # Display results
    st.header("Summary")
    st.write(result.get("summary", "No summary returned."))

    st.header("Competitors")
    comps = result.get("competitors")
    if comps:
        st.table(comps)
    else:
        st.write("No competitor data returned.")

    st.header("Revenue Chart")
    chart = result.get("revenue_chart_path")
    if chart and os.path.exists(chart):
        st.image(chart)
    else:
        st.write("No chart found.")

    st.header("Q&A")
    q = st.text_input("Ask something about this PDF:")
    if q:
        answer = result.get("qa", {}).get(q, "Answer not found.")
        st.write(answer)

    os.unlink(temp.name)
