import nltk
import identify_all
import not_clause


def whom_1(segment_set, num, ner):
    tok = nltk.word_tokenize(segment_set[num])
    tag = nltk.pos_tag(tok)
    gram = r"""chunk:{<TO>+<DT>?<RB.?>*<JJ.?>*<NN.?|PRP|PRP\$|VBG|DT|POS|CD|VBN>+}"""
    chunk_parse = nltk.RegexpParser(gram)
    chunk_ans = chunk_parse.parse(tag)

    first_list = identify_all.search_the_chunk(segment_set[num], chunk_ans)
    third_list = []

    if len(first_list) != 0:
        for temp_2 in range(len(chunk_ans)):
            str1 = ""
            str2 = ""
            str3 = ""
            if temp_2 in first_list:
                for temp_3 in range(temp_2):
                    if temp_3 in first_list:
                        str1 += not_clause.get_chunk(chunk_ans[temp_3])
                    else:
                        str1 += (chunk_ans[temp_3][0] + " ")

                for temp_3 in range(temp_2 + 1, len(chunk_ans)):
                    if temp_3 in first_list:
                        str3 += not_clause.get_chunk(chunk_ans[temp_3])
                    else:
                        str3 += (chunk_ans[temp_3][0] + " ")

                if chunk_ans[temp_2][1][1] == 'PRP':
                    str2 = " to whom "
                else:
                    for x in range(len(chunk_ans[temp_2])):
                        if (chunk_ans[temp_2][x][1] == "NNP" or chunk_ans[temp_2][x][1] == "NNPS" or chunk_ans[temp_2][x][1] == "NNS" or
                                chunk_ans[temp_2][x][1] == "NN"):
                            break

                    for x1 in range(len(ner)):

                        if ner[x1][0] == chunk_ans[temp_2][x][0]:
                            if ner[x1][1] == "PERSON":
                                str2 = " to whom "
                            elif ner[x1][1] == "LOC" or ner[x1][1] == "ORG" or ner[x1][1] == "GPE":
                                str2 = " where "
                            elif ner[x1][1] == "TIME" or ner[x1][1] == "DATE":
                                str2 = " when "
                            else:
                                str2 = "to what "

                tok = nltk.word_tokenize(str1)
                tag = nltk.pos_tag(tok)
                gram = r"""chunk:{<EX>?<DT>?<JJ.?>*<NN.?|PRP|PRP\$|POS|IN|DT|CC|VBG|VBN>+<RB.?>*<VB.?|MD|RP>+}"""
                chunk_parse = nltk.RegexpParser(gram)
                chunked1 = chunk_parse.parse(tag)

                sec_list = identify_all.search_the_chunk(str1, chunked1)
                if len(sec_list) != 0:
                    m = sec_list[len(sec_list) - 1]

                    str4 = not_clause.get_chunk(chunked1[m])
                    str4 = identify_all.verbphrase_identify(str4)
                    str5 = ""
                    str6 = ""

                    for temp_3 in range(m):
                        if temp_3 in sec_list:
                            str5 += not_clause.get_chunk(chunked1[temp_3])
                        else:
                            str5 += (chunked1[temp_3][0] + " ")

                    for temp_3 in range(m + 1, len(chunked1)):
                        if temp_3 in sec_list:
                            str6 += not_clause.get_chunk(chunked1[temp_3])
                        else:
                            str6 += (chunked1[temp_3][0] + " ")

                    st = str5 + str2 + str4 + str6 + str3
                    for l in range(num + 1, len(segment_set)):
                        st += ("," + segment_set[l])
                    st += '?'
                    st = identify_all.postprocess(st)
                    # st = 'Q.' + st
                    third_list.append(st)

    return third_list


def whom_2(segment_set, num, ner):
    tok = nltk.word_tokenize(segment_set[num])
    tag = nltk.pos_tag(tok)
    gram = r"""chunk:{<IN>+<DT>?<RB.?>*<JJ.?>*<NN.?|PRP|PRP\$|POS|VBG|DT|CD|VBN>+}"""
    chunk_parse = nltk.RegexpParser(gram)
    chunk_ans = chunk_parse.parse(tag)

    first_list = identify_all.search_the_chunk(segment_set[num], chunk_ans)
    third_list = []

    if len(first_list) != 0:
        for temp_2 in range(len(chunk_ans)):
            str1 = ""
            str2 = ""
            str3 = ""
            if temp_2 in first_list:
                for temp_3 in range(temp_2):
                    if temp_3 in first_list:
                        str1 += not_clause.get_chunk(chunk_ans[temp_3])
                    else:
                        str1 += (chunk_ans[temp_3][0] + " ")

                for temp_3 in range(temp_2 + 1, len(chunk_ans)):
                    if temp_3 in first_list:
                        str3 += not_clause.get_chunk(chunk_ans[temp_3])
                    else:
                        str3 += (chunk_ans[temp_3][0] + " ")

                if chunk_ans[temp_2][1][1] == 'PRP':
                    str2 = " " + chunk_ans[temp_2][0][0] + " whom "
                else:
                    for x in range(len(chunk_ans[temp_2])):
                        if (chunk_ans[temp_2][x][1] == "NNP" or chunk_ans[temp_2][x][1] == "NNPS" or chunk_ans[temp_2][x][1] == "NNS" or
                                chunk_ans[temp_2][x][1] == "NN"):
                            break

                    for x1 in range(len(ner)):
                        if ner[x1][0] == chunk_ans[temp_2][x][0]:
                            if ner[x1][1] == "PERSON":
                                str2 = " " + chunk_ans[temp_2][0][0] + " whom "
                            elif ner[x1][1] == "LOC" or ner[x1][1] == "ORG" or ner[x1][1] == "GPE":
                                str2 = " where "
                            elif ner[x1][1] == "TIME" or ner[x1][1] == "DATE":
                                str2 = " when "
                            else:
                                str2 = " " + chunk_ans[temp_2][0][0] + " what "

                tok = nltk.word_tokenize(str1)
                tag = nltk.pos_tag(tok)
                gram = r"""chunk:{<EX>?<DT>?<JJ.?>*<NN.?|PRP|PRP\$|POS|IN|DT|CC|VBG|VBN>+<RB.?>*<VB.?|MD|RP>+}"""
                chunk_parse = nltk.RegexpParser(gram)
                chunked1 = chunk_parse.parse(tag)

                sec_list = identify_all.search_the_chunk(str1, chunked1)
                if len(sec_list) != 0:
                    m = sec_list[len(sec_list) - 1]

                    str4 = not_clause.get_chunk(chunked1[m])
                    str4 = identify_all.verbphrase_identify(str4)
                    str5 = ""
                    str6 = ""

                    for temp_3 in range(m):
                        if temp_3 in sec_list:
                            str5 += not_clause.get_chunk(chunked1[temp_3])
                        else:
                            str5 += (chunked1[temp_3][0] + " ")

                    for temp_3 in range(m + 1, len(chunked1)):
                        if temp_3 in sec_list:
                            str6 += not_clause.get_chunk(chunked1[temp_3])
                        else:
                            str6 += (chunked1[temp_3][0] + " ")

                    st = str5 + str2 + str4 + str6 + str3
                    for l in range(num + 1, len(segment_set)):
                        st += ("," + segment_set[l])
                    st += '?'
                    st = identify_all.postprocess(st)
                    # st = 'Q.' + st
                    third_list.append(st)

    return third_list


def whom_3(segment_set, num, ner):
    tok = nltk.word_tokenize(segment_set[num])
    tag = nltk.pos_tag(tok)
    gram = r"""chunk:{<VB.?|MD|RP>+<DT>?<RB.?>*<JJ.?>*<NN.?|PRP|PRP\$|POS|VBG|DT|CD|VBN>+}"""
    chunk_parse = nltk.RegexpParser(gram)
    chunk_ans = chunk_parse.parse(tag)

    first_list = identify_all.search_the_chunk(segment_set[num], chunk_ans)
    third_list = []

    if len(first_list) != 0:
        for temp_2 in range(len(chunk_ans)):
            str1 = ""
            str2 = ""
            str3 = ""
            if temp_2 in first_list:
                for temp_3 in range(temp_2):
                    if temp_3 in first_list:
                        str1 += not_clause.get_chunk(chunk_ans[temp_3])
                    else:
                        str1 += (chunk_ans[temp_3][0] + " ")

                for temp_3 in range(temp_2 + 1, len(chunk_ans)):
                    if temp_3 in first_list:
                        str3 += not_clause.get_chunk(chunk_ans[temp_3])
                    else:
                        str3 += (chunk_ans[temp_3][0] + " ")

                if chunk_ans[temp_2][1][1] == 'PRP':
                    str2 = " whom "
                else:
                    for x in range(len(chunk_ans[temp_2])):
                        if (chunk_ans[temp_2][x][1] == "NNP" or chunk_ans[temp_2][x][1] == "NNPS" or chunk_ans[temp_2][x][1] == "NNS" or
                                chunk_ans[temp_2][x][1] == "NN"):
                            break

                    for x1 in range(len(ner)):
                        if ner[x1][0] == chunk_ans[temp_2][x][0]:
                            if ner[x1][1] == "PERSON":
                                str2 = " whom "
                            elif ner[x1][1] == "LOC" or ner[x1][1] == "ORG" or ner[x1][1] == "GPE":
                                str2 = " what "
                            elif ner[x1][1] == "TIME" or ner[x1][1] == "DATE":
                                str2 = " what time "
                            else:
                                str2 = " what "

                strx = not_clause.get_chunk(chunk_ans[temp_2])
                tok = nltk.word_tokenize(strx)
                tag = nltk.pos_tag(tok)
                gram = r"""chunk:{<VB.?|MD>+}"""
                chunk_parse = nltk.RegexpParser(gram)
                chunked1 = chunk_parse.parse(tag)

                strx = not_clause.get_chunk(chunked1[0])

                str1 += strx

                tok = nltk.word_tokenize(str1)
                tag = nltk.pos_tag(tok)
                gram = r"""chunk:{<EX>?<DT>?<JJ.?>*<NN.?|PRP|PRP\$|POS|IN|DT|CC|VBG|VBN>+<RB.?>*<VB.?|MD|RP>+}"""
                chunk_parse = nltk.RegexpParser(gram)
                chunked1 = chunk_parse.parse(tag)

                sec_list = identify_all.search_the_chunk(str1, chunked1)

                if len(sec_list) != 0:
                    m = sec_list[len(sec_list) - 1]

                    str4 = not_clause.get_chunk(chunked1[m])
                    str4 = identify_all.verbphrase_identify(str4)
                    str5 = ""
                    str6 = ""

                    for temp_3 in range(m):
                        if temp_3 in sec_list:
                            str5 += not_clause.get_chunk(chunked1[temp_3])
                        else:
                            str5 += (chunked1[temp_3][0] + " ")

                    for temp_3 in range(m + 1, len(chunked1)):
                        if temp_3 in sec_list:
                            str6 += not_clause.get_chunk(chunked1[temp_3])
                        else:
                            str6 += (chunked1[temp_3][0] + " ")

                    st = str5 + str2 + str4 + str6 + str3
                    for l in range(num + 1, len(segment_set)):
                        st += ("," + segment_set[l])
                    st += '?'
                    st = identify_all.postprocess(st)
                    # st = 'Q.' + st
                    third_list.append(st)

    return third_list


def whose(segment_set, num, ner):
    tok = nltk.word_tokenize(segment_set[num])
    tag = nltk.pos_tag(tok)
    gram = r"""chunk:{<DT|NN.?>*<PRP\$|POS>+<RB.?>*<JJ.?>*<NN.?|VBG|VBN>+<RB.?>*<VB.?|MD|RP>+}"""
    chunk_parse = nltk.RegexpParser(gram)
    chunk_ans = chunk_parse.parse(tag)

    first_list = identify_all.search_the_chunk(segment_set[num], chunk_ans)
    third_list = []

    if len(first_list) != 0:
        for temp in range(len(chunk_ans)):
            if temp in first_list:
                str1 = ""
                str3 = ""
                str2 = ""
                for temp_3 in range(temp):
                    if temp_3 in first_list:
                        str1 += not_clause.get_chunk(chunk_ans[temp_3])
                    else:
                        str1 += (chunk_ans[temp_3][0] + " ")
                str1 += " whose "

                for temp_3 in range(temp + 1, len(chunk_ans)):
                    if temp_3 in first_list:
                        str3 += not_clause.get_chunk(chunk_ans[temp_3])
                    else:
                        str3 += (chunk_ans[temp_3][0] + " ")

                if chunk_ans[temp][1][1] == 'POS':
                    for temp_3 in range(2, len(chunk_ans[temp])):
                        str2 += (chunk_ans[temp][temp_3][0] + " ")

                if chunk_ans[temp][0][1] == 'PRP$':
                    for temp_3 in range(1, len(chunk_ans[temp])):
                        str2 += (chunk_ans[temp][temp_3][0] + " ")

                str2 = str1 + str2 + str3
                str4 = ""

                for l in range(0, len(segment_set)):
                    if l < num:
                        str4 += (segment_set[l] + ",")
                    if l > num:
                        str2 += ("," + segment_set[l])
                str2 = str4 + str2
                str2 += '?'
                str2 = identify_all.postprocess(str2)
                # str2 = 'Q.' + str2
                third_list.append(str2)

    return third_list


def what_to_do(segment_set, num, ner):
    tok = nltk.word_tokenize(segment_set[num])
    tag = nltk.pos_tag(tok)
    gram = r"""chunk:{<TO>+<VB|VBP|RP>+<DT>?<RB.?>*<JJ.?>*<NN.?|PRP|PRP\$|POS|VBG|DT>*}"""
    chunk_parse = nltk.RegexpParser(gram)
    chunk_ans = chunk_parse.parse(tag)

    first_list = identify_all.search_the_chunk(segment_set[num], chunk_ans)
    third_list = []

    if len(first_list) != 0:
        for temp_2 in range(len(chunk_ans)):
            str1 = ""
            str2 = ""
            str3 = ""
            if temp_2 in first_list:
                for temp_3 in range(temp_2):
                    if temp_3 in first_list:
                        str1 += not_clause.get_chunk(chunk_ans[temp_3])
                    else:
                        str1 += (chunk_ans[temp_3][0] + " ")

                for temp_3 in range(temp_2 + 1, len(chunk_ans)):
                    if temp_3 in first_list:
                        str3 += not_clause.get_chunk(chunk_ans[temp_3])
                    else:
                        str3 += (chunk_ans[temp_3][0] + " ")

                ls = not_clause.get_chunk(chunk_ans[temp_2])
                tok = nltk.word_tokenize(ls)
                tag = nltk.pos_tag(tok)
                gram = r"""chunk:{<DT>?<RB.?>*<JJ.?>*<NN.?|PRP|PRP\$|POS|VBG|DT>+}"""
                chunk_parse = nltk.RegexpParser(gram)
                chunked2 = chunk_parse.parse(tag)
                lis = identify_all.search_the_chunk(ls, chunked2)
                if len(lis) != 0:
                    x = lis[len(lis) - 1]
                    ls1 = not_clause.get_chunk(chunked2[x])
                    index = ls.find(ls1)
                    str2 = " " + ls[0:index]
                else:
                    str2 = " to do "

                tok = nltk.word_tokenize(str1)
                tag = nltk.pos_tag(tok)
                gram = r"""chunk:{<EX>?<DT>?<JJ.?>*<NN.?|PRP|PRP\$|POS|IN|DT|CC|VBG|VBN>+<RB.?>*<VB.?|MD|RP>+}"""
                chunk_parse = nltk.RegexpParser(gram)
                chunked1 = chunk_parse.parse(tag)

                sec_list = identify_all.search_the_chunk(str1, chunked1)
                if len(sec_list) != 0:
                    m = sec_list[len(sec_list) - 1]

                    str4 = not_clause.get_chunk(chunked1[m])
                    str4 = identify_all.verbphrase_identify(str4)
                    str5 = ""
                    str6 = ""

                    for temp_3 in range(m):
                        if temp_3 in sec_list:
                            str5 += not_clause.get_chunk(chunked1[temp_3])
                        else:
                            str5 += (chunked1[temp_3][0] + " ")

                    for temp_3 in range(m + 1, len(chunked1)):
                        if temp_3 in sec_list:
                            str6 += not_clause.get_chunk(chunked1[temp_3])
                        else:
                            str6 += (chunked1[temp_3][0] + " ")

                    if chunked2[temp_2][1][1] == 'PRP':
                        tr = " whom "
                    else:
                        for x in range(len(chunk_ans[temp_2])):
                            if (chunk_ans[temp_2][x][1] == "NNP" or chunk_ans[temp_2][x][1] == "NNPS" or chunk_ans[temp_2][x][1] == "NNS" or
                                    chunk_ans[temp_2][x][1] == "NN"):
                                break

                        for x1 in range(len(ner)):
                            if ner[x1][0] == chunk_ans[temp_2][x][0]:
                                if ner[x1][1] == "PERSON":
                                    tr = " whom "
                                elif ner[x1][1] == "LOC" or ner[x1][1] == "ORG" or ner[x1][1] == "GPE":
                                    tr = " where "
                                elif ner[x1][1] == "TIME" or ner[x1][1] == "DATE":
                                    tr = " when "
                                else:
                                    tr = " what "

                    st = str5 + tr + str4 + str2 + str6 + str3
                    for l in range(num + 1, len(segment_set)):
                        st += ("," + segment_set[l])
                    st += '?'
                    st = identify_all.postprocess(st)
                    # st = 'Q.' + st
                    third_list.append(st)

    return third_list


def who(segment_set, num, ner):
    tok = nltk.word_tokenize(segment_set[num])
    tag = nltk.pos_tag(tok)
    gram = r"""chunk:{<EX>?<DT>?<JJ.?>*<NN.?|PRP|PRP\$|POS|IN|DT|CC|VBG|VBN>+<RB.?>*<VB.?|MD|RP>+}"""
    chunk_parse = nltk.RegexpParser(gram)
    chunk_ans = chunk_parse.parse(tag)

    first_list = identify_all.search_the_chunk(segment_set[num], chunk_ans)
    third_list = []

    if len(first_list) != 0:
        for temp_2 in range(len(first_list)):
            m = first_list[temp_2]
            str1 = ""
            for temp_3 in range(m + 1, len(chunk_ans)):
                if temp_3 in first_list:
                    str1 += not_clause.get_chunk(chunk_ans[temp_3])
                else:
                    str1 += (chunk_ans[temp_3][0] + " ")

            str2 = not_clause.get_chunk(chunk_ans[m])
            tok = nltk.word_tokenize(str2)
            tag = nltk.pos_tag(tok)

            for m11 in range(len(tag)):
                if tag[m11][1] == 'NNP' or tag[m11][1] == 'NNPS' or tag[m11][1] == 'NNS' or tag[m11][1] == 'NN':
                    break
            s11 = ' who '
            for m12 in range(len(ner)):
                if ner[m12][0] == tag[m11][0]:
                    if ner[m12][1] == 'LOC':
                        s11 = ' which place '
                    elif ner[m12][1] == 'ORG':
                        s11 = ' who '
                    elif ner[m12][1] == 'DATE' or ner[m12][1] == 'TIME':
                        s11 = ' what time '
                    else:
                        s11 = ' who '

            gram = r"""chunk:{<RB.?>*<VB.?|MD|RP>+}"""
            chunk_parse = nltk.RegexpParser(gram)
            chunked1 = chunk_parse.parse(tag)

            sec_list = identify_all.search_the_chunk(str2, chunked1)
            if len(sec_list) != 0:
                str2 = not_clause.get_chunk(chunked1[sec_list[0]])
                str2 = s11 + str2
                for temp_3 in range(sec_list[0] + 1, len(chunked1)):
                    if temp_3 in sec_list:
                        str2 += not_clause.get_chunk(chunk_ans[temp_3])
                    else:
                        str2 += (chunk_ans[temp_3][0] + " ")
                str2 += (" " + str1)

                tok_1 = nltk.word_tokenize(str2)
                str2 = ""
                for h in range(len(tok_1)):
                    if tok_1[h] == "am":
                        str2 += " is "
                    else:
                        str2 += (tok_1[h] + " ")

                for l in range(num + 1, len(segment_set)):
                    str2 += ("," + segment_set[l])
                str2 += '?'

                str2 = identify_all.postprocess(str2)
                # str2 = 'Q.' + str2
                third_list.append(str2)

    return third_list


def howmuch_2(segment_set, num, ner):
    tok = nltk.word_tokenize(segment_set[num])
    tag = nltk.pos_tag(tok)
    gram = r"""chunk:{<\$>*<CD>+<MD>?<VB|VBD|VBG|VBP|VBN|VBZ|RP>+}"""
    chunk_parse = nltk.RegexpParser(gram)
    chunk_ans = chunk_parse.parse(tag)

    first_list = identify_all.search_the_chunk(segment_set[num], chunk_ans)
    third_list = []

    if len(first_list) != 0:
        for temp_2 in range(len(first_list)):
            m = first_list[temp_2]
            str1 = ""
            for temp_3 in range(m + 1, len(chunk_ans)):
                if temp_3 in first_list:
                    str1 += not_clause.get_chunk(chunk_ans[temp_3])
                else:
                    str1 += (chunk_ans[temp_3][0] + " ")

            str2 = not_clause.get_chunk(chunk_ans[m])
            tok = nltk.word_tokenize(str2)
            tag = nltk.pos_tag(tok)
            gram = r"""chunk:{<RB.?>*<VB.?|MD|RP>+}"""
            chunk_parse = nltk.RegexpParser(gram)
            chunked1 = chunk_parse.parse(tag)
            s11 = ' how much '

            sec_list = identify_all.search_the_chunk(str2, chunked1)
            if len(sec_list) != 0:
                str2 = not_clause.get_chunk(chunked1[sec_list[0]])
                str2 = s11 + str2
                for temp_3 in range(sec_list[0] + 1, len(chunked1)):
                    if temp_3 in sec_list:
                        str2 += not_clause.get_chunk(chunk_ans[temp_3])
                    else:
                        str2 += (chunk_ans[temp_3][0] + " ")
                str2 += (" " + str1)

                tok_1 = nltk.word_tokenize(str2)
                str2 = ""
                for h in range(len(tok_1)):
                    if tok_1[h] == "am":
                        str2 += " is "
                    else:
                        str2 += (tok_1[h] + " ")

                for l in range(num + 1, len(segment_set)):
                    str2 += ("," + segment_set[l])
                str2 += '?'

                str2 = identify_all.postprocess(str2)
                # str2 = 'Q.' + str2
                third_list.append(str2)

    return third_list


def howmuch_1(segment_set, num, ner):
    tok = nltk.word_tokenize(segment_set[num])
    tag = nltk.pos_tag(tok)
    gram = r"""chunk:{<IN>+<\$>?<CD>+}"""
    chunk_parse = nltk.RegexpParser(gram)
    chunk_ans = chunk_parse.parse(tag)

    first_list = identify_all.search_the_chunk(segment_set[num], chunk_ans)
    third_list = []

    if len(first_list) != 0:
        for temp_2 in range(len(chunk_ans)):
            str1 = ""
            str2 = ""
            str3 = ""
            if temp_2 in first_list:
                for temp_3 in range(temp_2):
                    if temp_3 in first_list:
                        str1 += not_clause.get_chunk(chunk_ans[temp_3])
                    else:
                        str1 += (chunk_ans[temp_3][0] + " ")

                for temp_3 in range(temp_2 + 1, len(chunk_ans)):
                    if temp_3 in first_list:
                        str3 += not_clause.get_chunk(chunk_ans[temp_3])
                    else:
                        str3 += (chunk_ans[temp_3][0] + " ")

                str2 = ' ' + chunk_ans[temp_2][0][0] + ' how much '

                tok = nltk.word_tokenize(str1)
                tag = nltk.pos_tag(tok)
                gram = r"""chunk:{<EX>?<DT>?<JJ.?>*<NN.?|PRP|PRP\$|POS|IN|DT|CC|VBG|VBN>+<RB.?>*<VB.?|MD|RP>+}"""
                chunk_parse = nltk.RegexpParser(gram)
                chunked1 = chunk_parse.parse(tag)

                sec_list = identify_all.search_the_chunk(str1, chunked1)
                if len(sec_list) != 0:
                    m = sec_list[len(sec_list) - 1]

                    str4 = not_clause.get_chunk(chunked1[m])
                    str4 = identify_all.verbphrase_identify(str4)
                    str5 = ""
                    str6 = ""

                    for temp_3 in range(m):
                        if temp_3 in sec_list:
                            str5 += not_clause.get_chunk(chunked1[temp_3])
                        else:
                            str5 += (chunked1[temp_3][0] + " ")

                    for temp_3 in range(m + 1, len(chunked1)):
                        if temp_3 in sec_list:
                            str6 += not_clause.get_chunk(chunked1[temp_3])
                        else:
                            str6 += (chunked1[temp_3][0] + " ")

                    st = str5 + str2 + str4 + str6 + str3
                    for l in range(num + 1, len(segment_set)):
                        st += ("," + segment_set[l])
                    st += '?'
                    st = identify_all.postprocess(st)
                    # st = 'Q.' + st
                    third_list.append(st)

    return third_list


def howmuch_3(segment_set, num, ner):
    tok = nltk.word_tokenize(segment_set[num])
    tag = nltk.pos_tag(tok)
    gram = r"""chunk:{<MD>?<VB|VBD|VBG|VBP|VBN|VBZ>+<IN|TO>?<PRP|PRP\$|NN.?>?<\$>*<CD>+}"""
    chunk_parse = nltk.RegexpParser(gram)
    chunk_ans = chunk_parse.parse(tag)

    first_list = identify_all.search_the_chunk(segment_set[num], chunk_ans)
    third_list = []

    if len(first_list) != 0:
        for temp_2 in range(len(chunk_ans)):
            str1 = ""
            str2 = ""
            str3 = ""
            if temp_2 in first_list:
                for temp_3 in range(temp_2):
                    if temp_3 in first_list:
                        str1 += not_clause.get_chunk(chunk_ans[temp_3])
                    else:
                        str1 += (chunk_ans[temp_3][0] + " ")

                for temp_3 in range(temp_2 + 1, len(chunk_ans)):
                    if temp_3 in first_list:
                        str3 += not_clause.get_chunk(chunk_ans[temp_3])
                    else:
                        str3 += (chunk_ans[temp_3][0] + " ")

                strx = not_clause.get_chunk(chunk_ans[temp_2])
                tok = nltk.word_tokenize(strx)
                tag = nltk.pos_tag(tok)
                gram = r"""chunk:{<MD>?<VB|VBD|VBG|VBP|VBN|VBZ>+<IN|TO>?<PRP|PRP\$|NN.?>?}"""
                chunk_parse = nltk.RegexpParser(gram)
                chunked1 = chunk_parse.parse(tag)

                strx = not_clause.get_chunk(chunked1[0])
                str1 += (" " + strx)

                str2 = ' how much '

                tok = nltk.word_tokenize(str1)
                tag = nltk.pos_tag(tok)
                gram = r"""chunk:{<EX>?<DT>?<JJ.?>*<NN.?|PRP|PRP\$|POS|IN|DT|CC|VBG|VBN>+<RB.?>*<VB.?|MD|RP>+}"""
                chunk_parse = nltk.RegexpParser(gram)
                chunked1 = chunk_parse.parse(tag)

                sec_list = identify_all.search_the_chunk(str1, chunked1)

                if len(sec_list) != 0:
                    m = sec_list[len(sec_list) - 1]

                    str4 = not_clause.get_chunk(chunked1[m])
                    str4 = identify_all.verbphrase_identify(str4)
                    str5 = ""
                    str6 = ""

                    for temp_3 in range(m):
                        if temp_3 in sec_list:
                            str5 += not_clause.get_chunk(chunked1[temp_3])
                        else:
                            str5 += (chunked1[temp_3][0] + " ")

                    for temp_3 in range(m + 1, len(chunked1)):
                        if temp_3 in sec_list:
                            str6 += not_clause.get_chunk(chunked1[temp_3])
                        else:
                            str6 += (chunked1[temp_3][0] + " ")

                    st = str5 + str2 + str4 + str6 + str3

                    for l in range(num + 1, len(segment_set)):
                        st += ("," + segment_set[l])
                    st += '?'
                    st = identify_all.postprocess(st)
                    # st = 'Q.' + st
                    third_list.append(st)

    return third_list
