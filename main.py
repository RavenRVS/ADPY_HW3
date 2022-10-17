import re

import bs4
import requests

KEYWORDS = ['дизайн', 'фото', 'web', 'python']

HEADERS = {
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'Connection': 'keep-alive',
    'Cookie': '_ym_uid=1629214409553807773; _ym_d=1650622887; fl=ru; hl=ru; _ga=GA1.2.881908085.1659094610;'
              'visited_articles=226521:591587:488054:591553:303168:666062:306166:227377:321076;'
              ' habr_web_home_feed=/all/; _ym_isad=2; _gid=GA1.2.2087202015.1665507362',
    'Host': 'habr.com',
    'Referer': 'https://habr.com/ru/all/',
    'sec-ch-ua': '"Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safa'
}

URL = "https://habr.com"


def get_all_articles_from_hubr():
    response = requests.get(URL, headers=HEADERS)
    text = response.text

    soup = bs4.BeautifulSoup(text, features="html.parser")

    response.close()
    return soup.find_all("article")


def find_articles_by_keywords(all_articles):
    for article in all_articles:
        hubs = article.find_all(class_="tm-article-snippet__hubs-item-link")
        hubs = [hub.text.strip() for hub in hubs]
        date_art = article.find(class_="tm-article-snippet__datetime-published").contents[0].attrs["title"]
        href = f'{URL}{article.find(class_="tm-article-snippet__title-link").attrs["href"]}'
        title = article.find("h2").find("span").text
        response2 = requests.get(href, headers=HEADERS)
        text2 = response2.text
        soup = bs4.BeautifulSoup(text2, features="html.parser")
        body_article = soup.find_all(
            class_="article-formatted-body article-formatted-body article-formatted-body_version-2")
        result = f"{date_art} - {title} - {href}"
        for keyword in KEYWORDS:
            search_in_hubs_result = False
            for hub in hubs:
                if re.search(keyword, hub, re.IGNORECASE) is not None:
                    search_in_hubs_result = True
                    break
            if search_in_hubs_result is False:
                for block in body_article:
                    if re.search(keyword, block.text, re.IGNORECASE) is not None:
                        search_in_hubs_result = True
                        break
            if search_in_hubs_result is True:
                print(result)
                break


articles = get_all_articles_from_hubr()
find_articles_by_keywords(articles)
