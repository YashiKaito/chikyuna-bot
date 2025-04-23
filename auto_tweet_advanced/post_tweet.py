import tweepy
import openai
import os

# APIキーの読み込み
consumer_key = os.getenv("TWITTER_API_KEY")
consumer_secret = os.getenv("TWITTER_API_SECRET")
access_token = os.getenv("ACCESS_TOKEN")
access_token_secret = os.getenv("ACCESS_SECRET")
openai.api_key = os.getenv("OPENAI_API_KEY")

# セリフ生成（キャラクターの精度を高めるプロンプト）
def generate_tweet():
    prompt = (
        "あなたは知的でユーモラスな歴史案内人キャラ『チキューナ』です。"
        "毎日、世界遺産や歴史の雑学を、ちょっとズレた発言も交えつつ楽しく紹介します。"
        "フォロワーが思わず『何それ！？』と反応したくなるような、"
        "好奇心をくすぐる内容を140文字以内で1つ作成してください。"
        "キャラクター性を守ってください。"
    )
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.95,
            max_tokens=100
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print("OpenAIエラー:", e)
        return "チキューナです！今日は調子がGPTじゃないかも！？💦"

# 投稿処理
def post_tweet(message):
    auth = tweepy.OAuth1UserHandler(consumer_key, consumer_secret, access_token, access_token_secret)
    api = tweepy.API(auth)
    try:
        api.update_status(message)
        print("✅ 投稿完了:", message)
    except Exception as e:
        print("❌ Twitter投稿エラー:", e)

if __name__ == "__main__":
    message = generate_tweet()
    post_tweet(message)
