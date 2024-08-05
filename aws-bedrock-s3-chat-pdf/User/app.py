import boto3
import streamlit as st
import os
import uuid

from langchain_community.embeddings import BedrockEmbeddings
from langchain.llms.bedrock import Bedrock
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS

# Boto3 - S3 Client

s3_client = boto3.client("s3")

BUCKET_NAME = os.getenv("BUCKET_NAME")

# Boto3 - Bedrock client

bedrock_client = boto3.client(service_name="bedrock-runtime", region_name="us-east-1")

bedrock_embeddings = BedrockEmbeddings(model_id="amazon.titan-embed-text-v1", client=bedrock_client)

folderpath = "/tmp/"

def get_uuid():
    return str(uuid.uuid4())

def load_index():
    s3_client.download_file(Bucket=BUCKET_NAME, Key="my_faiss.faiss", Filename=f"{folderpath}my_faiss.faiss")
    s3_client.download_file(Bucket=BUCKET_NAME, Key="my_faiss.pkl", Filename=f"{folderpath}my_faiss.pkl")

def get_llm():
    llm = Bedrock(
        model_id="amazon.titan-text-lite-v1", 
        client=bedrock_client, 
        model_kwargs={'maxTokenCount': 512}
    )

    return llm

def get_response(llm, vectorstore, question):
    prompt_template = """

    Human: Please use the given context to provide concise answer to the question
    If you do not know the answer, just say that you dont know, dont try to make up an answer.
    <context>
    {context}
    </context>

    Question: {question}

    Assistant: """

    PROMPT = PromptTemplate(
        template=prompt_template, input_variables=["context", "question"]
    )

    qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vectorstore.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 5}
        ),
        return_source_documents=True,
        chain_type_kwargs={"prompt": PROMPT}
    )  
    answer=qa({"query": question})
    return answer['result']
    
def main():
    st.header("Chat with your PDF using GenAI")

    load_index()

    dir_list = os.listdir(folderpath)
    st.write(f"File and directories in {folderpath}")
    st.write(dir_list)

    faiss_index = FAISS.load_local(
        index_name = "my_faiss",
        folder_path = folderpath,
        embeddings = bedrock_embeddings,
        allow_dangerous_deserialization = True
    )

    st.write("Index is Ready")
    question = st.text_input("Please ask your question")

    if st.button("Ask Question"):
        with st.spinner("Querying..."):

            llm = get_llm()

            st.write(get_response(llm, faiss_index, question))
            st.success("Done")

if __name__ == "__main__":
    main()
