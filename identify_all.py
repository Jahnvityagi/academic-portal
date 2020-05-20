import nltk


def search_the_chunk(segment, chunked):
    m = len(chunked)
    first_list = []
    for temp_2 in range(m):
        if (len(chunked[temp_2]) > 2 or len(chunked[temp_2]) == 1):
            first_list.append(temp_2)
        if (len(chunked[temp_2]) == 2):
            try:
                string_1 = chunked[temp_2][0][0] + " " + chunked[temp_2][1][0]
            except Exception:
                pass
            else:
                if (string_1 in segment) == True:
                    first_list.append(temp_2)

    return first_list

def segment_identify(sen):
    segment_set = sen.split(",")
    return segment_set


def identify_the_clause(segment):
    tok = nltk.word_tokenize(segment)
    tag = nltk.pos_tag(tok)
    gram = r"""chunk:{<EX>?<DT>?<JJ.?>*<NN.?|PRP|PRP\$|POS|IN|DT|CC|VBG|VBN>+<RB.?|VB.?|MD|RP>+}"""
    chunkparser = nltk.RegexpParser(gram)
    chunked = chunkparser.parse(tag)

    flag = 0
    for temp_2 in range(len(chunked)):
        if (len(chunked[temp_2]) > 2):
            flag = 1
        if (len(chunked[temp_2]) == 2):
            try:
                string_1 = chunked[temp_2][0][0] + " " + chunked[temp_2][1][0]
            except Exception:
                pass
            else:
                if (string_1 in segment) == True:
                    flag = 1
        if flag == 1:
            break

    return flag


def verbphrase_identify(clause):
    tok = nltk.word_tokenize(clause)
    tag = nltk.pos_tag(tok)
    gram = r"""chunk:{<EX>?<DT>?<JJ.?>*<NN.?|PRP|PRP\$|POS|IN|DT|CC|VBG|VBN>+<RB.?>*<VB.?|MD|RP>+}"""
    chunkparser = nltk.RegexpParser(gram)
    chunked = chunkparser.parse(tag)
    string_1 = ""
    string_2 = ""
    string_3 = ""
    first_list = search_the_chunk(clause, chunked)
    if len(first_list) != 0:
        m = first_list[len(first_list) - 1]
        for temp_2 in range(len(chunked[m])):
            string_1 += chunked[m][temp_2][0]
            string_1 += " "

    tok1 = nltk.word_tokenize(string_1)
    tag1 = nltk.pos_tag(tok1)
    gram1 = r"""chunk:{<EX>?<DT>?<JJ.?>*<NN.?|PRP|PRP\$|POS|IN|DT|CC|VBG|VBN>+<RB.?>*}"""
    chunkparser1 = nltk.RegexpParser(gram1)
    chunked1 = chunkparser1.parse(tag1)

    sec_list = search_the_chunk(string_1, chunked1)
    if len(sec_list) != 0:

        m = sec_list[0]
        for temp_2 in range(len(chunked1[m])):
            string_2 += (chunked1[m][temp_2][0] + " ")

    tok1 = nltk.word_tokenize(string_1)
    tag1 = nltk.pos_tag(tok1)
    gram1 = r"""chunk:{<VB.?|MD|RP>+}"""
    chunkparser1 = nltk.RegexpParser(gram1)
    chunked2 = chunkparser1.parse(tag1)

    third_list = search_the_chunk(string_1, chunked2)
    if len(third_list) != 0:

        m = third_list[0]
        for temp_2 in range(len(chunked2[m])):
            string_3 += (chunked2[m][temp_2][0] + " ")

    X = ""
    string_4 = ""
    str = nltk.word_tokenize(string_3)
    if len(str) > 1:
        X = str[0]
        s = ""
        for temp_3 in range(1, len(str)):
            s += str[temp_3]
            s += " "
        string_3 = s
        string_4 = X + " " + string_2 + string_3

    if len(str) == 1:
        tag1 = nltk.pos_tag(str)
        if tag1[0][0] != 'are' and tag1[0][0] != 'were' and tag1[0][0] != 'is' and tag1[0][0] != 'am':
            if tag1[0][1] == 'VB' or tag1[0][1] == 'VBP':
                X = 'do'
            if tag1[0][1] == 'VBD' or tag1[0][1] == 'VBN':
                X = 'did'
            if tag1[0][1] == 'VBZ':
                X = 'does'
            string_4 = X + " " + string_2 + string_3
        if (tag1[0][0] == 'are' or tag1[0][0] == 'were' or tag1[0][0] == 'is' or tag1[0][0] == 'am'):
            string_4 = tag1[0][0] + " " + string_2

    return string_4


def subjectphrase_search(segment_set, num):
    string_2 = ""
    for temp_2 in range(num - 1, 0, -1):
        string_1 = ""
        flag = 0
        tok = nltk.word_tokenize(segment_set[temp_2])
        tag = nltk.pos_tag(tok)
        gram = r"""chunk:{<EX>?<DT>?<JJ.?>*<NN.?|PRP|PRP\$|POS|IN|DT|CC|VBG|VBN>+<RB.?>*<VB.?|MD|RP>+}"""
        chunkparser = nltk.RegexpParser(gram)
        chunked = chunkparser.parse(tag)


        first_list = search_the_chunk(segment_set[temp_2], chunked)

        if len(first_list) != 0:
            m = first_list[len(first_list) - 1]
            for temp_2 in range(len(chunked[m])):
                string_1 += chunked[m][temp_2][0]
                string_1 += " "


            tok1 = nltk.word_tokenize(string_1)
            tag1 = nltk.pos_tag(tok1)
            gram1 = r"""chunk:{<EX>?<DT>?<JJ.?>*<NN.?|PRP|PRP\$|POS|IN|DT|CC|VBG|VBN>+}"""
            chunkparser1 = nltk.RegexpParser(gram1)
            chunked1 = chunkparser1.parse(tag1)

            sec_list = search_the_chunk(string_1, chunked1)
            if len(sec_list) != 0:
                m = sec_list[len(sec_list) - 1]
                for temp_2 in range(len(chunked1[m])):
                    string_2 += (chunked1[m][temp_2][0] + " ")
                flag = 1

        if flag == 0:
            tok1 = nltk.word_tokenize(segment_set[temp_2])
            tag1 = nltk.pos_tag(tok1)
            gram1 = r"""chunk:{<EX>?<DT>?<JJ.?>*<NN.?|PRP|PRP\$|POS|IN|DT|CC|VBG|VBN>+}"""
            chunkparser1 = nltk.RegexpParser(gram1)
            chunked1 = chunkparser1.parse(tag1)

            sec_list = search_the_chunk(string_1, chunked1)
            str = nltk.word_tokenize(segment_set[temp_2])
            if len(chunked1[sec_list[0]]) == len(str):
                string_2 = segment_set[temp_2]
                flag = 1

        if flag == 1:
            break

    return string_2


def postprocess(string):
    tok = nltk.word_tokenize(string)
    tag = nltk.pos_tag(tok)

    string_1 = tok[0].capitalize()
    string_1 += " "
    if len(tok) != 0:
        for temp in range(1, len(tok)):
            if tag[temp][1] == "NNP":
                string_1 += tok[temp].capitalize()
                string_1 += " "
            else:
                string_1 += tok[temp].lower()
                string_1 += " "
        tok = nltk.word_tokenize(string_1)
        string_1 = ""
        for temp in range(len(tok)):
            if tok[temp] == "temp" or tok[temp] == "we":
                string_1 += "you"
                string_1 += " "
            elif tok[temp] == "my" or tok[temp] == "our":
                string_1 += "your"
                string_1 += " "
            elif tok[temp] == "your":
                string_1 += "my"
                string_1 += " "
            elif tok[temp] == "you":
                if temp - 1 >= 0:
                    to = nltk.word_tokenize(tok[temp - 1])
                    ta = nltk.pos_tag(to)
                    # print ta
                    if ta[0][1] == 'IN':
                        string_1 += "me"
                        string_1 += " "
                    else:
                        string_1 += "temp"
                        string_1 += " "
                else:
                    string_1 += "temp "

            elif tok[temp] == "am":
                string_1 += "are"
                string_1 += " "
            else:
                string_1 += tok[temp]
                string_1 += " "

    return string_1
