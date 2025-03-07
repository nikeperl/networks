import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By

from datetime import datetime


def parse_datetime(date_str: str) -> datetime:
    formats = [
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d %H:%M",
        "%Y-%m-%d",
        "%Y-%m",
        "%Y",
        "%d.%m.%Y %H:%M:%S",
        "%d.%m.%Y %H:%M",
        "%d.%m.%Y",
        "%d.%m",
        "%d/%m/%Y %H:%M:%S",
        "%d/%m/%Y %H:%M",
        "%d/%m/%Y",
        "%d/%m",
    ]

    for fmt in formats:
        try:
            dt = datetime.strptime(date_str, fmt)
            return datetime(
                dt.year if '%Y' in fmt else datetime.now().year,
                dt.month if '%m' in fmt else 1,
                dt.day if '%d' in fmt else 1,
                dt.hour if hasattr(dt, 'hour') else 0,
                dt.minute if hasattr(dt, 'minute') else 0,
                dt.second if hasattr(dt, 'second') else 0
            )
        except ValueError:
            continue

    print("Дата не установлена")
    return None


last_date = parse_datetime(input(
    "Введите дату от которой собрать новости: "))  # Здесь можно поставить дату от которой до текущего момента будут сохранены новости datetime(2025, 2, 26)

options = webdriver.ChromeOptions()
# options.add_argument("--headless=new")
options.add_argument("--blink-settings=imagesEnabled=false")
browser = webdriver.Chrome(options=options)

BASE_URL = "https://rozetked.me/news"
browser.get(BASE_URL)
print(browser.title)

pagination = browser.find_elements(By.CSS_SELECTOR, ".pagination__item a")
if pagination:
    last_page = int(pagination[-1].text)
else:
    last_page = 2

# Инициализация таблицы
df_header = pd.DataFrame(columns=["Заголовок", "Описание", "Дата", "Редактор", "Ссылка"])
df_header.to_csv("waste/news.csv", index=False, encoding='utf-8-sig')

for page in range(1, last_page):
    print(f"Собираем данные со страницы {page}...")
    browser.get(f"{BASE_URL}?page={page}")

    blocks = browser.find_element(By.CLASS_NAME, "feeds_holder")
    all_news = blocks.find_elements(By.CLASS_NAME, "block")

    for news in all_news:
        title_element = news.find_element(By.CLASS_NAME, "link")
        title = title_element.text if title_element else "Нет Заголовка"
        link = title_element.get_attribute("href") if title_element else "Нет ссылки"
        text_element = news.find_element(By.CLASS_NAME, "article-preview__text")
        text = text_element.text if text_element else "Нет Описания"
        date_element = news.find_element(By.CLASS_NAME, "article-preview__date")
        date = date_element.get_attribute("data-datum") if date_element else "Нет даты"
        author_element = news.find_element(By.CLASS_NAME, "article-preview__author")
        author = author_element.text if date_element else "Нет автора"

        # Заканчиваем программу если выходим за рамки даты
        if last_date and datetime.strptime(date, "%Y-%m-%d %H:%M:%S") < last_date:
            browser.close()
            exit()

        df = pd.DataFrame([[title, text, date, author, link]],
                          columns=["Заголовок", "Описание", "Дата", "Редактор", "Ссылка"])
        df.to_csv("waste/news.csv", index=False, mode='a', header=False, encoding='utf-8-sig')

browser.close()
