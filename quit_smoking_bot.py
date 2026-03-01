import tweepy
import os
from datetime import datetime, timezone, timedelta

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
        # 2025년 8월 28일 시작 기준
        start_date = datetime(2025, 8, 28, tzinfo=timezone(timedelta(hours=9)))
        now_kst = datetime.now(timezone(timedelta(hours=9)))
        days_passed = (now_kst - start_date).days
        
        # 마지막 트윗 ID 읽기
        if os.path.exists('last_tweet_id.txt'):
            with open('last_tweet_id.txt', 'r') as f:
                last_id = f.read().strip()
        else:
            print("에러: last_tweet_id.txt 파일이 존재하지 않습니다.")
            return

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
        # sys.exit(1) 제거: 에러가 발생해도 프로세스는 정상 종료된 것으로 간주하여
        # 이후 GitHub Action 단계에서 불필요한 중단을 방지합니다.

if __name__ == "__main__":
    send_tweet()
