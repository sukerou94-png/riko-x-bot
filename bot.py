from dotenv import load_dotenv
import os
import random
from datetime import datetime
import requests
from requests_oauthlib import OAuth1

load_dotenv("/Users/tomato/riko-x-bot/.env")

auth = OAuth1(
    os.environ["X_API_KEY"],
    os.environ["X_API_SECRET"],
    os.environ["X_ACCESS_TOKEN"],
    os.environ["X_ACCESS_TOKEN_SECRET"]
)

LINK_URL = "https://lit.link/riko_night"

posts = [
    "今日はちょっとゆっくり過ごしたい🌙",
    "最近ハマってることが増えてきた☺️",
    "今日は寄り道して帰ろうかな☕️",
    "おすすめの音楽あったら教えてほしい🎧",
    "今日はちょっと眠い日😴",
    "天気いいと散歩したくなる🌿",
    "帰りに何か甘いもの買おうかな🍰",
    "最近夜の時間が好きかも🌙",
    "今日はのんびりする日にする✨",
    "新しい服ほしいな〜👗",
    "最近よく聴く曲が頭から離れない🎧",
    "こういう何でもない時間って好き☺️",
    "夜ってなんか落ち着く🌙",
    "今日は気分転換したい日✨",
    "今日は何食べようかな🍜",
    "最近写真撮るのちょっと楽しい📷",
    "今日は気ままに過ごしてる",
    "新しいこと始めてみたいな✨",
    "おすすめあったら教えてね☺️",
    "好きなものに囲まれてる時間が一番落ち着く☺️",
]

link_posts = [
    "今日気になってたもの、まとめてみた🌙\nプロフィールから見られるよ👇",
    "夜にゆっくり見たいものをまとめてみた☺️\nプロフィールから👇",
    "ちょっと気になったものを置いておくね🌙\nプロフィールからどうぞ👇",
    "今日はこれをチェックしてた✨\n気になる人はプロフィールへ👇",
    "寝る前にちょっと見てみるのもいいかも🌙\nプロフィールに置いてあるよ👇",
    "最近気になってるものをまとめました☺️\n詳しくはプロフィールから👇",
    "夜の暇つぶしにどうぞ🌙\nプロフィールから見られます👇",
]

def post_to_x(text):
    r = requests.post(
        "https://api.x.com/2/tweets",
        auth=auth,
        json={"text": text}
    )

    print("HTTP:", r.status_code)
    print(r.text)

    return r.status_code == 201


def main():
    now = datetime.now()

    print("Riko X Bot")
    print("日本時間:", now.strftime("%Y-%m-%d %H:%M:%S"))

    hour = now.hour

    # 9:00〜20:59 → 通常投稿
    if 9 <= hour < 21:
        text = random.choice(posts)

        print("通常投稿:")
        print(text)

        if post_to_x(text):
            print("投稿成功！")
        else:
            print("投稿失敗")

    # 21:00〜23:59 → リンク投稿
    elif 21 <= hour < 24:
        text = random.choice(link_posts)
        text += "\n" + LINK_URL

        print("🌙 夜のリンク投稿:")
        print(text)

        if post_to_x(text):
            print("リンク投稿成功！")
        else:
            print("リンク投稿失敗")

    else:
        print("現在は投稿時間外です。")
        print("今回は投稿せず終了します。")


if __name__ == "__main__":
    main()
