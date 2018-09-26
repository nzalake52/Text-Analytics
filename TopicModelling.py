from nltk.tokenize import word_tokenize
import re
import string

file = open('D:/Niranjan/Data Science/Semester 2/Python & ML data sets/twitter_stream.txt', mode='r',encoding='utf-8')
twitter_stream = []
file.seek(0)
twitter_stream = file.readlines()
twitter_stream[17]


from nltk.tokenize import word_tokenize
twitter_tokenized = [word_tokenize(word) for word in twitter_stream]
print(len(twitter_stream),len(twitter_tokenized))
twitter_tokenized[1]

from nltk.corpus import stopwords
stopwordsEng = stopwords.words('english')

twitter_withoutStopwords = []
for sent in twitter_tokenized:
    new_sent = []
    for word in sent:
        if word not in stopwordsEng:
            new_sent.append(word)
    twitter_withoutStopwords.append(new_sent)

from nltk.stem import wordnet
wordnetLemma = wordnet.WordNetLemmatizer()
twitter_lemmatized = []

for sent in twitter_withoutStopwords:
    new_sent = []
    for word in sent:
        new_token = wordnetLemma.lemmatize(word)
        if new_token != '':
            new_sent.append(new_token)
    twitter_lemmatized.append(new_sent)

print(twitter_tokenized[7])
print(twitter_lemmatized[7])

regex = re.compile('[%s]' % re.escape(string.punctuation))
twitter_withoutPunc = []
for sent in twitter_lemmatized:
    new_sent = []
    for word in sent:
        if regex.sub('', word) != '':
            new_sent.append(regex.sub('', word))
    twitter_withoutPunc.append(new_sent)

print(twitter_tokenized[7])
print(twitter_lemmatized[7])
print(twitter_withoutPunc[7])

import gensim
from gensim import corpora

dictionary = corpora.Dictionary(twitter_withoutPunc)
corpus = [dictionary.doc2bow(doc) for doc in twitter_withoutPunc]
ldamodel = gensim.models.LdaMulticore(corpus,num_topics=1,id2word=dictionary,passes=1,workers=3)
print(ldamodel.print_topics(num_topics=4,num_words=5))
print(ldamodel.id2word)