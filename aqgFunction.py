import spacy
import clause
import not_clause
import identify_all
import nlpNER


class AutomaticQuestionGenerator():
    # AQG Parsing & Generate a question
    def aqgParse(self, sentence):
        print("HERE*******")
        nlp = spacy.load('en_core_web_md')
        print("*********LOADED SPACY MODEl")
        single_sentences = sentence.split(".")
        list_of_ques = []
        if len(single_sentences) != 0:
            for i in range(len(single_sentences)):
                segmentSets = single_sentences[i].split(",")

                tagger = nlpNER.tagger_func(nlp, single_sentences[i])

                if (len(segmentSets)) != 0:
                    for j in range(len(segmentSets)):
                        try:
                            list_of_ques += clause.howmuch_2(segmentSets, j, tagger)
                        except Exception:
                            pass

                        if identify_all.identify_the_clause(segmentSets[j]) == 1:
                            try:
                                list_of_ques += clause.whom_1(segmentSets, j, tagger)
                            except Exception:
                                pass
                            try:
                                list_of_ques += clause.whom_2(segmentSets, j, tagger)
                            except Exception:
                                pass
                            try:
                                list_of_ques += clause.whom_3(segmentSets, j, tagger)
                            except Exception:
                                pass
                            try:
                                list_of_ques += clause.whose(segmentSets, j, tagger)
                            except Exception:
                                pass
                            try:
                                list_of_ques += clause.what_to_do(segmentSets, j, tagger)
                            except Exception:
                                pass
                            try:
                                list_of_ques += clause.who(segmentSets, j, tagger)
                            except Exception:
                                pass
                            try:
                                list_of_ques += clause.howmuch_1(segmentSets, j, tagger)
                            except Exception:
                                pass
                            try:
                                list_of_ques += clause.howmuch_3(segmentSets, j, tagger)
                            except Exception:
                                pass


                            else:
                                try:
                                    s = identify_all.subjectphrase_search(segmentSets, j)
                                except Exception as e: print(e)

                                if len(s) != 0:
                                    segmentSets[j] = s + segmentSets[j]
                                    try:
                                        list_of_ques += clause.whom_1(segmentSets, j, tagger)
                                    except Exception:
                                        pass
                                    try:
                                        list_of_ques += clause.whom_2(segmentSets, j, tagger)
                                    except Exception:
                                        pass
                                    try:
                                        list_of_ques += clause.whom_3(segmentSets, j, tagger)
                                    except Exception:
                                        pass
                                    try:
                                        list_of_ques += clause.whose(segmentSets, j, tagger)
                                    except Exception:
                                        pass
                                    try:
                                        list_of_ques += clause.what_to_do(segmentSets, j, tagger)
                                    except Exception:
                                        pass
                                    try:
                                        list_of_ques += clause.who(segmentSets, j, tagger)
                                    except Exception:
                                        pass

                                    else:
                                        try:
                                            list_of_ques += not_clause.what_whom1(segmentSets, j, tagger)
                                        except Exception:
                                            pass
                                        try:
                                            list_of_ques += not_clause.what_whom2(segmentSets, j, tagger)
                                        except Exception:
                                            pass
                                        try:
                                            list_of_ques += not_clause.whose(segmentSets, j, tagger)
                                        except Exception:
                                            pass
                                        try:
                                            list_of_ques += not_clause.howmany(segmentSets, j, tagger)
                                        except Exception:
                                            pass
                                        try:
                                            list_of_ques += not_clause.howmuch_1(segmentSets, j, tagger)
                                        except Exception:
                                            pass

                list_of_ques.append('\n')
        return list_of_ques



    def DisNormal(self, str):
        print("\n")
        print("------X------")
        print("Start  output:\n")

        count = 0
        out = ""

        for i in range(len(str)):
            count = count + 1
            print("Q-0%d: %s" % (count, str[i]))

        print("")
        print("End  OutPut")
        print("-----X-----\n\n")
