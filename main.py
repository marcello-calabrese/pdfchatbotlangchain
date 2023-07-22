import pandas as pd
import numpy as np

import streamlit as st
from PyPDF2 import PdfReader
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import plotly.express as px
from stopword_helper import get_stopwords

from utils import extract_keywords, embed_text, extract_text_from_pdf, get_answer, get_basic_stats


## setting the page layout to wide

st.set_page_config(layout="wide", page_title="PDF Chatbot Dashboard")

# title of the app

st.title("PDF Chatbot Dashboard :parrot:")

st.success("This is a dashboard to help you navigate through your PDF files. You can upload the pdf file, ask questions about it and get answers from the chatbot. You can also get a wordcloud of the most used words in the pdf file and a chart with the top ten keywords.")

st.header("First of all. Upload your PDF file here")

# Add a file uploader to the first column
pdf = st.file_uploader("Upload your PDF file", type="pdf")

# Create 2 columns in streamlit
col1, col2 = st.columns(2)




with col1:
    st.markdown(''' ### In this section you can :green[use the chatbot to ask questions] about the pdf file. Upload the file first!!''')
    
    if pdf is not None:
        # create a pdf reader object
        
        index = embed_text(extract_text_from_pdf(pdf))
        
        query = st.text_area("Ask a question about the pdf file")
        
        button = st.button("Get answer")
        
        if button:
            # make a spinner
            with st.spinner("Thinking..."):
                
                    
                st.write(get_answer(index, query))
                
                                                          

with col2:
    st.markdown('''### In this section you can have basic statistics of the pdf, :red[visualize the wordcloud] and main keywords of the file in a nice bar chart. Upload the file first!!''')
    if pdf is not None:
        # create a pdf reader object
        pdf_reader = PdfReader(pdf)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
       
        # create a pandas dataframe with the basic statistics of the pdf file: number of pages, number of words, number of characters, number of sentences
        
        st.markdown(''' #### :green[Basic statistics of the PDF file]''')
        
        if st.button("Get basic statistics of the PDF file"):
                
                              
                # Call function to get the basic statistics of the pdf file
                
                basic_stats = get_basic_stats(text)
                
                # Create a pandas dataframe with the basic statistics of the pdf file
                
                df = pd.DataFrame(basic_stats, index=['Value'])
                
                # transpose the dataframe
                
                df = df.T
                
                # display the dataframe
                
                st.table(df)
        
        
        # create a wordcloud of the text and show in streamlit
        
        st.markdown(''' #### :green[Wordcloud of the PDF file]''')
        if st.button("Generate Wordcloud", ):
            
            stopwords_set = get_stopwords('english ')
        
            wordcloud = WordCloud(background_color='white', stopwords=stopwords_set, min_word_length=3).generate(text)
            
           # Create a figure and axes
            fig, ax = plt.subplots()

            # Set the figure background color to white
            fig.set_facecolor('white')

            # Display the word cloud
            ax.imshow(wordcloud, interpolation='bilinear')
            ax.axis('off')
            
            st.pyplot(fig)
            
        
        # Create a chart with top ten keywords and their frequency in the document
        
        st.markdown(''' #### :green[Top 10 keywords and their frequency in the PDF file]''')
            
        if st.button('Get top 10 keywords and their frequency'):
        
        # create a function to get the top 10 keywords and their frequency in the document
              
                
                keywords = extract_keywords(text)
                
                # Display top keywords and frequencies in a chart with plotly express
                
                df = pd.DataFrame(keywords, columns=['keywords', 'count'])
                
                fig = px.bar(df, x='keywords', y='count', title='Top 10 keywords and their frequency in the PDF file')
                
                st.plotly_chart(fig)
                
       

    
        