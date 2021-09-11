import requests
from isodate import parse_duration
from django.shortcuts import render
from django.conf import settings


def Index(request):

    # 動画検索url
    search_url = 'https://www.googleapis.com/youtube/v3/search'
    # 動画の詳細情報取得url
    video_url = 'https://www.googleapis.com/youtube/v3/videos'

    # 動画検索時のパラメーター
    # ユーザーの操作によって検索結果の並び順を変更
    if request.POST.get('submit') == 'relevance':
        search_params = {
            'part': 'snippet',
            'q': '筋トレ',
            'key': settings.YOUTUBE_DATA_API_KEY,
            'maxResults': 9,
            'type': 'video',
            'order': 'relevance'
        }
    elif request.POST.get('submit') == 'date':
        search_params = {
            'part': 'snippet',
            'q': '筋トレ',
            'key': settings.YOUTUBE_DATA_API_KEY,
            'maxResults': 9,
            'type': 'video',
            'order': 'date'
        }
    elif request.POST.get('submit') == 'viewCount':
        search_params = {
            'part': 'snippet',
            'q': '筋トレ',
            'key': settings.YOUTUBE_DATA_API_KEY,
            'maxResults': 9,
            'type': 'video',
            'order': 'viewCount'
        }
    else:
        search_params = {
            'part': 'snippet',
            'q': '筋トレ',
            'key': settings.YOUTUBE_DATA_API_KEY,
            'maxResults': 9,
            'type': 'video',
            'order': 'relevance'
        }

    # 動画idを格納する配列
    video_ids = []

    # 検索リクエスト
    r = requests.get(search_url, params=search_params)

    # 検索結果をjson形式で格納
    results = r.json()['items']

    # 検索結果からvideo_idを配列に格納
    for result in results:
        video_ids.append(result['id']['videoId'])

    # 動画情報取得時のパラメーター
    video_params = {
        'key': settings.YOUTUBE_DATA_API_KEY,
        'part': 'snippet,contentDetails',
        'id': video_ids,
        'maxResults': 9
    }

    # 動画情報取得リクエスト
    r = requests.get(video_url, params=video_params)

    # 取得した動画情報をjson形式で格納
    results = r.json()['items']

    # 必要な動画情報を格納する配列
    videos = []

    # 取得した動画情報から使用する情報のみvideo_dataにまとめ、動画一本分の情報をvideosに格納
    # これを取得した動画本数分繰り返す
    for result in results:
        video_data = {
            'title': result['snippet']['title'],
            'id': result['id'],
            'url': f'https://www.youtube.com/watch?v={result["id"]}',
            'duration': int(parse_duration(result['contentDetails']['duration']).total_seconds() // 60),
            'thumbnail': result['snippet']['thumbnails']['high']['url']
        }
        videos.append(video_data)

    # index.htmlに渡す形にデータを整形
    context = {
        'videos': videos
    }

    return render(request, 'myapp/index.html', context)



# 「このサイトについて」のページを表示
def About(request):
    return render(request, 'myapp/about.html')
