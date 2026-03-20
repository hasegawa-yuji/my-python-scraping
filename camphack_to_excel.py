import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# 1. 設定
URL = "https://camphack.nap-camp.com/"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

print("情報を取得中...")
response = requests.get(URL, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')

# 2. 記事タイトルを取得（最新のクラス名に対応）
# サイトの構造によって 'p' だったり 'h2' だったりするため、より広く探します
articles = soup.select('.articleList__title, .articleCard__title')

data_list = []
print("\n--- 取得結果 ---")

# 3. 上から3つを取り出す
for i, article in enumerate(articles[:3], 1):
    title = article.get_text(strip=True)
    print(f"{i}位: {title}")
    data_list.append({"順位": i, "記事タイトル": title})
    time.sleep(1)

# 4. Excel保存
if data_list:
    df = pd.DataFrame(data_list)
    # ファイル名は「camp_ranking.xlsx」
    df.to_excel("camp_ranking.xlsx", index=False)
    print("\n✅ camp_ranking.xlsx という名前で保存しました！")
else:
    print("\n❌ データが見つかりませんでした。URLやクラス名を確認してください。")