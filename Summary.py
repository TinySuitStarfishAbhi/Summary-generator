import streamlit as st
import bs4 as bs
import re
import urllib.request
import heapq
import nltk

st.title("Generate a simple summary. ")

input_link = st.text_input("Enter a Wikipedia Link!")
gen_sent = st.number_input("Enter number of sentences", value=0, step=1)

try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('tokenizers/stopwords')
except LookupError:
    nltk.download('punkt')
    nltk.download('tokenizers/stopwords')

if(input_link==""):
    st.write("Hello! Enter a valid Wikipedia URL to get started!")
else:
    scraped_data = urllib.request.urlopen(input_link)
    article = scraped_data.read()

    parsed_article = bs.BeautifulSoup(article,'lxml')
    paragraphs = parsed_article.find_all('p')

    article_text = ""
    for p in paragraphs:
        article_text += p.text

    article_text = re.sub(r'\[[0-9]*\]', ' ', article_text)
    article_text = re.sub(r'\s+', ' ', article_text)

    formatted_article_text = re.sub('[^a-zA-Z]', ' ', article_text )
    formatted_article_text = re.sub(r'\s+', ' ', formatted_article_text)

    sentence_list = nltk.sent_tokenize(article_text)

    stopwords = nltk.corpus.stopwords.words('english')
    word_frequencies = {}
    for word in nltk.word_tokenize(formatted_article_text):
        if word not in stopwords:
            if word not in word_frequencies.keys():
                word_frequencies[word] = 1
            else:
                word_frequencies[word] += 1

    maximum_frequncy = max(word_frequencies.values())

    for word in word_frequencies.keys():
        word_frequencies[word] = (word_frequencies[word]/maximum_frequncy)

    sentence_scores = {}
    for sent in sentence_list:
        for word in nltk.word_tokenize(sent.lower()):
            if word in word_frequencies.keys():
                if len(sent.split(' ')) < 25:
                    if sent not in sentence_scores.keys():
                        sentence_scores[sent] = word_frequencies[word]
                    else:
                        sentence_scores[sent] += word_frequencies[word]

    summary_sentences = heapq.nlargest(int(gen_sent), sentence_scores, key=sentence_scores.get)

    summary = ' '.join(summary_sentences)
    st.markdown("**Here's the summary** -")
    st.write(summary)
