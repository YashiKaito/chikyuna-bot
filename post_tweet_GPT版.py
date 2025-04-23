import tweepy
import openai
import os

# 環境変数からAPIキーを取得
consumer_key = os.getenv("TWITTER_API_KEY")
consumer_secret = os.getenv("TWITTER_API_SECRET")
access_token = os.getenv("ACCESS_TOKEN")
access_token_secret = os.getenv("ACCESS_SECRET")
openai.api_key = os.getenv("OPENAI_API_KEY")

# セリフ生成（GPT）
def generate_tweet():
    prompt = (
        "キャラクター「チキューナ」は、好奇心旺盛でボケの多い案内人です。"
        "彼女が世界遺産や歴史の話題に関して、元気でちょっとおかしなツイートを"
        "140文字以内で1つ、キャラクターになりきってつぶやいてください。"
    )
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.9,
            max_tokens=100
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        print("OpenAIエラー:", e)
        return "チキューナだよ〜！今日はちょっと調子がGPTじゃないかも！？💦"

# Twitter認証
auth = tweepy.OAuth1UserHandler(consumer_key, consumer_secret, access_token, access_token_secret)
api = tweepy.API(auth)

# 投稿処理
message = generate_tweet()

try:
    api.update_status(message)
    print("✅ GPTセリフ投稿完了:", message)
except Exception as e:
    print("❌ Twitter投稿エラー:", e)
