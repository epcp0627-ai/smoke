import tweepy
import os
import sys # 추가
from datetime import datetime, timezone, timedelta

# 환경 변수 로드
API_KEY = os.environ.get('TWITTER_API_KEY')
API_SECRET = os.environ.get('TWITTER_API_SECRET')
ACCESS_TOKEN = os.environ.get('TWITTER_ACCESS_TOKEN')
ACCESS_SECRET = os.environ.get('TWITTER_ACCESS_SECRET')

def send_tweet():
    try:
        client = tweepy.Client(
            consumer_key=API_KEY,
            consumer_secret=API_SECRET,
            access_token=ACCESS_TOKEN,
            access_token_secret=ACCESS_SECRET
        )

        start_date = datetime(2025, 8, 28, tzinfo=timezone(timedelta(hours=9)))
        now_kst = datetime.now(timezone(timedelta(hours=9)))
        days_passed = (now_kst - start_date).days
        
        with open('last_tweet_id.txt', 'r') as f:
            last_id = f.read().strip()

        text = f"금연 {days_passed}일차"
        response = client.create_tweet(text=text, in_reply_to_tweet_id=last_id)
        
        with open('last_tweet_id.txt', 'w') as f:
            f.write(str(response.data['id']))
        
        print(f"성공: {days_passed}일차")

    except Exception as e:
        print(f"에러 발생: {e}")
        sys.exit(1) # 이 코드가 있어야 디스코드 알림이 발송됩니다.

if __name__ == "__main__":
    send_tweet()
