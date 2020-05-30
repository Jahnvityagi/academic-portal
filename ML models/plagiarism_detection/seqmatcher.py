from nltk import tokenize

def tokenizee(filename):
    text = filename
    tzr = tokenize.RegexpTokenizer(r'\w+')
    tokens = tzr.tokenize(text)
    result = []
    lenT = len(tokens)
    count = 0
    for i in range(lenT):
        result.append((tokens[i], count, count))
        count += len(tokens[i])
    return result

def toText(arr):
    cleanText = ''.join(str(x[0]) for x in arr)
    return cleanText

from difflib import SequenceMatcher    
import docx
def getText(filename):
    doc = docx.Document(filename)
    fullText = []
    for para in doc.paragraphs:
        fullText.append(para.text)
    return '\n'.join(fullText)
    
f1 = input("Enter file1:")
f2 = input("Enter file2:")

fn1 = getText(f1)
fn2 = getText(f2)
tokens1 = tokenizee(filename1)
file1 = toText(tokens1)
tokens2 = tokenizee(filename2)
file2 = toText(tokens2)
SM = SequenceMatcher(None, file1, file2)
plag_ratio = SM.ratio() * 100

print("\nPlagiarism ratio: ", plag_ratio, "%.")
