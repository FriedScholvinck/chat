from openai import OpenAI
import streamlit as st


st.set_page_config(
    page_title="XomniaGPT",
    page_icon="assets/xomnia_logo.png",
)

st.title("XomniaGPT")

avatars = {
    'user': 'assets/programmer.png',
    'assistant': f'assets/xomnia_logo.png'
}

try:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
except:
    st.error("Please add your OpenAI API key to .streamlit/secrets.toml.")
    st.stop()

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello, I'm a your smart assistant."}
    ]

for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar=avatars[message["role"]]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="assets/programmer.png"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar=avatars[message["role"]]):
        message_placeholder = st.empty()
        full_response = ""
        for response in client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        ):
            full_response += (response.choices[0].delta.content or "")
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})
