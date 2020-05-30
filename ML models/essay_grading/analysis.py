import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from nltk import tokenize

data = pd.read_csv('dataset.csv')
scores = list(data['score'])


import matplotlib.pyplot as plt
import numpy as np
import collections



c = collections.Counter(scores)
c = sorted(c.items())
numbers = [i[0] for i in c]

freq = [i[1] for i in c]

f, ax = plt.subplots()


plt.bar(numbers, freq)
plt.title("Frequency of Scores")
plt.xlabel("Score")
plt.ylabel("Frequency")
ax.set_xticks(range(0, 11))
ax.set_xticklabels(numbers)

plt.show()
