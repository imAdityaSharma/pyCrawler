from bs4 import BeautifulSoup
import requests
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize as wt
import asyncio

class crawler:
    def __init__(self, lpassed):

        self.links = [lpassed]

    def remove_stopwords(self, text):
        stopWords = set(stopwords.words('english'))
        words = wt(text)
        filtered_words = [word for word in words if word.lower() not in stopWords]
        return ' '.join(filtered_words)

    async def crawler(self):
        url_regex = re.compile(r'https?://\S+')
        content = {}
        flag = 0
        for i in self.links:
            flag+=1
            response = requests.get(i)
            if response.status_code == 200:
                soup: BeautifulSoup = BeautifulSoup(response.content, 'html.parser')
                title = soup.title.string if soup.title else "No Title Found"
                textinfo = self.remove_stopwords(soup.get_text())
                content['title'] = {'link': i, 'info': textinfo}
                all_page_links = [link.get('href') for link in soup.find_all('a')]
                for link in all_page_links:
                    if link is None:
                        continue
                    else:
                        if url_regex.match(link) and \
                                not re.search(r'privacy(?:-|_)?(?:policy|notice)|terms(?:-|_)?of(?:-|_)?service', link,
                                              re.IGNORECASE) \
                                and not re.search(r'\.(exe|pdf|zip|rar|tar|gz|dmg|iso)$', link, re.IGNORECASE):
                            self.links.append(link)
                            # print(link)
                if flag ==10:
                    yield content
                    await asyncio.sleep(5)
                    flag =0
                else: continue
            else:
                continue
