import streamlit as st

from rag import ask_rag

st.set_page_config(
    page_title="PDF RAG Assistant",
    page_icon="📄",
    layout="wide",
)

st.title(
    "📄 PDF RAG Assistant"
)

st.markdown(
    """
Multi-turn PDF Question Answering

Pipeline:

PDF → Chunking → Embeddings → FAISS → Memory → Gemini
"""
)

if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------------------
# Render Chat History
# ---------------------

for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):
        st.markdown(
            message["content"]
        )

# ---------------------
# Chat Input
# ---------------------

prompt = st.chat_input(
    "Ask a question about your PDF"
)

if prompt:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt,
        }
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.spinner(
        "Thinking..."
    ):
        result = ask_rag(prompt)

    answer = result["answer"]

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer,
        }
    )

    with st.chat_message(
        "assistant"
    ):
        st.markdown(answer)

        with st.expander(
            "Retrieved Chunks"
        ):
            for idx, chunk in enumerate(
                result["chunks"],
                start=1
            ):
                st.markdown(
                    f"### Chunk {idx}"
                )

                st.write(chunk)

                st.divider()