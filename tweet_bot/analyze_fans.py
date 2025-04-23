import os
import pandas as pd
import tweepy
from collections import defaultdict
from datetime import datetime, timedelta

# 環境変数からTwitter認証情報と対象ユーザー名を取得
BEARER_TOKEN = os.getenv("TW_BEARER_TOKEN")
USERNAME = os.getenv("TW_USERNAME")

client = tweepy.Client(bearer_token=BEARER_TOKEN, wait_on_rate_limit=True)

# 対象ユーザーのIDを取得
user = client.get_user(username=USERNAME).data
user_id = user.id

# 過去7日間のツイートを取得
now = datetime.utcnow()
start_time = now - timedelta(days=7)

tweets = client.get_users_tweets(
    id=user_id,
    start_time=start_time.isoformat("T") + "Z",
    max_results=100,
    tweet_fields=["id", "created_at"]
).data or []

# 各ツイートに対するリアクションを集計
weights = {"reply": 3, "retweet": 2, "like": 1}
score = defaultdict(lambda: {"reply": 0, "retweet": 0, "like": 0})

for tweet in tweets:
    tweet_id = tweet.id

    # リプライ（v2には明確なリプ取得APIがないため省略 or v1.1要）
    # 代替案として reply だけ仮に0で

    # リツイートしたユーザー
    try:
        rt_users = client.get_retweeters(tweet_id).data or []
        for user in rt_users:
            score[user.username]["retweet"] += 1
    except Exception:
        pass

    # いいねしたユーザー
    try:
        like_users = client.get_liking_users(tweet_id).data or []
        for user in like_users:
            score[user.username]["like"] += 1
    except Exception:
        pass

# スコア集計・出力
records = []
for username, counts in score.items():
    total = sum(counts[k] * weights[k] for k in counts)
    records.append({
        "ユーザー": username,
        "リプ数": counts["reply"],
        "RT数": counts["retweet"],
        "いいね数": counts["like"],
        "スコア": total
    })

df_week = pd.DataFrame(records).sort_values(by="スコア", ascending=False)
df_week.to_csv("weekly_fan_score.csv", index=False)

# 累計の更新
if os.path.exists("total_fan_score.csv"):
    df_total = pd.read_csv("total_fan_score.csv")
    df_total.set_index("ユーザー", inplace=True)
else:
    df_total = pd.DataFrame(columns=["ユーザー", "リプ数", "RT数", "いいね数", "スコア"])
    df_total.set_index("ユーザー", inplace=True)

for row in records:
    user = row["ユーザー"]
    if user not in df_total.index:
        df_total.loc[user] = [0, 0, 0, 0]
    df_total.loc[user, "リプ数"] += row["リプ数"]
    df_total.loc[user, "RT数"] += row["RT数"]
    df_total.loc[user, "いいね数"] += row["いいね数"]
    df_total.loc[user, "スコア"] += row["スコア"]

df_total = df_total.reset_index().sort_values(by="スコア", ascending=False)
df_total.to_csv("total_fan_score.csv", index=False)