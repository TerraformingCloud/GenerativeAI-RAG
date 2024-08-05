import os
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import BedrockEmbeddings
from langchain.vectorstores import FAISS
from langchain.indexes import VectorstoreIndexCreator
from langchain.llms.bedrock import Bedrock


def hr_index():
  data_load = PyPDFLoader('https://www.upl-ltd.com/images/people/downloads/Leave-Policy-India.pdf')

  data_split = RecursiveCharacterTextSplitter(
    separators=["\n\n", " ", ""],
    chunk_size=100,
    chunk_overlap=10
  )

  # data_sample = 'Welcome to the most comprehensive AWS CDK - V2 on Udemy.'
  # data_split_test = data_split.split_text(data_sample)
  # print(data_split_test)

  data_embeddings = BedrockEmbeddings(
    credentials_profile_name='default',
    model_id='amazon.titan-embed-text-v1'
  )

  data_index = VectorstoreIndexCreator(
    text_splitter=data_split,
    embedding=data_embeddings,
    vectorstore_cls=FAISS
  )

  db_index = data_index.from_loaders(loaders=[data_load])

  return db_index


def hr_llm():
  llm=Bedrock(
    credentials_profile_name='default',
    model_id='anthropic.claude-v2:1',
    model_kwargs={
      "max_tokens_to_sample": 300,
      "temperature": 0.1,
      "top_p": 0.9})
  return llm

def hr_rag_response(index, question):
  rag_llm = hr_llm()
  hr_rag_query = index.query(question=question, llm=rag_llm)
  return hr_rag_query

