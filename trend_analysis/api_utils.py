import requests
from googleapiclient.discovery import build
from django.conf import settings
from pytrends.request import TrendReq

def get_youtube_channel_data(channel_url):
    # Extract the channel ID from the URL
    channel_id = extract_channel_id(channel_url)
    
    youtube = build('youtube', 'v3', developerKey=settings.YOUTUBE_API_KEY)
    
    channel_response = youtube.channels().list(
        part='snippet,statistics',
        id=channel_id
    ).execute()

    if 'items' in channel_response:
        channel_data = channel_response['items'][0]
        return {
            'title': channel_data['snippet']['title'],
            'description': channel_data['snippet']['description'],
            'thumbnail': channel_data['snippet']['thumbnails']['default']['url'],
            'subscriber_count': int(channel_data['statistics']['subscriberCount']),
            'view_count': int(channel_data['statistics']['viewCount']),
            'video_count': int(channel_data['statistics']['videoCount']),
        }
    return None

def extract_channel_id(channel_url):
    # Implement logic to extract channel ID from the URL
    # This is a placeholder implementation
    if 'channel/' in channel_url:
        return channel_url.split('channel/')[1]
    elif 'user/' in channel_url:
        # Additional logic to handle user URLs
        pass
    return None

def get_google_trends_data(keyword, geo='US'):
    pytrends = TrendReq(hl='en-US', tz=360)
    pytrends.build_payload([keyword], timeframe='today 12-m', geo=geo)
    
    interest_over_time = pytrends.interest_over_time()
    related_queries = pytrends.related_queries()
    
    return {
        'interest_over_time': interest_over_time.to_dict()[keyword] if not interest_over_time.empty else {},
        'related_queries': related_queries[keyword] if keyword in related_queries else {}
    }

def get_video_performance(channel_id):
    youtube = build('youtube', 'v3', developerKey=settings.YOUTUBE_API_KEY)
    
    videos_response = youtube.search().list(
        part='id',
        channelId=channel_id,
        type='video',
        order='date',
        maxResults=10
    ).execute()

    video_ids = [item['id']['videoId'] for item in videos_response.get('items', [])]
    
    videos_data = youtube.videos().list(
        part='snippet,statistics',
        id=','.join(video_ids)
    ).execute()

    return [
        {
            'title': video['snippet']['title'],
            'views': int(video['statistics']['viewCount']),
            'likes': int(video['statistics']['likeCount']),
            'comments': int(video['statistics']['commentCount'])
        }
        for video in videos_data.get('items', [])
    ]
