from bs4 import BeautifulSoup
import requests
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize as wt
links=['https://www.geeksforgeeks.org/']
url_regex = re.compile(r'https?://\S+')

def remove_stopwords(text):
    stopWords = set(stopwords.words('english'))
    words = wt(text)
    filtered_words = [word for word in words if word.lower() not in stopWords]
    return ' '.join(filtered_words)

content = {}
def crawler():
    for i in links:
        response = requests.get(i)
        if response.status_code == 200:
            soup: BeautifulSoup = BeautifulSoup(response.content, 'html.parser')
            title = soup.title.string if soup.title else "No Title Found"
            textinfo = remove_stopwords(soup.get_text())
            content['title']={'link':i,'info':textinfo}
            alll = [link.get('href') for link in soup.find_all('a')]
            for link in alll:
                if link is None:
                    continue
                else:
                    if url_regex.match(link) and \
                        not re.search(r'privacy(?:-|_)?(?:policy|notice)|terms(?:-|_)?of(?:-|_)?service', link, re.IGNORECASE)\
                            and not re.search(r'\.(exe|pdf|zip|rar|tar|gz|dmg|iso)$', link, re.IGNORECASE):
                        links.append(link)
                        # print(link)
            print(content)
        else:
            continue


crawler()
