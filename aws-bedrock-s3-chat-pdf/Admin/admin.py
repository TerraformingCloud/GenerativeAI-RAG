import boto3
import streamlit as st
import os
import uuid

from langchain_community.embeddings import BedrockEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS

# Boto3 - S3 Client

s3_client = boto3.client("s3")

BUCKET_NAME = os.getenv("BUCKET_NAME")

# Boto3 - Bedrock client

bedrock_client = boto3.client(service_name="bedrock-runtime", region_name="us-east-1")

bedrock_embeddings = BedrockEmbeddings(model_id="amazon.titan-embed-text-v1", client=bedrock_client)


# Get UUID

def get_uuid():
    return str(uuid.uuid4())


# Split the pages/text into chunks

def text_splitter(pages, chunk_size, chunk_overlap):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )
    docs = text_splitter.split_documents(pages)
    return docs


# Create a Vector store 

def vector_db(request_id, documents):
    faiss_db = FAISS.from_documents(documents, bedrock_embeddings)
    filename = f"{request_id}.bin"
    folderpath = "/tmp"
    faiss_db.save_local(index_name=filename, folder_path=folderpath)

    # Upload docs to S3 bucket
    s3_client.upload_file(Filename=folderpath + "/" + filename + ".faiss", Bucket=BUCKET_NAME, Key="my_faiss.faiss")
    s3_client.upload_file(Filename=folderpath + "/" + filename + ".pkl", Bucket=BUCKET_NAME, Key="my_faiss.pkl")

    return True


def main():
    st.write("Chat with your PDF")
    uploaded_file = st.file_uploader("Upload your PDF file")
    if uploaded_file is not None:
        request_id = get_uuid()
        st.write(f"Request Id: {request_id}")
        saved_filename = f"{request_id}.pdf"

        with open(saved_filename, mode="wb") as f:
            f.write(uploaded_file.getvalue())

        loader = PyPDFLoader(saved_filename)
        pages = loader.load_and_split()

        st.write(f"Total pages: {len(pages)}")

        # Split text

        split_docs = text_splitter(pages, 1000, 200)
        st.write(f"Length of the split docs: {len(split_docs)}")
        # st.write("================================================")
        # st.write(split_docs[0])
        # st.write("================================================")
        # st.write(split_docs[1])


        st.write("Creating a vector db")
        result = vector_db(request_id, split_docs)

        if result:
            st.write("PDF has been processed successfully!!!")
        else:
            st.write("!!! Error processing the PDF")



if __name__ == "__main__":
    main()
