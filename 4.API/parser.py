from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By


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

    return None

def parse_news(news):
    title_element = news.find_element(By.CLASS_NAME, "link")
    title = title_element.text if title_element else "Нет Заголовка"
    link = title_element.get_attribute("href") if title_element else "Нет ссылки"

    text_element = news.find_element(By.CLASS_NAME, "article-preview__text")
    text = text_element.text if text_element else "Нет Описания"

    date_element = news.find_element(By.CLASS_NAME, "article-preview__date")
    date = date_element.get_attribute("data-datum") if date_element else "Нет даты"

    author_element = news.find_element(By.CLASS_NAME, "article-preview__author")
    author = author_element.text if date_element else "Нет автора"

    return {
        "title": title,
        "description": text,
        "date": date,
        "author": author,
        "link": link
    }


def parse_website(url, date_str=None):
    last_date = parse_datetime(date_str)
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless=new")
    options.add_argument("--blink-settings=imagesEnabled=false")
    browser = webdriver.Chrome(options=options)
    
    browser.get(url)
    print(f"Собераем данные с сайта: {browser.title}")
    
    pagination = browser.find_elements(By.CSS_SELECTOR, ".pagination__item a")
    if pagination:
        last_page = int(pagination[-1].text)
    else:
        last_page = 2

    news_data = []
    for page in range(1, last_page):
        print(f"Собираем данные со страницы {page}...")
        browser.get(f"{url}?page={page}")
    
        blocks = browser.find_element(By.CLASS_NAME, "feeds_holder")
        all_news = blocks.find_elements(By.CLASS_NAME, "block")
    
        for news in all_news:
            news_dict = parse_news(news)

            # Заканчиваем программу если выходим за рамки даты
            if last_date and datetime.strptime(news_dict["date"], "%Y-%m-%d %H:%M:%S") < last_date:
                browser.close()
                return news_data

            news_data.append(news_dict)
    
    browser.close()
    return news_data
