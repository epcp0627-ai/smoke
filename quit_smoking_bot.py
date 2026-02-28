import tweepy
import os
from datetime import datetime, timezone, timedelta
import sys # 종료 신호를 보내기 위해 추가

# 환경 변수 로드
API_KEY = os.environ.get('TWITTER_API_KEY')
API_SECRET = os.environ.get('TWITTER_API_SECRET')
ACCESS_TOKEN = os.environ.get('TWITTER_ACCESS_TOKEN')
ACCESS_SECRET = os.environ.get('TWITTER_ACCESS_SECRET')

def send_tweet():
    try:
        # Twitter API v2 인증
        client = tweepy.Client(
            consumer_key=API_KEY,
            consumer_secret=API_SECRET,
            access_token=ACCESS_TOKEN,
            access_token_secret=ACCESS_SECRET
        )

        # 시작 날짜 및 현재 날짜 계산 (KST 기준)
        start_date = datetime(2025, 8, 28, tzinfo=timezone(timedelta(hours=9)))
        now_kst = datetime.now(timezone(timedelta(hours=9)))
        days_passed = (now_kst - start_date).days
        
        # 마지막 트윗 ID 읽기
        with open('last_tweet_id.txt', 'r') as f:
            last_id = f.read().strip()

        # 트윗 내용 작성
        text = f"금연 {days_passed}일차."

        # 트윗 전송 (답글 형식)
        response = client.create_tweet(text=text, in_reply_to_tweet_id=last_id)
        new_id = response.data['id']

        # 성공 시 새로운 트윗 ID 저장
        with open('last_tweet_id.txt', 'w') as f:
            f.write(str(new_id))
        
        print(f"성공: {days_passed}일차 트윗 완료 (ID: {new_id})")

    except Exception as e:
        print(f"에러 발생: {e}")
        # 이 부분이 핵심입니다. 
        # 0이 아닌 숫자로 종료해야 GitHub Actions가 'Failure'로 인식합니다.
        sys.exit(1) 

if __name__ == "__main__":
    send_tweet()
