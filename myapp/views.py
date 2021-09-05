import requests
from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.views.generic import TemplateView

# Create your views here.


def Index(request):
    search_url = 'https://www.googleapis.com/youtube/v3/search'
    params = {
        'part': 'snippet',
        'q': 'learn python',
        'key': settings.YOUTUBE_DATA_API_KEY,
        'maxResults': 9,
        'type':'video'
    }

    video_ids = []
    r = requests.get(search_url, params=params)
    results = r.json()['items']
    for result in results:
        print(result['id']['videoId'])

    return render(request, 'myapp/index.html')
