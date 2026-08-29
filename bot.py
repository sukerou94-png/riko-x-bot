from dotenv import load_dotenv
import os
import time
import random
import json
from datetime import datetime, timedelta
import requests
from requests_oauthlib import OAuth1

# =========================
# 設定
# =========================

load_dotenv("/Users/tomato/riko-x-bot/.env")

auth = OAuth1(
    os.environ["X_API_KEY"],
    os.environ["X_API_SECRET"],
    os.environ["X_ACCESS_TOKEN"],
    os.environ["X_ACCESS_TOKEN_SECRET"]
)

# 夜に載せたいリンク
# ↓↓↓ 自分のリンクに変更する ↓↓↓
LINK_URL = "https://lit.link/riko_night"

# 通常投稿をする時間帯
NORMAL_START = 9
NORMAL_END = 20

# 夜のリンク投稿時間帯
LINK_START = 21
LINK_END = 23

# 1日の通常投稿回数
NORMAL_POSTS_PER_DAY = 5

# 投稿履歴ファイル
HISTORY_FILE = "/Users/tomato/riko-x-bot/history.json"


# =========================
# 通常投稿
# =========================

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
    "今日はちょっと寄り道してみる☕️",
    "こういう何でもない時間って好き☺️",
    "明日は何しようかな",
    "最近お気に入りの場所ができた🌿",
    "今日は早めに帰ってゆっくりしたい",
    "夜に散歩するのも意外といいかも🌙",
    "最近また映画見たい気分🎬",
    "好きなものの話するの楽しい☺️",
    "今日は気分転換したい日✨",
    "コンビニ寄って帰ろうかな🥤",
    "最近ちょっと忙しかったから休憩中☕️",
    "こういう時間に聴く音楽っていいよね🎧",
    "今日は何食べようかな🍜",
    "休日はゆっくりする派です😌",
    "最近写真撮るのちょっと楽しい📷",
    "夜ってなんか落ち着く🌙",
    "今日は気ままに過ごしてる",
    "新しいこと始めてみたいな✨",
    "おすすめあったら教えてね☺️",
    "最近ちょっと散歩するのにハマってる🚶‍♀️",
    "今日は好きな曲をずっと聴いてる🎧",
    "帰ったらゆっくり映画でも見ようかな🎬",
    "今日はちょっとだけ自分甘やかす日🍰",
    "最近お気に入りが増えてきた✨",
    "なんとなく今日は夜更かししたい気分🌙",
    "明日の予定どうしようかな",
    "今日はのんびりモード😴",
    "好きなものに囲まれてる時間が一番落ち着く☺️",
]


# =========================
# 夜のリンク投稿
# =========================

link_posts = [
    "今日気になってたもの、まとめてみた🌙\nプロフィールから見られるよ👇",
    "夜にゆっくり見たいものをまとめてみた☺️\n気になる人はプロフィールから👇",
    "ちょっと気になったものを置いておくね🌙\nプロフィールからどうぞ👇",
    "今日はこれをチェックしてた✨\n気になる人はプロフィールへ👇",
    "寝る前にちょっと見てみるのもいいかも🌙\nプロフィールに置いてあるよ👇",
    "最近気になってるものをまとめました☺️\n詳しくはプロフィールから👇",
    "夜の暇つぶしにどうぞ🌙\nプロフィールから見られます👇",
    "気になるものがあったらここから見てみてね✨\n👇",
]


# =========================
# 履歴
# =========================

def load_history():
    if not os.path.exists(HISTORY_FILE):
        return {
            "used_posts": [],
            "last_post": "",
            "last_link_date": ""
        }

    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {
            "used_posts": [],
            "last_post": "",
            "last_link_date": ""
        }


def save_history(history):
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)


# =========================
# 投稿
# =========================

def post_to_x(text):
    r = requests.post(
        "https://api.x.com/2/tweets",
        auth=auth,
        json={"text": text}
    )

    print("HTTP:", r.status_code)
    print(r.text)

    if r.status_code == 201:
        print("投稿成功！")
        return True

    print("投稿失敗")
    return False


# =========================
# 通常投稿を選ぶ
# =========================

def choose_normal_post(history):

    available = [
        p for p in posts
        if p != history["last_post"]
    ]

    # 全部使ったら履歴をリセット
    if not available:
        history["used_posts"] = []
        available = [
            p for p in posts
            if p != history["last_post"]
        ]

    text = random.choice(available)

    return text


# =========================
# リンク投稿
# =========================

def choose_link_post():

    text = random.choice(link_posts)

    # URLを最後に追加
    text += "\n" + LINK_URL

    return text


# =========================
# 今日のリンク投稿済み確認
# =========================

def link_posted_today(history):

    today = datetime.now().strftime("%Y-%m-%d")

    return history.get("last_link_date") == today


# =========================
# ランダム時刻
# =========================

def random_time_between(start_hour, end_hour):

    now = datetime.now()

    start = now.replace(
        hour=start_hour,
        minute=0,
        second=0,
        microsecond=0
    )

    end = now.replace(
        hour=end_hour,
        minute=59,
        second=59,
        microsecond=0
    )

    if end <= start:
        end += timedelta(days=1)

    seconds = random.randint(
        0,
        int((end - start).total_seconds())
    )

    return start + timedelta(seconds=seconds)


# =========================
# メイン
# =========================

history = load_history()

print("================================")
print("Riko X Bot 起動")
print("================================")

print("通常投稿時間:", NORMAL_START, "〜", NORMAL_END)
print("夜リンク投稿:", LINK_START, "〜", LINK_END)
print("通常投稿数:", NORMAL_POSTS_PER_DAY)
print()


# =========================
# 今日の通常投稿予定を作る
# =========================

today = datetime.now()

normal_times = []

for i in range(NORMAL_POSTS_PER_DAY):

    hour = random.randint(
        NORMAL_START,
        NORMAL_END - 1
    )

    minute = random.randint(0, 59)

    post_time = today.replace(
        hour=hour,
        minute=minute,
        second=random.randint(0, 59),
        microsecond=0
    )

    normal_times.append(post_time)


# 時刻順にする
normal_times.sort()

print("今日の通常投稿予定:")

for t in normal_times:
    print(" -", t.strftime("%H:%M:%S"))

print()


# =========================
# 夜リンク投稿予定
# =========================

if not link_posted_today(history):

    link_time = random_time_between(
        LINK_START,
        LINK_END
    )

    print(
        "夜のリンク投稿予定:",
        link_time.strftime("%H:%M:%S")
    )

else:

    link_time = None
    print("今日はリンク投稿済みです")


print()
print("Botは待機中...")
print()


# =========================
# 投稿ループ
# =========================

posted_normal = []

while True:

    now = datetime.now()

    # -------------------------
    # 通常投稿
    # -------------------------

    for post_time in normal_times:

        if post_time in posted_normal:
            continue

        if now >= post_time:

            text = choose_normal_post(history)

            print()
            print("通常投稿:")
            print(text)

            success = post_to_x(text)

            if success:

                history["last_post"] = text
                history["used_posts"].append(text)

                # 履歴が増えすぎないようにする
                history["used_posts"] = history["used_posts"][-100:]

                save_history(history)

                posted_normal.append(post_time)

                print("次の通常投稿を待ちます")


    # -------------------------
    # 夜リンク投稿
    # -------------------------

    if link_time is not None:

        if now >= link_time:

            today_string = datetime.now().strftime(
                "%Y-%m-%d"
            )

            if history.get("last_link_date") != today_string:

                text = choose_link_post()

                print()
                print("🌙 夜のリンク投稿:")
                print(text)

                success = post_to_x(text)

                if success:

                    history["last_link_date"] = today_string

                    history["last_post"] = text

                    save_history(history)

                    print("夜のリンク投稿完了！")

                link_time = None


    # -------------------------
    # 10秒ごとに確認
    # -------------------------

    time.sleep(10)
