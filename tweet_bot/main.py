
from generate_text import generate_tweet
from tweet import post_to_twitter

def main():
    tweet = generate_tweet()
    print(f"Generated Tweet:\n{tweet}\n")
    post_to_twitter(tweet)

if __name__ == "__main__":
    main()
