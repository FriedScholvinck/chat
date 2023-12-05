# from llama_index.llms import OpenAI
# import openai

import streamlit as st
from llama_index import (Document, ServiceContext, StorageContext,
                         VectorStoreIndex, load_index_from_storage)

DOMAIN = 'xomnia'
DATA_DIR = f'data/{DOMAIN}'
title = DOMAIN.title()

st.set_page_config(page_title='Chat', page_icon=f'assets/{DOMAIN}_logo.png', layout="centered", initial_sidebar_state="auto", menu_items=None)
st.title(f'{title} Chat')


# Initialize the chat messages history
if "messages" not in st.session_state.keys():
    st.session_state.messages = [
        {"role": "assistant", "content": f"Ask me a question about the website of {title}!"}
    ]

avatars = {
    'user': 'assets/programmer.png',
    'assistant': f'assets/{DOMAIN}_logo.png'
}

@st.cache_resource(show_spinner=False)
def load_data():
    with st.spinner(text="Loading indexed documents..."):
        # reader = SimpleDirectoryReader(input_dir="./data", recursive=True)
        # docs = reader.load_data()
        # service_context = ServiceContext.from_defaults(llm=OpenAI(model="gpt-3.5-turbo", temperature=0.5, system_prompt=f"You are an expert on the {name} website and your job is to answer technical questions. Assume that all questions are related to {name}. Keep your answers technical and based on facts – do not hallucinate features."))
        # index = VectorStoreIndex.from_documents(docs, service_context=service_context)


        # rebuild storage context
        storage_context = StorageContext.from_defaults(persist_dir=DATA_DIR)

        # load index
        index = load_index_from_storage(storage_context)
        return index



if "index" not in st.session_state:
    st.session_state.index = load_data()


if "chat_engine" not in st.session_state.keys(): # Initialize the chat engine
        st.session_state.chat_engine = st.session_state.index.as_chat_engine(chat_mode="condense_question", verbose=True)

if prompt := st.chat_input("Your question"): # Prompt for user input and save to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

for message in st.session_state.messages: # Display the prior chat messages
    with st.chat_message(message["role"], avatar=avatars[message["role"]]):
        st.write(message["content"])

# If last message is not from assistant, generate a new response
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant", avatar=avatars["assistant"]):
        with st.spinner("Thinking..."):
            response = st.session_state.chat_engine.chat(prompt)
            st.write(response.response)
            message = {"role": "assistant", "content": response.response}
            st.session_state.messages.append(message) # Add response to message history