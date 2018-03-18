import re
from nltk import word_tokenize
import string
import  gensim.models as md
from gensim.models.phrases import Phrases, Phraser

def preProcessor(textFile):
    print('Starting pre-processing of the corpus..')
    print('Start: Word Tokenizing')

    textFilev1 = []
    textFilev1 = [word_tokenize(sent) for sent in textFile]

    print('Stop: Word Tokenizing')
    print('Start: ASCII encoding for special characters')

    textFilev2 = []
    for sent in textFilev1:
        new_sent = []
        for word in sent:
            new_word = word.encode('ascii', 'ignore').decode('utf-8')
            if new_word != '':
                new_sent.append(new_word)
        textFilev2.append(new_sent)

    print('Stop: ASCII encoding for special characters')
    print('Start: Stopwords Removal')

    stopwordsFile = open('D:/Niranjan/Data Science/Semester 2/Python & ML data sets/stopwords.txt')
    stopwordsFile.seek(0)
    stopwordsV1 = stopwordsFile.readlines()
    stopwordsV2 = []
    for sent in stopwordsV1:
        sent.replace('\n', '')
        new_word = sent[0:len(sent) - 1]
        stopwordsV2.append(new_word.lower())

    textFilev1 = []
    for sent in textFilev2:
        new_sent = []
        for word in sent:
            if word.lower() not in stopwordsV2:
                new_sent.append(word.lower())
        textFilev1.append(new_sent)

    print('Stop: Stopwords Removal')
    print('Start: Punctuation Removal')

    textFilev2 = []
    for sent in textFilev1:
        new_sent = []
        for word in sent:
            if word not in string.punctuation:
                new_sent.append(word)
        textFilev2.append(new_sent)

    print('Stop: Punctuation Removal')
    print('Start: Phrase Detection')

    textFilev1 = []
    common_terms = ["of", "with", "without", "and", "or", "the", "a", "so", "and"]
    phraseTrainer = Phrases(textFilev2, delimiter=b' ', common_terms=common_terms)
    phraser = Phraser(phraseTrainer)
    for article in textFilev2:
        textFilev1.append((phraser[article]))

    print('Stop: Phrase Detection')

    return textFilev1