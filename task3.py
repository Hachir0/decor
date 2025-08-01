import requests
import bs4
from bs4 import BeautifulSoup
import datetime

KEYWORDS = ['дизайн', 'фото', 'web', 'python']

def logger(path):
    def __logger(old_function):
        def new_function(*args, **kwargs):
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_entry = f"{timestamp} - {old_function.__name__} - args: {args}, kwargs: {kwargs}\n"

            with open(f'{path}', "a", encoding="utf-8") as log_file:
                log_file.write(log_entry)

            result = old_function(*args, **kwargs)

            with open(f"{path}", "a", encoding="utf-8") as log_file:
                log_file.write(f"Результат: {result}\n\n")

            return result

        return new_function

    return __logger


@logger('search_keywords.log')
def search_keywords(txt):
    txt = txt.lower()
    for key in KEYWORDS:
        if key in txt:
            return True
    return False


@logger('habr_parser.log')
def parse_habr_articles():

    resp = requests.get("https://habr.com/ru/articles/")
    soup = bs4.BeautifulSoup(resp.text, features='html.parser')
    articles = soup.find("div", class_="tm-articles-list")
    article_list = articles.find_all("article", class_="tm-articles-list__item")

    for artic in article_list:
        link = artic.find("a", class_="tm-title__link")['href']
        res = requests.get(f'https://habr.com{link}')
        art_soup = bs4.BeautifulSoup(res.text, features='html.parser')
        text_ = art_soup.find("div", class_="tm-article-body")

        if search_keywords(text_.text):
            a = "True"
        else:
            a = "False"

        title = art_soup.find("h1", class_="tm-title tm-title_h1")
        date = art_soup.find("time")["title"]
        print(f"Название статьи: {title.text}")
        print(f'Ссылка: https://habr.com{link}')
        print(f'Статья была опубликована: {date}')

        if a == 'True':
            print("В данной статье есть ключевое-(ые) слово-(а)!")
        else:
            print("В данной статье нет ключевых слов!")

        print("----------------------------------------------------------------------------------------")


if __name__ == '__main__':
    parse_habr_articles()