from __future__ import division
from math import log10, sqrt
from string import punctuation
import os, nltk,docx
from nltk.stem import WordNetLemmatizer
  
lemmatizer = WordNetLemmatizer()
getLogs = True

def getText(filename):
    doc = docx.Document(filename)
    fullText = []
    for para in doc.paragraphs:
        fullText.append(para.text)
    return '\n'.join(fullText)
    
def compareDocument(TFIDF_weightvector_1, TFIDF_weightvector_2):
    TFIDF_weightvector_intersection = set(TFIDF_weightvector_1).intersection(set(TFIDF_weightvector_2))
    
    print("Intersection result: ")
    print(TFIDF_weightvector_intersection)
    TFIDF_weightvector_intersection_len = len(TFIDF_weightvector_intersection)

    TFIDF_weightvector_union = set()

    for tfidfweightvector_1 in TFIDF_weightvector_1:
        TFIDF_weightvector_union.add(tfidfweightvector_1)

    for tfidfweightvector_2 in TFIDF_weightvector_2:
        TFIDF_weightvector_union.add(tfidfweightvector_2)

    print("Union result:")
    print(TFIDF_weightvector_union)

    TFIDF_weightvector_union_len = len(TFIDF_weightvector_union)

    return TFIDF_weightvector_intersection_len / TFIDF_weightvector_union_len
    
if getLogs:
    print("Collecting files....")

file1 = input("file1:")
file2 = input("file2:")

text1 = getText(file1)
text2 = getText(file2)

#file1 = open(file1,'r')
#file2 = open(file2,'r')
#text1 = file1.read()
#text2 = file2.read()

tzr = nltk.tokenize.RegexpTokenizer(r'\w+')
unique_words1 = set(tzr.tokenize(text1))
unique_words2 = set(tzr.tokenize(text2))
unique_words_ns1 = []
unique_words_ns2 = []

print("Unique words:")
print(unique_words1)
print(unique_words2)

stopwords = nltk.corpus.stopwords.words('english')
for word in unique_words1:
    if word not in stopwords:
        unique_words_ns1.append(lemmatizer.lemmatize(word))
        
for word in unique_words2:
    if word not in stopwords:
        unique_words_ns2.append(lemmatizer.lemmatize(word))

if getLogs:
    print ('Unique words without stopwords and lemmatized:')
    print(unique_words_ns1)
    print(unique_words_ns2)


sim = compareDocument(unique_words_ns1, unique_words_ns2)
print ("\nJaccard similarity between given doc and", sim*100 , "%")

