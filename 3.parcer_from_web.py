# import selenium
# import webdriver-manager
#
import time
from time import sleep

# vim test.py
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager

# options = Options()
# options.add_argument('--headless')
# options.add_argument('--no-sandbox')
# options.add_argument('--disable-dev-shm-usage')
browser = webdriver.Chrome()

browser.get("https://rozetked.me/news")
print(browser.title)

block = browser.find_element(By.CLASS_NAME, "feeds_holder")
all_news = block.find_elements(By.CSS_SELECTOR, ".block.article-preview.main-grid__block")

news_data = []
idx = 0
for news in all_news:
    idx += 1
    text = news.text.strip().split("\n")  # Разделяем текст по строкам
    link_element = news.find_element(By.CSS_SELECTOR, "a.article-preview__img-wrap")  # Находим ссылку
    link = link_element.get_attribute("href") if link_element else "Нет ссылки"

    news_data.append([idx, text[0], text[1], text[2], text[3], link])

df = pd.DataFrame(news_data, columns=["ID", "Заголовок", "Описание", "Дата", "Редактор", "Ссылка"])

df.to_csv("waste/news.csv", index=False, encoding="utf-8-sig")

# browser.find_element(By.XPATH, "http").click()


browser.close()