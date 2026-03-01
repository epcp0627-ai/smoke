import tweepy
import os
from datetime import datetime, timezone, timedelta

def send_tweet():
    # 환경 변수 로드
    auth_data = {
        "consumer_key": os.environ.get('TWITTER_API_KEY'),
        "consumer_secret": os.environ.get('TWITTER_API_SECRET'),
        "access_token": os.environ.get('TWITTER_ACCESS_TOKEN'),
        "access_token_secret": os.environ.get('TWITTER_ACCESS_SECRET')
    }

    client = tweepy.Client(**auth_data)

    # 날짜 계산 (2025-08-28 시작 기준)
    start_date = datetime(2025, 8, 28, tzinfo=timezone(timedelta(hours=9)))
    now_kst = datetime.now(timezone(timedelta(hours=9)))
    days_passed = (now_kst - start_date).days
    
    # 마지막 트윗 ID 읽기
    with open('last_tweet_id.txt', 'r') as f:
        last_id = f.read().strip()

    # 트윗 전송 및 ID 업데이트
    text = f"금연 {days_passed}일차."
    response = client.create_tweet(text=text, in_reply_to_tweet_id=last_id)
    
    with open('last_tweet_id.txt', 'w') as f:
        f.write(str(response.data['id']))
    
    print(f"성공: 금연{days_passed}일차")

if __name__ == "__main__":
    send_tweet()
