import tweepy
import os
from datetime import datetime, timezone, timedelta

def send_tweet():
    auth_data = {
        "consumer_key": os.environ.get('TWITTER_API_KEY'),
        "consumer_secret": os.environ.get('TWITTER_API_SECRET'),
        "access_token": os.environ.get('TWITTER_ACCESS_TOKEN'),
        "access_token_secret": os.environ.get('TWITTER_ACCESS_SECRET')
    }

    client = tweepy.Client(**auth_data)

    # 2026-03-01 기준 192일차가 되려면 시작일은 2025-08-21입니다.
    start_date = datetime(2025, 8, 21, tzinfo=timezone(timedelta(hours=9)))
    now_kst = datetime.now(timezone(timedelta(hours=9)))
    days_passed = (now_kst - start_date).days
    
    # 마지막 트윗 ID 읽기
    with open('last_tweet_id.txt', 'r') as f:
        last_id = f.read().strip()

    # 트윗 전송
    text = f"금연 {days_passed}일차"
    response = client.create_tweet(text=text, in_reply_to_tweet_id=last_id)
    
    # 성공 시 새로운 트윗 ID 저장
    with open('last_tweet_id.txt', 'w') as f:
        f.write(str(response.data['id']))
    
    print(f"성공: {days_passed}일차 트윗 완료")

if __name__ == "__main__":
    send_tweet()
