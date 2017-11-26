import re
import string
import matplotlib.pyplot as plt

frequency = {}
###Change file to your search word file
document_text = open('SearchWord_tweets.txt', 'r')
text_string = document_text.read().lower()
match_pattern = re.findall(r'\b[a-z]{3,15}\b', text_string)

for word in match_pattern:
    count = frequency.get(word, 0)
    frequency[word] = count + 1

frequency_list = frequency.keys()

dictionary = {}
sorted_dictionary = {}


for words in frequency_list:
    #print words, frequency[words]
    wordfreq = (frequency[words])

    if wordfreq > 250:
        dictionary.update({words: wordfreq})
        print(words, wordfreq)
    sorted_dictionary.update(sorted(dictionary.iteritems(), key=lambda (k, v): (-v, k))[:10])



print("#####################################")
#print(dictionary)
print(sorted_dictionary)
print(type(sorted_dictionary))


plt.bar(range(len(sorted_dictionary)), sorted_dictionary.values(), align='center')
plt.xticks(range(len(sorted_dictionary)), sorted_dictionary.keys())

plt.show()