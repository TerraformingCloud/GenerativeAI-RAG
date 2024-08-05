import streamlit as st
from streamlit_extras.add_vertical_space import add_vertical_space
from langchain_aws import BedrockLLM

# Reference: https://docs.streamlit.io/knowledge-base/tutorials/llm-quickstart
st.title('🤖 Chat with an AI Bot')
#st.caption("Powered by Amazon Bedrock, Langchain and Redis")

add_vertical_space(1)


def generate_responses(input_text):
    llm = BedrockLLM(
      credentials_profile_name="default",
      model_id=model_id
    )
    st.info(llm(input_text))

with st.sidebar:
    st.subheader('LLM Chat App',  divider="rainbow")
    st.markdown('''
    ## About
    This app is Powered by:
    - [:red[🎈 Streamlit]](https://streamlit.io/)
    - [:green[🦜🔗 LangChain]](https://python.langchain.com/)
    - [:orange[☁️ Amazon Bedrock]](https://aws.amazon.com/bedrock/) LLM model
 
    ''')
    add_vertical_space(3)
    st.write('From the Platform Engineering Team.')

model_id = st.selectbox(
    "Select a Chat Model",
    ("amazon.titan-text-lite-v1", "anthropic.claude-v2:1", "cohere.command-light-text-v14"),
    index=0,
    placeholder="Choose an LLM Model..."
)

st.write("Selected model:", model_id)
 
with st.form('my_form'):
    text = st.text_area(label='',placeholder="Enter your query here.")
    # text = st.text_area(
    #     'Chat is powered by Amazon Bedrock')

    submitted = st.form_submit_button('Submit', type="primary")
    if submitted:
        generate_responses(text)