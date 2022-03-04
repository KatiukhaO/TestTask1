import requests, re, csv
import pandas as pd
from openpyxl.workbook import Workbook
from bs4 import BeautifulSoup
from config import URL, HEADER, MAIN_URL, file_name, file_name_xlsx


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

def save_doc_csv(items, path):
    with open(path, "w", encoding="utf-16") as file:
        writer = csv.writer(file, delimiter=",")
        writer.writerow(["Model phones", "Price", "Link by description", "Link by site"])
        for item in  items:
            writer.writerow([item["model"], item["price"], item["link_by_model"], item["link_by_site"]])


def save_doc_xls(items, path):
    z = pd.DataFrame(items)
    z.to_excel(path, index=False )


def parser():
    PAGINATION = int(input("Enter number pages for pagination's : "))
    html = get_html(URL)
    if html.status_code == 200:
        cards = []
        for page in range(1, PAGINATION+1):
            print(f"Parsing pages number : {page}")
            p = f"?p={page}"
            html = get_html(URL+p)
            cards.extend(get_content(html))
            save_doc_xls(cards, file_name_xlsx)
            # save_doc_csv(cards, file_name)
        print(f"We have {len(cards)} recording in our file")
    else:
        print("Error")

if __name__ == "__main__":
    parser()







