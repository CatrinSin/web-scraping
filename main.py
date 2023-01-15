import bs4
import requests
from fake_headers import Headers

KEYWORDS = {'Сегодня', 'проект', 'параметры', 'web', 'Python'}

HEADERS = Headers(browser="chrome", os="win", headers=True).generate()

URL = "https://habr.com/ru/all/"

response = requests.get(URL, headers=HEADERS)
text = response.text

soup = bs4.BeautifulSoup(text, features='html.parser')

articles = soup.find_all("article")
for article in articles:
    previews = article.find_all(class_='tm-article-body tm-article-snippet__lead')
    previews = [preview.text.strip() for preview in previews]
    for preview in previews:
        preview = preview.split()
        preview = [p.strip('!.,:;"«» ”') for p in preview]
        preview = set(preview)
        # print(preview)
        if preview.intersection(KEYWORDS):
            date = article.find(class_='tm-article-snippet__datetime-published').find('time').text
            title = article.find(class_='tm-article-snippet__title tm-article-snippet__title_h2').find('span').text
            href = article.find(class_='tm-article-snippet__title-link').attrs['href']
            print(f' <{date}> - <{title}> - <https://habr.com{href}>')


