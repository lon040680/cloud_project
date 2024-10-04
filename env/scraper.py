import requests
from bs4 import BeautifulSoup
import sqlite3

# 假設我們從一個簡單的新聞網站取得標題
def fetch_news():
    url = 'https://news.google.com/home?hl=zh-TW&gl=TW&ceid=TW:zh-Hant'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    articles = soup.find_all('a', class_='gPFEn')
    # 遍歷結果並列印出標題和連結
    for article in articles:
        title = article.text
        link = article['href']
        # print(f"Title: {title}")
        # print(f"Link: {link}")
    
    # 如果沒有找到文章，返回一個空列表
    if not articles:
        print("No articles found")
        return []

    data = [(article.text, article['href']) for article in articles]
    return data
    
# 存入SQLite
def save_to_db(data):
    conn = sqlite3.connect('news.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS news (title TEXT, link TEXT)')
    cursor.executemany('INSERT INTO news VALUES (?, ?)', data)
    conn.commit()
    conn.close()

def fetch_from_db():
    # 連接到資料庫
    conn = sqlite3.connect('news.db')
    cursor = conn.cursor()
    
    # 執行查詢命令
    cursor.execute('SELECT * FROM news')
    
    # 獲取並列印資料
    rows = cursor.fetchall()
    for row in rows:
        print(f"Title: {row[0]}")
    
    # 關閉資料庫連線
    conn.close()

if __name__ == "__main__":
    news_data = fetch_news()
    save_to_db(news_data)
    fetch_from_db()
