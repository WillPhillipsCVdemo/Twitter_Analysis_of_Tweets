from collections import Counter
import numpy as np
import matplotlib.pyplot as plt

###Change file to your search word file
file = open(r"SearchWord_tweets.txt", "r", encoding="utf-8-sig")

wordcount = Counter(file.read().split())


labels, values = zip(*wordcount.items())

indexes = np.arange(len(labels))
width = 1

plt.bar(indexes, values, width)
plt.xticks(indexes + width * 0.5, labels)
plt.show()

print(labels)