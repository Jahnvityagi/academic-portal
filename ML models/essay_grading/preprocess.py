import xlrd
import csv

def csv_from_excel():
    wb = xlrd.open_workbook('asap-aes/training_set_rel3.xlsx')
    sh = wb.sheet_by_name('training_set')
    your_csv_file = open('data.csv', 'w+')
    wr = csv.writer(your_csv_file, quoting=csv.QUOTE_ALL)

    for rownum in range(sh.nrows):
        wr.writerow(sh.row_values(rownum))

    your_csv_file.close()
    
#csv_from_excel()

import pandas as pd

data = pd.read_csv('data.csv')

essays_1 = list(data['essay'][i] for i in range(len(data['essay'])) if data['essay_set'][i]==1)
essays_2 = list(data['essay'][i] for i in range(len(data['essay'])) if data['essay_set'][i]==2)
essays_7 = list(data['essay'][i] for i in range(len(data['essay'])) if data['essay_set'][i]==7)
essays_8 = list(data['essay'][i] for i in range(len(data['essay'])) if data['essay_set'][i]==8)

scores_1 = list(data['domain1_score'][i] for i in range(len(data['domain1_score'])) if data['essay_set'][i]==1) #range = 2-12
scores_2 = list(data['domain1_score'][i] + data['domain2_score'][i] for i in range(len(data['domain1_score'])) if data['essay_set'][i]==2) #range = 2-10
scores_7 = list(data['domain1_score'][i] for i in range(len(data['domain1_score'])) if data['essay_set'][i]==7) #range = 0-30
scores_8 = list(data['domain1_score'][i] for i in range(len(data['domain1_score'])) if data['essay_set'][i]==8) #range = 0-60


#normalize scores between 0 to 100
scores_1 = list( int(((scores_1[i]-2)/10)*10) for i in range(len(scores_1)))
scores_2 = list( int(((scores_2[i]-2)/8)*10) for i in range(len(scores_2)))
scores_7 = list( int(((scores_7[i]-0)/30)*10) for i in range(len(scores_7)))
scores_8 = list( int(((scores_8[i]-0)/60)*10) for i in range(len(scores_8)))

data = []

data.append(['essay', 'topic', 'score', 'word_length'])

for i in range(len(essays_1)):
    data.append([essays_1[i],'''More and more people use computers, but not everyone agrees that this benefits society. Those who support advances in technology believe that
    computers have a positive effect on people. They teach hand-eye coordination,
    give people the ability to learn about faraway places and people, and even
    allow people to talk online with other people. Others have different ideas.
    Some experts are concerned that people are spending too much time on their
    computers and less time exercising, enjoying nature, and interacting with
    family and friends. Write a letter to your local newspaper in which you state
    your opinion on the effects computers have on people. Persuade the readers to
    agree with you.''', scores_1[i],350])

for i in range(len(essays_2)):
    data.append([essays_2[i],'''Censorship in the Libraries: "All of us can think of a book that we hope none of our children or any other children have taken off the shelf. But if
    I have the right to remove that book from the shelf -- that work I abhor --
    then you also have exactly the same right and so does everyone else.
    And then we have no books left on the shelf for any of us." --Katherine
    Paterson, Author. Write a persuasive essay to a newspaper reflecting your
    vies on censorship in libraries. Do you believe that certain materials,
    such as books, music, movies, magazines, etc., should be removed from the
    shelves if they are found offensive? Support your position with convincing
    arguments from your own experience, observations, and/or reading.''', scores_2[i],350])

for i in range(len(essays_7)):
    data.append([essays_7[i], '''Write about patience. Being patient means that you are understanding and
    tolerant. A patient person experience difficulties without complaining.
    Do only one of the following: write a story about a time when you were patient
    OR write a story about a time when someone you know was patient OR write a
    story in your own way about patience.''' , scores_7[i],250])

for i in range(len(essays_8)):
    data.append([essays_8[i], '''We all understand the benefits of laughter. For example, someone once
    said, “Laughter is the shortest distance between two people.” Many
    other people believe that laughter is an important part of any relationship.
    Tell a true story in which laughter was one element or part.''' , scores_8[i],650])

pd.DataFrame(data).to_csv('dataset.csv', index=False)
