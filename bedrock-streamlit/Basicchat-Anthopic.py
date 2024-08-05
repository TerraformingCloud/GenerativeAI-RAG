import streamlit as st
from streamlit_extras import add_vertical_space
import dotenv
import boto3

import os
import random
import json

dotenv.load_dotenv()

# Reference: https://docs.streamlit.io/knowledge-base/tutorials/build-conversational-apps
st.title('🤖 Chat Bot')
st.subheader("Powered by Amazon Berock with Anthropic Claude v2",
             divider="rainbow")

with st.sidebar:
    st.subheader('🦜💬 LLM Chat App',  divider="rainbow")
    st.markdown('''
    ## About
    This app is Powered by:
    - [:red[🎈 Streamlit]](https://streamlit.io/)
    - [:green[🦜🔗 LangChain]](https://python.langchain.com/)
    - [:orange[☁️ Amazon Bedrock]](https://aws.amazon.com/bedrock/) LLM model
 
    ''')
    #add_vertical_space(3)
    st.write('From the Platform Engineering Team.')

@st.cache_data
def get_welcome_message() -> str:
    return random.choice(
        [
            "Hello there! How can I assist you today?",
            "Hi there! Is there anything I can help you with?",
            "Do you need help?",
        ]
    )


@st.cache_resource
def get_bedrock_client():
    return boto3.client(service_name='bedrock-runtime', region_name='us-east-1')


def get_history() -> str:
    hisotry_list = [
        f"{record['role']}: {record['content']}" for record in st.session_state.messages
    ]
    return '\n\n'.join(hisotry_list)


client = get_bedrock_client()
modelId = 'anthropic.claude-v2:1'
accept = 'application/json'
contentType = 'application/json'


welcome_message = get_welcome_message()
with st.chat_message('assistant'):
    st.markdown(welcome_message)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    display_role = 'user'
    if message['role'] == 'Assistant':
        display_role = 'assistant'

    with st.chat_message(display_role):
        st.markdown(message["content"])


def parse_stream(stream):
    full_response = ""
    for event in stream:
        chunk = event.get('chunk')
        if chunk:
            message = json.loads(chunk.get('bytes').decode())[
                'completion'] or ""
            full_response += message
            yield message
    st.session_state.messages.append(
        {"role": "Assistant", "content": full_response}
    )


if prompt := st.chat_input("Ask your question"):
    st.session_state.messages.append({"role": "Human", "content": prompt})
    with st.chat_message("Human"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        history = get_history()
        body = json.dumps({
            "prompt": f"{history}\n\nAssistant:",
            "max_tokens_to_sample": 300,
            "temperature": 0.1,
            "top_p": 0.9,
        })
        response = client.invoke_model_with_response_stream(
            body=body,
            modelId=modelId,
        )
        stream = response.get('body')
        if stream:
            # st.write_stream is introduced in streamlit v1.31.0
            st.write_stream(parse_stream(stream))


if DEBUG := os.getenv("DEBUG", False):
    st.subheader("History", divider="rainbow")
    history_list = [
        f"{record['role']}: {record['content']}" for record in st.session_state.messages
    ]
    st.write(history_list)