import pandas as pd
from nltk import tokenize
from spellchecker import SpellChecker
from nltk.corpus import wordnet as wn
import textstat
import http.client
import urllib.request, urllib.parse, urllib.error
from xml.etree import ElementTree
import csv
import nltk
stopwords = nltk.corpus.stopwords.words('english')

data = pd.read_csv('dataset.csv')
features = []
_key = None

#grammar checker API code from: https://github.com/Shahabks/mystracher/blob/master/mystracher.py
def setDefaultKey(key):
    global _key
    _key = key

def checkDocument(text, key=None):
    global _key
    if key is None:
        if _key is None:
            raise Exception('Please provide key as argument or set it using setDefaultKey() first')
        key = _key

    params = urllib.parse.urlencode({
        'key': key,
        'data': text,
    })
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': '*/*',
        'User-Agent':' python-ATD',
    }
    service = http.client.HTTPConnection("service.afterthedeadline.com")
    service.request("POST", "/checkDocument", body=params, headers=headers)
    response = service.getresponse()
    if response.status != http.client.OK:
        service.close()
        raise Exception('Unexpected response code from AtD service %d' % response.status)
    response_text = response.read()
    e = ElementTree.fromstring(response_text)
    service.close()
    errs = e.findall('message')
    if len(errs) > 0:
        raise Exception('Server returned an error: %s' % errs[0].text)
    return [Error(err) for err in e.findall('error')]

class Error:
    """ AtD Error Object
    These are to be returned in a list by checkText()
    Available properties are: string, description, precontext, type, url
    and suggestions. """
    def __init__(self, e):
        self.string = e.find('string').text
        self.description = e.find('description').text
        self.precontext = e.find('precontext').text
        self.type = e.find('type').text
        if not e.find('url') is None:
            self.url = e.find('url').text
        else:
            self.url = ""
        if not e.find('suggestions') is None:
            self.suggestions = [o.text for o in e.find('suggestions').findall('option')]
        else:
            self.suggestions = []
    def __str__(self):
        return "%s (%s)" % (self.string, self.description)

def getGrammarMistakes(essay):
    cnt = 0
    setDefaultKey('mygra2019#shs')
    errs=checkDocument(essay)
    for error in errs:
        if error.type=="grammar":
            cnt+=1
    return cnt

def getSpellingMistakes(words):
    spell = SpellChecker()
    return len(spell.unknown(words))

storage = {}
def getTopicCoherenceScore(essay_words, topic_words):
    score = 0
    for topic_word in topic_words:
        for essay_word in essay_words:
            myScore = 0
            if (topic_word,essay_word) not in storage:
                maximum_similarity = -1
                t_synset = wn.synsets(topic_word)
                s_synset = wn.synsets(essay_word)
                if (len (t_synset) != 0 and len (s_synset) != 0):
                    for synset_one in t_synset:
                        for synset_two in s_synset:
                            similarity = wn.path_similarity (synset_one,synset_two)
                            if similarity != None and similarity > maximum_similarity:
                                maximum_similarity = similarity
                                myScore += similarity
                score += myScore
                storage[(topic_word,essay_word)] = myScore
            else:
                score += storage[(topic_word,essay_word)]
    return score

def getAvgSentenceLength(sents):
    avg = 0
    tzr = tokenize.RegexpTokenizer(r'\w+')
    for s in sents:
        avg += len(tzr.tokenize(s))
    avg /= len(sents)
    return avg


for i in range(0,data.shape[0]):
    essay = data['essay'][i]
    topic = data['topic'][i]
    sents = tokenize.sent_tokenize(essay)
    tzr = tokenize.RegexpTokenizer(r'\w+')
    essay_words = tzr.tokenize(essay)
    topic_words = tzr.tokenize(topic)
    essay_words_uniq = []
    topic_words_uniq = []
    for word in essay_words:
        if word not in stopwords:
            essay_words_uniq.append(word)
    for word in topic_words:
           if word not in stopwords:
               topic_words_uniq.append(word)

    dataset_row = []
    print ("calculating lengths...")
    dataset_row.append(len(sents))
    dataset_row.append(len(essay_words_uniq))
    print("calculating spell errors...")
    dataset_row.append(getSpellingMistakes(essay_words))
    print("calculating grammar errors...")
    dataset_row.append(getGrammarMistakes(essay))
    print("calculating coherence...")
    dataset_row.append(getTopicCoherenceScore(essay_words_uniq, topic_words_uniq))
    dataset_row.append(getAvgSentenceLength(sents))
    dataset_row.append(len(set(essay_words_uniq)))
    print("calculating indices")
    dataset_row.append(textstat.flesch_reading_ease(essay))
    dataset_row.append(textstat.coleman_liau_index(essay))
    print(i, dataset_row)
    with open('features_data_final.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow(dataset_row)
