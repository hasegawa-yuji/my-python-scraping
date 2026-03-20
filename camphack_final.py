import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import os

# 保存先のパスを取得（今のフォルダ）
current_dir = os.path.dirname(__file__)
file_path = os.path.join(current_dir, "camp_ranking.xlsx")

URL = "https://camphack.nap-camp.com/"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

print("CAMP HACKから情報を取得中...")

try:
    response = requests.get(URL, headers=headers, timeout=10)
    response.raise_for_status() # エラーがあればここで止める
    soup = BeautifulSoup(response.text, 'html.parser')

    # 修正ポイント：タイトルが含まれる可能性のある全てのリンクテキストを探す
    # aタグ（リンク）の中から、記事タイトルっぽいものを抽出
    articles = soup.select('a p, a h2, .articleList__title')

    data_list = []
    unique_titles = set() # 重複除け

    for article in articles:
        title = article.get_text(strip=True)
        # 短すぎるテキストや重複を除外
        if len(title) > 10 and title not in unique_titles:
            unique_titles.add(title)
            data_list.append({"順位": len(data_list) + 1, "記事タイトル": title})
        
        if len(data_list) >= 3: # 3つ見つかったら終了
            break

    if data_list:
        print("\n--- 取得成功！最新TOP3 ---")
        for item in data_list:
            print(f"{item['順位']}位: {item['記事タイトル']}")

        # Excel保存
        df = pd.DataFrame(data_list)
        df.to_excel(file_path, index=False)
        print(f"\n✅ 保存完了: {file_path}")
    else:
        print("\n❌ まだデータが見つかりません。サイトの構造が特殊なようです。")

except Exception as e:
    print(f"\nエラーが発生しました: {e}")