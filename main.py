import requests
import csv
from bs4 import BeautifulSoup
from config import URL, HEADER, MAIN_URL
import re


def get_html(url, params=""):
    r = requests.get(url, headers=HEADER, params=params)
    return r


def get_content(html):
    soup = BeautifulSoup(html.text, "html.parser")
    items = soup.find_all("div", class_="products-list-item products-catalog-grid__item products-list-item--grid")
    prices = []
    for item in items:
        prices.append(item.find("div", {"class" : "products-list-item__actions-price-current"}))
    clear_prices = []
    for s in list(map(str, prices)):
        digits_price = re.findall(r"\ (\d+\ \d+)", s)
        if digits_price:
            clear_prices.append(digits_price[0])
        else:
            clear_prices.append("Очікується")
    cards = []
    for s, item in zip(clear_prices, items):
        cards.append(
            {
                "model": item.find("div", class_="products-list-item__info").find("a").get_text(strip=True),
                "price": s ,
                "link_by_model": item.find("div", class_="products-list-item__info").find("a").get("href"),
                "link_by_site" : MAIN_URL
            }
        )

    return cards




print(get_content(get_html(URL)))


