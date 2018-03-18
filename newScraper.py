import urllib3
from bs4 import BeautifulSoup
import pandas as pd
import datetime as dt


urlOpener = urllib3.PoolManager()


url = ['https://timesofindia.indiatimes.com/2017/1/6/archivelist/year-2017,month-1,starttime-42736.cms']
all_urls = []
for index in range(42736, 43100):
    all_urls.append('https://timesofindia.indiatimes.com/2017/1/6/archivelist/year-2017,month-1,starttime-'+str(index)+'.cms')

articleURLs = []
for urlIndex in range(0, len(all_urls)):
    print('Processing URL number: ', urlIndex)
    page = urlOpener.urlopen('GET', all_urls[urlIndex])
    soup = BeautifulSoup(page.data)
    title = soup.find_all('a')

    for i in range(0, len(title)):
        try:
            if(str(title[i]).find('life-style')>0 or str(title[i]).find('business')>0 or str(title[i]).find('world')>0
            or str(title[i]).find('city')>0 or str(title[i]).find('sports')>0 or str(title[i]).find('india')>0):
                url = str(title[i])[str(title[i]).find('href=') + 6:str(title[i]).find('.cms') + 4]
                if url != '' and url.find('http') < 0:
                    articleURLs.append('https://timesofindia.indiatimes.com/'+url)

        except:
            pass


articleURLFile = pd.DataFrame()
articleURLFile['url'] = articleURLs
pd.DataFrame.to_csv(articleURLFile, 'D:/articleURLFile.csv')

articleURLFile = pd.read_csv('D:/articleURLFile.csv')
articleURLs = articleURLFile['url']

titles = []
description = []
type = []
url = []
for urlIndex in range(30000, len(articleURLs)):
    try:
        print('Processing URL number: ', urlIndex)
        page = urlOpener.urlopen('GET', articleURLs[urlIndex])
        soup = BeautifulSoup(page.data)

        desc = soup.find_all('div', attrs={'class': 'section1'})
        title = soup.find_all('h1')

        if len(desc) > 0 and len(title) > 0:
            titles.append(title[0].text)
            description.append(desc[0].text)

            type.append(articleURLs[urlIndex][str(articleURLs[urlIndex]).index('//', 10) +
                              2:articleURLs[urlIndex].index('/', str(articleURLs[urlIndex]).index('//', 10) + 2)])

            url.append(articleURLs[urlIndex])


    except:
        pass

Articles = pd.DataFrame()
Articles['title'] = titles
Articles['description'] = description
Articles['type'] = type
Articles['url'] = url

pd.DataFrame.to_csv(Articles,'D:/articlesNew'+str(dt.datetime.now()).replace(':','-')+'.csv')

print(len(titles), len(description))
