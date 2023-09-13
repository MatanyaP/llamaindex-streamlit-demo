# 3.1. Import libraries
import streamlit as st
from llama_index import VectorStoreIndex, ServiceContext, Document
from llama_index.llms import OpenAI
import openai
from llama_index import SimpleDirectoryReader

# Initialize message history
openai.api_key = st.secrets.openai_key

st.header("Cambium Chatbot with LlamaIndex")

if "messages" not in st.session_state.keys():  # Initialize the chat message history
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Hi, I'm Cambium chatbot. Ask me about Cambium!",
        }
    ]


# 3.3. Load and index data
@st.cache_resource(show_spinner=False)  # Cache the data loading
def load_data():
    with st.spinner(text="Loading and indexing your data, keep it cool..."):
        reader = SimpleDirectoryReader(input_dir="./data", recursive=True)
        docs = reader.load_data()
        service_context = ServiceContext.from_defaults(
            llm=OpenAI(
                model="gpt-3.5-turbo",
                temperature=0.5,
                system_prompt="You are an expert in Cambium software company. Keep your answers informative and polite",
            )
        )
        index = VectorStoreIndex.from_documents(docs, service_context=service_context)
        return index


index = load_data()

# 3.4. Create the chat engine
chat_engine = index.as_chat_engine(chat_mode="condense_question", verbose=True)

# 3.5. Prompt for user input and display message history
if prompt := st.chat_input("Ask about Cambium"):
    st.session_state.messages.append({"role": "user", "content": prompt})

for message in st.session_state.messages:  # Display the prior chat messages
    with st.chat_message(message["role"]):
        st.write(message["content"])

# 3.6. Pass query to chat engine and display response
# If last message is not from assistant, generate a new response
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking about your question..."):
            response = chat_engine.chat(prompt)
            st.write(response.response)
            message = {"role": "assistant", "content": response.response}
            st.session_state.messages.append(message)  # Add response to message history
