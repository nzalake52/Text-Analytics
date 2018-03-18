import urllib3
from bs4 import BeautifulSoup
import pandas as pd
import datetime as dt


urlOpener = urllib3.PoolManager()


navigationURL = ['https://timesofindia.indiatimes.com/city',
                 'https://timesofindia.indiatimes.com/india',
                 'https://timesofindia.indiatimes.com/world',
                 'https://timesofindia.indiatimes.com/business',
                 'https://timesofindia.indiatimes.com/sports',
                 'https://timesofindia.indiatimes.com/etimes',
                 'https://timesofindia.indiatimes.com/life-style']


all_urls = []
articleClass = []
for navUrlIndex in range(0, len(navigationURL)):
    page = urlOpener.urlopen('GET', navigationURL[navUrlIndex])
    soup = BeautifulSoup(page.data)
    type = navigationURL[navUrlIndex][str(navigationURL[1]).index('/', 10) + 1:]
    if type == 'etimes' or type == 'life-style':
        title = soup.find_all('li', attrs={'data-action':'SectionListing_NewsItem'})
    else:
        title = soup.find_all('span', attrs={'class': 'w_tle'})

    for i in range(0, len(title)):
        try:
            all_urls.append(navigationURL[navUrlIndex]+
                            str(title[i])[str(title[i]).find('href=') + 6:str(title[i]).find('.cms') + 4])
            articleClass.append(navigationURL[navUrlIndex][str(navigationURL[1]).index('/', 10)+1:])
        except:
            pass

set(articleClass)
titles = []
description = []
type = []
url = []
for urlIndex in range(0, len(all_urls)):
    print('Processing URL number: ',urlIndex)
    try:
        page = urlOpener.urlopen('GET', all_urls[urlIndex])
        soup = BeautifulSoup(page.data)

        desc = soup.find_all('div', attrs={'class':'section1'})
        description.append(desc[0].text)

        type.append(articleClass[urlIndex])

        url.append(all_urls[urlIndex])

        title = soup.find_all('h1')
        titles.append(title[0].text)

    except:
        pass

print(len(titles),len(description))

#Articles = pd.read_csv('D:/articles.csv')

Articles = pd.DataFrame(columns=['title','description'])
Articles['title'] = titles
Articles['description'] = description
Articles['url'] = url
Articles['type'] = type

pd.DataFrame.to_csv(Articles,'D:/articles'+str(dt.date.today())+'.csv')

from sklearn.feature_extraction.text import TfidfVectorizer
tfidf = TfidfVectorizer()
tfidfarray = tfidf.fit_transform(Articles['description']).toarray()

searchResult = []
count = 0
for file in Articles['description']:
    count += 1
    if 'Delhi' in file:
        searchResult.append(count-1)
str(searchResult)

tfidfSum = []
for i in searchResult:
    tfidfSum.append(sum(tfidfarray[i]))

index = pd.DataFrame({'score':tfidfSum})
index['index'] = searchResult
index.sort_values(by='score', ascending=False, inplace=True)

for i in index['index']:
    print(Articles['title'][i])


page = urlOpener.urlopen('GET', 'https://timesofindia.indiatimes.com/etimes')
soup = BeautifulSoup(page.data)

desc = soup.find_all('li', attrs={'data-action':'SectionListing_NewsItem'})
str(desc)[str(desc).find('href=') + 6:str(desc).find('.cms') + 4]
description.append(desc[0].text)

type.append(articleClass[urlIndex])

url.append(all_urls[urlIndex])

title = soup.find_all('h1', attrs = {'class':'heading1'})
titles.append(title[0].text)
