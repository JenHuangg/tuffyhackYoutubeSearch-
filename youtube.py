
import urllib.parse
import urllib.request
import json


YOUTUBE_HTTP_REQUEST = "https://www.googleapis.com/youtube/v3"
API_KEY = #API KEY


class Search:
    def __init__(self, to_search):
        url = _create_search_url(to_search)
        self._search = _get_result(url)
        videos_url = _get_videos(self._search)
        self._videos = _get_result(videos_url)

    def get_video_title(self, vid_num: int) -> str:
        title = self._make_snippet_func('title')
        return title(vid_num)

    def get_description(self, vid_num: int) -> str:
        description = self._make_snippet_func('description')
        return description(vid_num)
    
    def get_published_date(self, vid_num: int) -> str:
        date = self._make_snippet_func('publishedAt')
        date_published = date(vid_num)
        formatted_date = date_published[:10] + ' ' + date_published[11:-1]
        return formatted_date
    
    def get_channel_title(self, vid_num:int) -> str:
        title = self._make_snippet_func('channelTitle')
        return title(vid_num)

    def get_view_count(self, vid_num:int) -> str:
        views = self._make_video_stats_func('viewCount')
        formatted_views = '{:,}'.format(int(views(vid_num)))
        return formatted_views

    def get_liked_count(self, vid_num: int) -> str:
        liked = self._make_video_stats_func('likeCount')
        return liked(vid_num)

    def get_disliked_count(self, vid_num: int) -> str:
        disliked = self._make_video_stats_func('dislikeCount')
        return disliked(vid_num)

    def get_duration(self, vid_num: int) -> str:
        duration = self._make_general_func('contentDetails')
        length = duration('duration', vid_num)
        time = length[2:-1]
        formatted_duration = time.replace('M', ':')
        return formatted_duration
        
    

    def _make_snippet_func(self, need:str) -> 'function(int) -> str':
        def get_this(vid_num: int):
            to_get = self._search['items'][vid_num - 1]['snippet'][need]
            return to_get

        return get_this
        
    def _make_video_stats_func(self, need: str) -> 'function(int) -> str':
        def get_this(vid_num: int):
            to_get = self._videos['items'][vid_num - 1]['statistics'][need]
            return to_get

        return get_this

    def _make_general_func(self, need: str) -> "function(int) -> str":
        def get_this(sub_category: str, vid_num: int):
            to_get = self._videos['items'][vid_num - 1][need][sub_category]
            return to_get

        return get_this



def _create_search_url(to_search) -> str:

    search_parameters = [
        ('key', API_KEY), ('type', 'video'),
        ('order', 'viewCount'), ('part', 'snippet'),
        ('maxResults', 10),
        ('q', to_search)
        ]

    return YOUTUBE_HTTP_REQUEST + '/search?' + urllib.parse.urlencode(search_parameters)

def _get_result(url: str) -> dict:
    response = None

    try:
        request = urllib.request.Request(url)
        response = urllib.request.urlopen(request)
        json_text = response.read().decode(encoding = 'utf-8')

        return json.loads(json_text)

    finally:
        if response != None:
            response.close()

def _get_videos(result: dict) -> dict:
    video_ids = ''
    for item in result['items']:
        video_ids = video_ids + ',' + item['id']['videoId']

    
    search_parameters = [
        ('key', API_KEY),
        ('part', 'snippet, statistics,id, contentDetails'),
        ('id', video_ids[1:])]

    url = YOUTUBE_HTTP_REQUEST + '/videos?' + urllib.parse.urlencode(search_parameters)
    
    return url
    
        

def _print_information(result: dict) -> None:

    for item in result['items']:
        print(item['snippet']['title'])
        print(item['snippet']['thumbnails'])
        print()

            

if __name__ == '__main__':
 pass
    
