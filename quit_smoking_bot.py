import tweepy
import os
from datetime import datetime, timezone, timedelta

def send_tweet():
    # 환경 변수 로드 및 인증 설정
    # Client 생성 시 bearer_token을 포함하는 것이 안정적입니다.
    client = tweepy.Client(
        consumer_key=os.environ.get('TWITTER_API_KEY'),
        consumer_secret=os.environ.get('TWITTER_API_SECRET'),
        access_token=os.environ.get('TWITTER_ACCESS_TOKEN'),
        access_token_secret=os.environ.get('TWITTER_ACCESS_SECRET')
    )

    # 날짜 계산
    start_date = datetime(2025, 8, 21, tzinfo=timezone(timedelta(hours=9)))
    now_kst = datetime.now(timezone(timedelta(hours=9)))
    days_passed = (now_kst - start_date).days
    
    # 마지막 트윗 ID 읽기 (파일이 없거나 비어있는 경우 예외 처리)
    last_id = None
    if os.path.exists('last_tweet_id.txt'):
        with open('last_tweet_id.txt', 'r') as f:
            content = f.read().strip()
            if content:
                last_id = content

    text = f"금연 {days_passed}일차"

    try:
        # 트윗 전송
        # last_id가 있을 때만 타래(reply)로 작성, 없으면 단독 트윗
        if last_id:
            response = client.create_tweet(text=text, in_reply_to_tweet_id=last_id)
        else:
            response = client.create_tweet(text=text)
        
        # 성공 시 새로운 트윗 ID 저장
        new_id = response.data['id']
        with open('last_tweet_id.txt', 'w') as f:
            f.write(str(new_id))
        
        print(f"성공: {days_passed}일차 트윗 완료 (ID: {new_id})")

    except tweepy.errors.Forbidden as e:
        print(f"권한 에러(403): API 설정에서 'Read and Write' 권한과 'Access Token' 재발급 여부를 확인하세요.\n상세: {e}")
    except Exception as e:
        print(f"기타 에러 발생: {e}")

if __name__ == "__main__":
    send_tweet()
