import streamlit as st
import re
from collections import Counter
# import the pypdf2 library
from PyPDF2 import PdfReader
from open_ai_key import OPENAI_API_KEY
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain import OpenAI
from langchain.document_loaders import PyPDFLoader
from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chains.question_answering import load_qa_chain
from stopword_helper import get_stopwords

st.cache()
def get_basic_stats(text):
                    
                    # i want to create a dictionary to store the basic statistics of the pdf file
                    
                    basic_stats = {}
                    
                                        
                    # i want to count the number of words in the pdf file
                    
                    basic_stats['Number of words'] = len(text.split())
                    
                    # i want to count the number of characters in the pdf file
                    
                    basic_stats['Number of characters'] = len(text)
                    
                    # i want to count the number of sentences in the pdf file
                    
                    basic_stats['Number of sentences'] = len(text.split('.'))
                    
                    return basic_stats




st.cache()
def extract_keywords(text):
    text = re.sub(r'\s+', ' ', text)  # Remove extra spaces
    words = re.findall(r'\w+', text.lower())  # Extract words
    stopwords_set = get_stopwords('english ')
    stopwords = stopwords_set  # stop words from nltk
    keywords = [word for word in words if word not in stopwords]  # Remove stop words
    return Counter(keywords).most_common(10)  # Get top 10 keywords with their frequencies

st.cache()
def extract_text_from_pdf(pdf_path):
        """
        Extracts text from a PDF file and returns it as a string.

        Parameters:
            pdf_path (str): The file path of the PDF to be read.

        Returns:
            str: The extracted text from the PDF.
        """
        pdf_reader = PdfReader(pdf_path)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text

st.cache()    
def embed_text(text):
        """Split the text and embed it in a FAISS vector store"""
        text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800, chunk_overlap=0, separators=["\n\n", ".", "?", "!", " ", ""])
        
        texts = text_splitter.split_text(text)

        embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
        index = FAISS.from_texts(texts, embeddings)

        return index

st.cache()
def get_answer(index, query):
        """Returns answer to a query using langchain QA chain"""

        docs = index.similarity_search(query)

        chain = load_qa_chain(OpenAI(temperature=0, openai_api_key=OPENAI_API_KEY))
        answer = chain.run(input_documents=docs, question=query)

        return answer