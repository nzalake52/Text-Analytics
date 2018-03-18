import pandas as pd
import re

nyTimesFile = open('D:/Niranjan/Data Science/Semester 2/Python & ML data sets/nytimes_news_articles.txt', encoding='latin-1')
nyTimesFile.seek(0)
nyTimesV1 = nyTimesFile.readlines()
nyTimesTemp = []
nyTimesURL = []



for i in range(0, len(nyTimesV1)-1):
    if re.findall('URL', nyTimesV1[i]) == []:
        sent = sent + nyTimesV1[i]
        if (re.findall('URL', nyTimesV1[i+1]) != []) and (i+1 < len(nyTimesV1)):
            nyTimesTemp.append(sent.strip())
    else:
        sent = ''
        nyTimesURL.append(nyTimesV1[i])

for i in range(0, len(nyTimesTemp)):
    nyTimesTemp[i] = nyTimesTemp[i]+'articleID'+str(i)


from TextMining.TextPreprocessing import preProcessor
nytimes = preProcessor(nyTimesTemp)


def file_indexing(file):
    fileIndex = {}
    for index, word in enumerate(file):
        if word in fileIndex.keys():
            fileIndex[word].append(index)
        else:
            fileIndex[word] = [index]
    return fileIndex

nyTimesIndex = {}
for sent in nytimes:
    nyTimesIndex[' '.join(sent)] = file_indexing(sent)


def fullIndex(intIndex):
    totalindex = {}
    for fileName in intIndex.keys():
        for word in intIndex[fileName].keys():
            if word in totalindex.keys():
                if fileName in totalindex[word].keys():
                    totalindex[word][fileName].extend(intIndex[fileName][word][:])
                else:
                    totalindex[word][fileName] = intIndex[fileName][word]
            else:
                totalindex[word] = {fileName : intIndex[fileName][word]}
    return totalindex

nyTimesIndexV1 = fullIndex(nyTimesIndex)

def wordSearch(word, index):
    if word in index.keys():
        return [file for file in index[word].keys()]

def phraseQuery(string, index):
    lists, result = [], []
    for word in string.split():
        lists.append(wordSearch(word, index))
    setList = set(lists[0]).intersection(*lists)
    for fileName in setList:
        result.append(fileName)
    #     temp = []
    #     for word in string.split():
    #         temp.append(nyTimesIndexV1[word][fileName][:])
    #     for i in range(len(temp)):
    #         for ind in range(len(temp[i])):
    #             temp[i][ind] = temp[i][ind] - i
    #     if set(temp[0]).intersection(*temp):
    #         result.append(fileName)
    return result



searchResult = phraseQuery('kanye west', nyTimesIndexV1)
searchResult1 = []
for file in wordSearch('kanye', nyTimesIndexV1):
    searchResult1.append(file)
for file in wordSearch('west', nyTimesIndexV1):
    if file not in searchResult1:
        searchResult1.append(file)


from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
tfidf = TfidfVectorizer().fit(searchResult1)
searchResult1TFIDF = tfidf.transform(searchResult1)
searchResultTFIDF = tfidf.transform(searchResult)
sims = cosine_similarity(searchResult1TFIDF, searchResultTFIDF)


cosineSum = []
for ind in range(len(sims)):
    cosineSum.append(sum(sims[ind]))

sumDF = pd.DataFrame({'score':cosineSum})
sumDF['index'] = [i for i in range(len(cosineSum))]
sumDF.sort_values(by='score', inplace=True, ascending=False)


for ind in sumDF['index']:
    print(nyTimesURL[int(searchResult1[ind][str(searchResult1[ind]).find('articleid')+9:])], '\n')