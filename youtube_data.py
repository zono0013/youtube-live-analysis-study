from googleapiclient.discovery import build
import pandas as pd
from datetime import datetime, timedelta
import time
import re


def create_youtube_client(api_key):
    return build('youtube', 'v3', developerKey=api_key)


def contains_japanese(text):
    """
    文字列に日本語（ひらがな・カタカナ）が含まれているかチェック
    """
    pattern = r'[ぁ-んァ-ン]'
    return bool(re.search(pattern, str(text)))


def get_date_ranges(days=3, interval=1):
    """
    指定された日数を小さな期間に分割して日付範囲のリストを生成
    """
    ranges = []
    end_date = datetime.utcnow()

    for i in range(0, days, interval):
        end = end_date - timedelta(days=i)
        start = end - timedelta(days=interval)
        ranges.append({
            'start': start.isoformat("T") + "Z",
            'end': end.isoformat("T") + "Z"
        })

    return ranges


def search_live_videos(youtube, date_range, page_token=None):
    """
    日本のライブ配信を検索
    """
    try:
        return youtube.search().list(
            part='snippet',
            type='video',
            eventType='completed',
            publishedAfter=date_range['start'],
            publishedBefore=date_range['end'],
            maxResults=50,
            pageToken=page_token,
            regionCode='JP',  # 日本の地域コードを指定
            relevanceLanguage='ja',  # 日本語のコンテンツを優先
            fields='items(id/videoId,snippet(title,channelTitle,publishedAt,description)),nextPageToken'
        ).execute()
    except Exception as e:
        print(f"検索エラー: {e}")
        time.sleep(60)
        return None


def get_video_details(youtube, video_ids):
    """
    動画の詳細情報を取得
    """
    try:
        return youtube.videos().list(
            part='liveStreamingDetails,statistics,snippet',
            id=','.join(video_ids),
            fields='items(id,statistics(viewCount),liveStreamingDetails(actualStartTime,actualEndTime,concurrentViewers),snippet(defaultLanguage,defaultAudioLanguage))'
        ).execute()
    except Exception as e:
        print(f"詳細取得エラー: {e}")
        time.sleep(10)
        return None


def collect_live_stream_data(api_key):
    youtube = create_youtube_client(api_key)
    date_ranges = get_date_ranges()
    all_videos = set()
    video_data = []

    for date_range in date_ranges:
        print(f"期間の検索中: {date_range['start']} から {date_range['end']}")
        page_token = None

        while True:
            search_response = search_live_videos(youtube, date_range, page_token)
            if not search_response:
                continue

            current_video_ids = []
            for item in search_response.get('items', []):
                video_id = item['id']['videoId']
                if video_id not in all_videos:
                    all_videos.add(video_id)
                    current_video_ids.append(video_id)
                    video_data.append({
                        'video_id': video_id,
                        'title': item['snippet']['title'],
                        'channel_name': item['snippet']['channelTitle'],
                        'published_at': item['snippet']['publishedAt'],
                        'description': item['snippet']['description']
                    })

            if current_video_ids:
                details_response = get_video_details(youtube, current_video_ids)
                if details_response:
                    for item in details_response.get('items', []):
                        video_id = item['id']
                        live_details = item.get('liveStreamingDetails', {})
                        stats = item.get('statistics', {})

                        for video in video_data:
                            if video['video_id'] == video_id:
                                video.update({
                                    'start_time': live_details.get('actualStartTime'),
                                    'end_time': live_details.get('actualEndTime'),
                                    'view_count': int(stats.get('viewCount', 0))
                                })

            time.sleep(1)

            page_token = search_response.get('nextPageToken')
            if not page_token:
                print("paging ok")
                break

    # データフレームの作成
    df = pd.DataFrame([v for v in video_data if v.get('view_count', 0) > 0])

    # 日本語コンテンツのフィルタリング
    japanese_streams = df[df['title'].apply(contains_japanese) | df['channel_name'].apply(contains_japanese)]

    # 日時データを日本時間に変換
    for col in ['published_at', 'start_time', 'end_time']:
        if col in japanese_streams.columns:
            japanese_streams[col] = pd.to_datetime(japanese_streams[col]).dt.tz_convert('Asia/Tokyo')

    # 配信時間を計算
    japanese_streams['duration_minutes'] = (pd.to_datetime(japanese_streams['end_time']) -
                                            pd.to_datetime(japanese_streams['start_time'])).dt.total_seconds() / 60

    # CSVに保存
    japanese_streams.to_csv('japanese_live_streams_filtered.csv', index=False)
    print(f"収集完了: {len(japanese_streams)} 件の日本のライブ配信を保存しました")

    # 統計情報を表示
    print("\n視聴回数の統計:")
    print(f"平均視聴回数: {japanese_streams['view_count'].mean():.2f}")
    print(f"最大視聴回数: {japanese_streams['view_count'].max()}")
    print(f"最小視聴回数: {japanese_streams['view_count'].min()}")

    if 'duration_minutes' in japanese_streams.columns:
        print("\n配信時間の統計（分）:")
        print(f"平均配信時間: {japanese_streams['duration_minutes'].mean():.2f}")
        print(f"最長配信時間: {japanese_streams['duration_minutes'].max():.2f}")
        print(f"最短配信時間: {japanese_streams['duration_minutes'].min():.2f}")

    return japanese_streams


# APIキーを設定して実行
API_KEY = 'YOUR_API_KEY'  # 自分のAPIキーを入力
df = collect_live_stream_data(API_KEY)