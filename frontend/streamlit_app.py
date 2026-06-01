import requests
import streamlit as st


API_URL = "http://localhost:8000/api/chat"
EVALUATION_URL = "http://localhost:8000/api/evaluate"

# Default value so app never fails even if sidebar changes
top_k = 3


st.set_page_config(
    page_title="Enterprise Knowledge Assistant",
    page_icon="🤖",
    layout="wide"
)

st.title("Enterprise Knowledge Assistant")
st.caption(
    "RAG based enterprise document Q&A assistant using FastAPI, Qdrant, embeddings and Groq"
)

if "messages" not in st.session_state:
    st.session_state.messages = []


with st.sidebar:
    st.header("Settings")

    top_k = st.slider(
        "Number of document chunks to retrieve",
        min_value=1,
        max_value=10,
        value=3
    )

    st.markdown("### Sample Questions")
    st.markdown("- Who approves purchase orders above 50000 dollars?")
    st.markdown("- How many days of annual leave are employees eligible for?")
    st.markdown("- When should employees return company laptop?")
    st.markdown("- What is the domestic travel meal reimbursement limit?")
    st.markdown("- Who can perform machine maintenance?")

    st.markdown("---")
    st.header("Evaluation")

    if st.button("Run RAG Evaluation"):
        with st.spinner("Running evaluation on golden questions..."):
            try:
                eval_response = requests.post(
                    EVALUATION_URL,
                    timeout=300,
                )
                eval_response.raise_for_status()
                eval_data = eval_response.json()

                summary = eval_data.get("summary", {})

                st.success(f"Evaluation Status: {summary.get('status')}")

                col1, col2 = st.columns(2)

                with col1:
                    st.metric("Overall Score", summary.get("average_overall_score"))
                    st.metric("Source Match", summary.get("average_source_match_score"))

                with col2:
                    st.metric("Keyword Score", summary.get("average_keyword_score"))
                    st.metric("Answer Present", summary.get("average_answer_present_score"))

                with st.expander("View Detailed Evaluation Results"):
                    for item in eval_data.get("results", []):
                        st.markdown(f"**Question:** {item.get('question')}")
                        st.markdown(f"**Expected Source:** {item.get('expected_source')}")
                        st.markdown(f"**Overall Score:** {item.get('overall_score')}")
                        st.markdown(f"**Answer:** {item.get('answer')}")
                        st.divider()

            except Exception as error:
                st.error(f"Evaluation failed: {str(error)}")


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


user_question = st.chat_input("Ask a question from enterprise documents...")

if user_question:
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_question
        }
    )

    with st.chat_message("user"):
        st.markdown(user_question)

    with st.chat_message("assistant"):
        with st.spinner("Searching documents and generating answer..."):
            try:
                response = requests.post(
                    API_URL,
                    json={
                        "question": user_question,
                        "top_k": top_k
                    },
                    timeout=180
                )

                response.raise_for_status()
                data = response.json()

                answer = data.get("answer", "No answer returned.")
                sources = data.get("sources", [])

                st.markdown(answer)

                if sources:
                    st.markdown("### Sources")
                    for source in sources:
                        st.markdown(
                            f"- **{source.get('document_name')}**, "
                            f"Chunk: {source.get('chunk_number')}, "
                            f"Score: {round(source.get('score', 0), 4)}"
                        )

                with st.expander("View retrieved chunks"):
                    for chunk in data.get("retrieved_chunks", []):
                        st.markdown(f"**Document:** {chunk.get('document_name')}")
                        st.markdown(f"**Chunk:** {chunk.get('chunk_number')}")
                        st.markdown(chunk.get("chunk_text"))
                        st.divider()

                assistant_message = answer

            except Exception as error:
                assistant_message = f"Error: {str(error)}"
                st.error(assistant_message)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": assistant_message
        }
    )