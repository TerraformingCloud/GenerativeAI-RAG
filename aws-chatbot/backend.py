from langchain.chains import ConversationChain
from langchain.memory import ConversationSummaryBufferMemory
from langchain_aws import ChatBedrock

def demo_chatbot():
  demo_llm = ChatBedrock(
    credentials_profile_name='default',
    model_id='anthropic.claude-v2:1',
    model_kwargs={
      #"max_tokens_to_sample": 300,
      "temperature": 0.1,
      "top_p": 1,
      "stop_sequences": ["\n\nHuman:"]
    })

  return demo_llm

# response = demo_chatbot(input_text="Tell me a joke.")
# print(response)

def demo_memory():
  llm_data= demo_chatbot()
  memory = ConversationSummaryBufferMemory(
    llm=llm_data,
    max_token_limit=300
  )
  return memory

def demo_conversation(input_text,memory):
  llm_chain_data=demo_chatbot()
  llm_conversation = ConversationChain(
    llm=llm_chain_data,
    memory=memory,
    verbose=True
  )

  chat_reply = llm_conversation.invoke(input_text)
  return chat_reply['response']