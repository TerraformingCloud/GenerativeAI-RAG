# Source:Below code is provided by Streamlit and AWS 

#1 import streamlit and chatbot file
import streamlit as st 
from streamlit_extras.add_vertical_space import add_vertical_space
import backend as demo  #**Import your Chatbot file as demo

#2 Set Title for Chatbot - https://docs.streamlit.io/library/api-reference/text/st.title
st.title("Your personal AI assistant :speech_balloon:") # **Modify this based on the title you want in want

#3 LangChain memory to the session cache - Session State - https://docs.streamlit.io/library/api-reference/session-state
if 'memory' not in st.session_state: 
    st.session_state.memory = demo.demo_memory() #** Modify the import and memory function() attributes initialize the memory

#4 Add the UI chat history to the session cache - Session State - https://docs.streamlit.io/library/api-reference/session-state
if 'chat_history' not in st.session_state: #see if the chat history hasn't been created yet
    st.session_state.chat_history = [] #initialize the chat history

#5 Re-render the chat history (Streamlit re-runs this script, so need this to preserve previous chat messages)
for message in st.session_state.chat_history: 
    with st.chat_message(message["role"]):
        st.markdown(message["text"]) 

with st.sidebar:
    st.title('💬 LLM Chat App')
    st.markdown('''
    ## About
    This app is an LLM-powered chatbot built using:
    - [Streamlit](https://streamlit.io/)
    - [LangChain](https://python.langchain.com/)
    - [Claude/Anthropic](https://www.anthropic.com/claude) LLM model
 
    ''')
    add_vertical_space(5)
    st.write('Made for VamsiOrg')
 

#6 Enter the details for chatbot input box 
     
input_text = st.chat_input("Powered by Amazon Bedrock and Claude Anthropic") # **display a chat input box
if input_text: 
    with st.chat_message("user"): 
        st.spinner('Thinking...')
        st.markdown(input_text) 
    
    st.session_state.chat_history.append({"role":"user", "text":input_text}) 

    chat_response = demo.demo_conversation(input_text=input_text, memory=st.session_state.memory) #** replace with ConversationChain Method name - call the model through the supporting library
    
    with st.chat_message("assistant"):
      st.markdown(chat_response) 
    
    st.session_state.chat_history.append({"role":"assistant", "text":chat_response}) 