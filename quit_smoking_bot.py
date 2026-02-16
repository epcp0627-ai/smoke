import tweepy
from datetime import datetime, timedelta, timezone
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

    # 1. 마지막 트윗 ID 불러오기
    if os.path.exists(ID_FILE):
        with open(ID_FILE, "r") as f:
            parent_id = f.read().strip()
    else:
        parent_id = "2009090586499035210"

    # 2. 한국 시간(KST) 기준으로 오늘 날짜 가져오기
    kst = timezone(timedelta(hours=9))
    now_kst = datetime.now(kst)
    today = now_kst.date()
    
    # 3. 날짜 계산 (2025-08-22를 1일차로 설정)
    start = datetime.strptime(START_DATE, "%Y-%m-%d").date()
    days_passed = (today - start).days + 1

    # 4. 트윗 작성
    text = f"금연 {days_passed}일차"
    
    try:
        response = client.create_tweet(text=text, in_reply_to_tweet_id=parent_id)
        new_id = response.data['id']

        # 새 ID 저장
        with open(ID_FILE, "w") as f:
            f.write(str(new_id))
        print(f"성공: {today} 기준 {days_passed}일차 트윗 완료")
    except Exception as e:
        print(f"에러 발생: {e}")

if __name__ == "__main__":
    post_update()
