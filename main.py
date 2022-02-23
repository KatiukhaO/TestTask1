import requests
import csv
from bs4 import BeautifulSoup
from config import URL, HEADER


def get_html(url, params=""):
    r = requests.get(url, headers=HEADER, params=params)
    return r


def get_content(html):
    soup = BeautifulSoup(html.text, "html.parser")
    items = soup.find_all("div", class_="products-list-item products-catalog-grid__item products-list-item--grid")
    cards_phones = []
    for item in items:
        cards_phones.append(
            {
                "model": item.find("div", class_="products-list-item__info").find("a").get_text(strip=True),
                #"price": item.find("div", class_="products-list-item__actions-price-current").get_text(strip=True),       # не працює
                "link_by_model": item.find("div", class_="products-list-item__info").find("a").get("href")
            }
        )


    return cards_phones


# print(get_html(URL).text)
print(get_content(get_html(URL)))
