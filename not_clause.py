import nltk
import identify_all


def get_chunk(chunked):
    string_1 = ""
    for i in range(len(chunked)):
        string_1 += (chunked[i][0] + " ")
    return string_1

def what_whom1(segment_set, num, ner):
    tok = nltk.word_tokenize(segment_set[num])
    tag = nltk.pos_tag(tok)
    gram = r"""chunk:{<TO>+<DT>?<RB.?>*<JJ.?>*<NN.?|PRP|PRP\$|VBG|DT|POS|CD|VBN>+}"""
    chunkparser = nltk.RegexpParser(gram)
    chunked = chunkparser.parse(tag)

    first_list = identify_all.chunk_search(segment_set[num], chunked)
    s = []

    if len(first_list) != 0:
        for i in range(len(chunked)):
            string_1 = ""
            string_3 = ""
            if i in first_list:
                for temp in range(i):
                    if temp in first_list:
                        string_1 += get_chunk(chunked[temp])
                    else:
                        string_1 += (chunked[temp][0] + " ")
                for temp in range(i + 1, len(chunked)):
                    if temp in first_list:
                        string_3 += get_chunk(chunked[temp])
                    else:
                        string_3 += (chunked[temp][0] + " ")

                if chunked[i][1][1] == 'PRP':
                    string_2 = "to whom "
                else:
                    for x in range(len(chunked[i])):
                        if (chunked[i][x][1] == "NNP" or chunked[i][x][1] == "NNPS" or chunked[i][x][1] == "NNS" or
                                chunked[i][x][1] == "NN"):
                            break

                    for x1 in range(len(ner)):
                        if ner[x1][0] == chunked[i][x][0]:
                            if ner[x1][1] == "PERSON":
                                string_2 = " to whom "
                            elif ner[x1][1] == "LOC" or ner[x1][1] == "ORG" or ner[x1][1] == "GPE":
                                string_2 = " where "
                            elif ner[x1][1] == "TIME" or ner[x1][1] == "DATE":
                                string_2 = " when "
                            else:
                                string_2 = "to what"

                string_4 = string_1 + string_2 + string_3
                for temp in range(len(segment_set)):
                    if temp != num:
                        string_4 += ("," + segment_set[temp])
                string_4 += '?'
                string_4 = identify_all.postprocess(string_4)
                # string_4 = 'Q.' + string_4
                s.append(string_4)
    return s


def what_whom2(segment_set, num, ner):
    tok = nltk.word_tokenize(segment_set[num])
    tag = nltk.pos_tag(tok)
    gram = r"""chunk:{<IN>+<DT>?<RB.?>*<JJ.?>*<NN.?|PRP|PRP\$|POS|VBG|DT|CD|VBN>+}"""
    chunkparser = nltk.RegexpParser(gram)
    chunked = chunkparser.parse(tag)
    first_list = identify_all.chunk_search(segment_set[num], chunked)
    s = []

    if len(first_list) != 0:
        for i in range(len(chunked)):
            string_1 = ""
            string_3 = ""
            if i in first_list:
                for temp in range(i):
                    if temp in first_list:
                        string_1 += get_chunk(chunked[temp])
                    else:
                        string_1 += (chunked[temp][0] + " ")
                for temp in range(i + 1, len(chunked)):
                    if temp in first_list:
                        string_3 += get_chunk(chunked[temp])
                    else:
                        string_3 += (chunked[temp][0] + " ")

                if chunked[i][1][1] == 'PRP':
                    string_2 = " " + chunked[i][0][0] + " whom "
                else:
                    for x in range(len(chunked[i])):
                        if (chunked[i][x][1] == "NNP" or chunked[i][x][1] == "NNPS" or chunked[i][x][1] == "NNS" or
                                chunked[i][x][1] == "NN"):
                            break

                    for x1 in range(len(ner)):
                        if ner[x1][0] == chunked[i][x][0]:
                            if ner[x1][1] == "PERSON":
                                string_2 = " " + chunked[i][0][0] + "whom "
                            elif ner[x1][1] == "LOC" or ner[x1][1] == "ORG" or ner[x1][1] == "GPE":
                                string_2 = " where "
                            elif ner[x1][1] == "TIME" or ner[x1][1] == "DATE":
                                string_2 = " when "
                            else:
                                string_2 = " " + chunked[i][0][0] + " what"

                string_4 = string_1 + string_2 + string_3
                for temp in range(len(segment_set)):
                    if temp != num:
                        string_4 += ("," + segment_set[temp])
                string_4 += '?'
                string_4 = identify_all.postprocess(string_4)
                # string_4 = 'Q.' + string_4
                s.append(string_4)
    return s


def whose(segment_set, num, ner):
    tok = nltk.word_tokenize(segment_set[num])
    tag = nltk.pos_tag(tok)
    gram = r"""chunk:{<NN.?>*<PRP\$|POS>+<RB.?>*<JJ.?>*<NN.?|VBG|VBN>+}"""
    chunkparser = nltk.RegexpParser(gram)
    chunked = chunkparser.parse(tag)

    first_list = identify_all.chunk_search(segment_set[num], chunked)
    s = []

    if len(first_list) != 0:
        for i in range(len(chunked)):
            string_1 = ""
            string_3 = ""
            string_2 = " whose "
            if i in first_list:
                for temp in range(i):
                    if temp in first_list:
                        string_1 += get_chunk(chunked[temp])
                    else:
                        string_1 += (chunked[temp][0] + " ")
                for temp in range(i + 1, len(chunked)):
                    if temp in first_list:
                        string_3 += get_chunk(chunked[temp])
                    else:
                        string_3 += (chunked[temp][0] + " ")
                if chunked[i][1][1] == 'POS':
                    for temp in range(2, len(chunked[i])):
                        string_2 += (chunked[i][temp][0] + " ")
                else:
                    for temp in range(1, len(chunked[i])):
                        string_2 += (chunked[i][temp][0] + " ")

                string_4 = string_1 + string_2 + string_3
                for temp in range(len(segment_set)):
                    if temp != num:
                        string_4 += ("," + segment_set[temp])
                string_4 += '?'
                string_4 = identify_all.postprocess(string_4)
                # string_4 = 'Q.' + string_4
                s.append(string_4)
    return s


def howmany(segment_set, num, ner):
    tok = nltk.word_tokenize(segment_set[num])
    tag = nltk.pos_tag(tok)
    gram = r"""chunk:{<DT>?<CD>+<RB>?<JJ|JJR|JJS>?<NN|NNS|NNP|NNPS|VBG>+}"""
    chunkparser = nltk.RegexpParser(gram)
    chunked = chunkparser.parse(tag)

    first_list = identify_all.chunk_search(segment_set[num], chunked)
    s = []

    if len(first_list) != 0:
        for i in range(len(chunked)):
            string_1 = ""
            string_3 = ""
            string_2 = " how many "
            if i in first_list:
                for temp in range(i):
                    if temp in first_list:
                        string_1 += get_chunk(chunked[temp])
                    else:
                        string_1 += (chunked[temp][0] + " ")
                for temp in range(i + 1, len(chunked)):
                    if temp in first_list:
                        string_3 += get_chunk(chunked[temp])
                    else:
                        string_3 += (chunked[temp][0] + " ")

                st = get_chunk(chunked[i])
                tok = nltk.word_tokenize(st)
                tag = nltk.pos_tag(tok)
                gram = r"""chunk:{<RB>?<JJ|JJR|JJS>?<NN|NNS|NNP|NNPS|VBG>+}"""
                chunkparser = nltk.RegexpParser(gram)
                chunked1 = chunkparser.parse(tag)

                sec_list = identify_all.chunk_search(st, chunked1)
                z = ""

                for temp in range(len(chunked1)):
                    if temp in sec_list:
                        z += get_chunk(chunked1[temp])

                string_4 = string_1 + string_2 + z + string_3
                for temp in range(len(segment_set)):
                    if temp != num:
                        string_4 += ("," + segment_set[temp])
                string_4 += '?'
                string_4 = identify_all.postprocess(string_4)
                # string_4 = 'Q.' + string_4
                s.append(string_4)
    return s


def howmuch_1(segment_set, num, ner):
    tok = nltk.word_tokenize(segment_set[num])
    tag = nltk.pos_tag(tok)
    gram = r"""chunk:{<IN>+<\$>?<CD>+}"""
    chunkparser = nltk.RegexpParser(gram)
    chunked = chunkparser.parse(tag)

    first_list = identify_all.chunk_search(segment_set[num], chunked)
    s = []

    if len(first_list) != 0:
        for i in range(len(chunked)):
            string_1 = ""
            string_3 = ""
            string_2 = " how much "
            if i in first_list:
                for temp in range(i):
                    if temp in first_list:
                        string_1 += get_chunk(chunked[temp])
                    else:
                        string_1 += (chunked[temp][0] + " ")
                for temp in range(i + 1, len(chunked)):
                    if temp in first_list:
                        string_3 += get_chunk(chunked[temp])
                    else:
                        string_3 += (chunked[temp][0] + " ")

                string_2 = chunked[i][0][0] + string_2
                string_4 = string_1 + string_2 + string_3
                for temp in range(len(segment_set)):
                    if temp != num:
                        string_4 += ("," + segment_set[temp])
                string_4 += '?'
                string_4 = identify_all.postprocess(string_4)
                # string_4 = 'Q.' + string_4
                s.append(string_4)
    return s
