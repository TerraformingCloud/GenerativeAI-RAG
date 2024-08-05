import os
from langchain_community.document_loaders import PyPDFLoader

data_load = PyPDFLoader('https://www.upl-ltd.com/images/people/downloads/Leave-Policy-India.pdf')

data_test = data_load.load_and_split()

print(f"Total number of pages: {len(data_test)}")

print(data_test[0])

print("---------------------------------------------------------")

print(data_test[1])