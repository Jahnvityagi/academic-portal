from __future__ import division
from math import log10, sqrt
from string import punctuation
import os, nltk,docx

DATASET = 'Dataset/No Plagiarism'
getLogs = False

def getText(filename):
    doc = docx.Document(filename)
    fullText = []
    for para in doc.paragraphs:
        fullText.append(para.text)
    return '\n'.join(fullText)
    
def computeDFs(unique_words, list_of_assignment_files):
    list_of_df = []
    for unique_word in unique_words:
        counter = 0
        for assignment_file in list_of_assignment_files:
#            f = open(assignment_file, 'r')
#            all_text = f.read().replace('\n', ' ')
            all_text = getText(assignment_file).replace('\n', ' ')
            all_text = all_text.lower().replace("'", " ")
            if unique_word in all_text:
                counter += 1
        list_of_df.append(counter)
    return list_of_df

def computeTFIDF(assignment_file, unique_words, DFs, NUM_DOCS):
    list_of_TFIDFweightvector = []
#    f = open(assignment_file, 'r')
#    all_text = f.read().replace('\n', ' ').lower()
    all_text = getText(assignment_file).replace('\n', ' ').lower()
    for idx in range(0, len(unique_words)):
        TF = all_text.count(unique_words[idx]) / len(all_text.split())
        IDF = (log10(NUM_DOCS / (DFs[idx]+1)))
        weightVector = TF * IDF
        list_of_TFIDFweightvector.append(weightVector)

    return list_of_TFIDFweightvector

def compareDocument(TFIDF_weightvector_1, TFIDF_weightvector_2):
    dotProducts = 0

    for idx in range(0, len(TFIDF_weightvector_1)):
        dotProducts = dotProducts + (TFIDF_weightvector_1[idx] * TFIDF_weightvector_2[idx])

    magnitude_1 = 0
    for idx in range(0, len(TFIDF_weightvector_1)):
        magnitude_1 = magnitude_1 + (TFIDF_weightvector_1[idx] * TFIDF_weightvector_1[idx])

    magnitude_2 = 0
    for idx in range(0, len(TFIDF_weightvector_2)):
        magnitude_2 = magnitude_2 + (TFIDF_weightvector_2[idx] * TFIDF_weightvector_2[idx])

    if magnitude_1 == 0: # to avoid divide by zero error
        magnitude_1 = 0.000001
    if magnitude_2 == 0:
        magnitude_2 = 0.000001

    print("DOT PRODUCT: ", dotProducts)
    print("\n\nMAGNITUDES: ", magnitude_1, ", ",magnitude_2)

    return (dotProducts / (sqrt(magnitude_1) * sqrt(magnitude_2)))

if getLogs:
    print("Collecting files....")

assignment_files = []
for filename in os.listdir(DATASET):
    assignment_files.append(DATASET + '/' + filename)
    
if getLogs:
    print("Reading files....")
    
all_text = ""
for fname in assignment_files:
#    infile = open(fname, 'r')
#    lines = infile.read()
#    all_text += lines
    all_text += getText(fname)

if getLogs:
    print("Tokenizing words....")

all_text = all_text.replace('\n', ' ').lower()
tzr = nltk.tokenize.RegexpTokenizer(r'\w+')
unique_words = set(tzr.tokenize(all_text))
unique_words_no_stopwords = []

if getLogs:
    print("Removing stopwords....")

stopwords = nltk.corpus.stopwords.words('english')
for word in unique_words:
    if word not in stopwords:
        unique_words_no_stopwords.append(word)

if getLogs:
    print ('Unique words without stopwords:',unique_words_no_stopwords)


if getLogs:
    print("Computing DFs...")

DFs = computeDFs(unique_words_no_stopwords, assignment_files)

if getLogs:
    print("Computing TFIDFs...")

TFIDF_weightvectors = []
for assignment_file in assignment_files:
    TFIDF_weightvectors.append(computeTFIDF(assignment_file, unique_words_no_stopwords, DFs, len(assignment_files)))

if getLogs:
    print ('TFIDF weight vectors',TFIDF_weightvectors,'\n')

def getFileIndex(filename):
    for i in range(len(assignment_files)):
        if assignment_files[i] == filename:
            return i
    return -1
    
def printPlagiarismRatio(filename):
    idx = getFileIndex(filename)
    if idx==-1:
        print ("FILE NOT FOUND")
    else:
        for i in range(len(assignment_files)):
            if i != idx:
                    cosineSim = compareDocument(TFIDF_weightvectors[i], TFIDF_weightvectors[idx])
                    print ("Cosine similarity between given doc and", assignment_files[i], " = ", cosineSim*100 , "%")

printPlagiarismRatio("Dataset/No Plagiarism/Source.docx")
