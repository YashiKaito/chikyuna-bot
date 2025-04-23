import tweepy
import os

# Twitter APIキーを環境変数から取得
consumer_key = os.getenv("TWITTER_API_KEY")
consumer_secret = os.getenv("TWITTER_API_SECRET")
access_token = os.getenv("ACCESS_TOKEN")
access_token_secret = os.getenv("ACCESS_SECRET")

# 認証
auth = tweepy.OAuth1UserHandler(consumer_key, consumer_secret, access_token, access_token_secret)
api = tweepy.API(auth)

# 固定メッセージで投稿（GPTなし）
message = "チキューナだよ〜！今日は世界遺産を紹介……しないで昼寝したいかも〜💤"

# 投稿
try:
    api.update_status(message)
    print("✅ ツイート完了！")
except Exception as e:
    print("❌ エラーが発生しました：", e)
