import requests
from bs4 import BeautifulSoup
import sqlite3
import pandas as pd

# 假設我們從一個簡單的新聞網站取得標題
def fetch_news():
    url = 'https://example-news-site.com'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    articles = soup.find_all('h2', class_='article-title')
    data = [(article.text, article.a['href']) for article in articles]
    return data

# 存入SQLite
def save_to_db(data):
    conn = sqlite3.connect('news.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS news (title TEXT, link TEXT)')
    cursor.executemany('INSERT INTO news VALUES (?, ?)', data)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    news_data = fetch_news()
    save_to_db(news_data)
