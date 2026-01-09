import tweepy
from datetime import datetime
import os

# API 키 설정
API_KEY = os.environ["TWITTER_API_KEY"]
API_SECRET = os.environ["TWITTER_API_SECRET"]
ACCESS_TOKEN = os.environ["TWITTER_ACCESS_TOKEN"]
ACCESS_SECRET = os.environ["TWITTER_ACCESS_SECRET"]

START_DATE = "2025-08-22"
ID_FILE = "last_tweet_id.txt"

def post_update():
    client = tweepy.Client(
        consumer_key=API_KEY, consumer_secret=API_SECRET,
        access_token=ACCESS_TOKEN, access_token_secret=ACCESS_SECRET
    )

    # 마지막 트윗 ID 불러오기
    if os.path.exists(ID_FILE):
        with open(ID_FILE, "r") as f:
            parent_id = f.read().strip()
    else:
        parent_id = "2009090586499035210"

    # 날짜 계산
    start = datetime.strptime(START_DATE, "%Y-%m-%d")
    days_passed = (datetime.now() - start).days + 1

    # 트윗 작성
    text = f"금연 {days_passed}일차"
    response = client.create_tweet(text=text, in_reply_to_tweet_id=parent_id)
    
    new_id = response.data['id']

    # 새 ID 저장
    with open(ID_FILE, "w") as f:
        f.write(str(new_id))

if __name__ == "__main__":
    post_update()
