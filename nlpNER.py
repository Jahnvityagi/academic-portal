import spacy

def tagger_func(nlp, tokenize):
    doc = nlp(tokenize)

    end_list = []
    array = [[]]
    for word in doc:
        array[0] = 0
        for ner in doc.ents:
            if (ner.text == word.text):
                end_list.append((word.text, ner.label_))
                array[0] = 1
        if (array[0] == 0):
            end_list.append((word.text, 'O'))

    return end_list

def hn_validate(sentence):
    flag = 1

    len_sent = len(sentence)
    if (len_sent > 4):
        for i in range(len_sent):
            if (i+4 < len_sent):
                if (sentence[i]==' ' and sentence[i+1]=='h' and sentence[i+2]==' ' and sentence[i+3]=='N' and sentence[i+4]==' '):
                    flag = 0


    return flag
