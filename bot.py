import os
import random
import time
import requests

from requests_oauthlib import OAuth1


# ============================================================
# X API 認証
# GitHub Actions の Secrets から読み込む
# ============================================================

API_KEY = os.environ["X_API_KEY"]
API_SECRET = os.environ["X_API_SECRET"]
ACCESS_TOKEN = os.environ["X_ACCESS_TOKEN"]
ACCESS_TOKEN_SECRET = os.environ["X_ACCESS_TOKEN_SECRET"]

LINK_URL = os.environ.get("LINK_URL", "")

auth = OAuth1(
    API_KEY,
    client_secret=API_SECRET,
    resource_owner_key=ACCESS_TOKEN,
    resource_owner_secret=ACCESS_TOKEN_SECRET,
)


# ============================================================
# 通常投稿
# ============================================================

posts = [
    "気になるもの置いてみた🌙よかったらプロフィールから見てね👇",
    "最近ハマってるものを少しまとめてみた🫶プロフィールから見られるよ👇",
    "暇なときに見る用にまとめてみた🌙プロフィールからどうぞ👇",
    "最近気になってるものをまとめてみた👀プロフィールから見てね👇",
    "夜に見るのにちょうどいいものまとめてみた🌙プロフィールから見てね👇",
    "ちょっと気になるものがあったのでまとめてみた👀プロフィールからどうぞ👇",
]


# ============================================================
# 夜の投稿
# ============================================================

link_posts = [
    "夜なのでちょっと気になるものをまとめてみた🌙",
    "この時間に見るとちょうどいいものをまとめてみた👀",
    "寝る前にちょっと見てみて🌙プロフィールからどうぞ👇",
    "最近気になってるものを夜用にまとめてみた🫶",
]


# ============================================================
# Xへ投稿
# ============================================================

def post_to_x(text):
    url = "https://api.x.com/2/tweets"

    response = requests.post(
        url,
        auth=auth,
        json={"text": text},
        timeout=30,
    )

    print("HTTP status:", response.status_code)

    if response.ok:
        print("投稿成功！")
        print(text)
        return True

    print("投稿失敗")
    print(response.text)
    return False


# ============================================================
# メイン処理
# ============================================================

def main():

    print("=" * 50)
    print("Riko X Bot 起動")
    print("=" * 50)

    # --------------------------------------------------------
    # GitHub Actions が毎時起動するので、
    # ここでは最初の55分待機はしない
    # --------------------------------------------------------

    print("ランダム待機を開始します。")

    wait_minutes = random.randint(3, 55)

    print(f"あと {wait_minutes} 分待ってから投稿します。")

    time.sleep(wait_minutes * 60)


    # --------------------------------------------------------
    # 待機後の時刻を確認
    # --------------------------------------------------------

    from datetime import datetime
    from zoneinfo import ZoneInfo

    now = datetime.now(ZoneInfo("Asia/Tokyo"))
    hour = now.hour

    print("=" * 50)
    print("実際の投稿判定時刻:", now.strftime("%Y-%m-%d %H:%M:%S"))
    print("=" * 50)


    # --------------------------------------------------------
    # 9:00〜20:59
    # 通常投稿
    # --------------------------------------------------------

    if 9 <= hour <= 20:

        text = random.choice(posts)

        print("通常投稿を選択しました。")

        post_to_x(text)

        return


    # --------------------------------------------------------
    # 21:00〜23:59
    # リンク誘導投稿
    # --------------------------------------------------------

    if 21 <= hour <= 23:

        text = random.choice(link_posts)

        if LINK_URL:
            text = text + "\n" + LINK_URL
        else:
            print("警告: LINK_URL が設定されていません。")

        print("夜の投稿を選択しました。")

        post_to_x(text)

        return


    # --------------------------------------------------------
    # 0:00〜8:59
    # 投稿しない
    # --------------------------------------------------------

    print("現在は投稿時間外です。")
    print("今回は投稿せず終了します。")


# ============================================================
# 起動
# ============================================================

if __name__ == "__main__":
    main()
