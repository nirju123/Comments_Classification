import googleapiclient.discovery
import re
import requests
from save_files import save_as_csv, save_as_txt

def get_video_id_from_url(video_url):
    # Regular expression pattern to match the video ID in a video URL
    pattern = r"(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/watch\?v=|youtu\.be\/)([a-zA-Z0-9_-]{11})"

    # Search for the video ID in the URL using the pattern
    match = re.search(pattern, video_url)

    # If a match is found, return the video ID
    if match:
        return match.group(1)
    else:
        return None


def get_channel_id_from_video_id(api_key, video_id):
    youtube = googleapiclient.discovery.build('youtube', 'v3', developerKey=api_key)

    # Request to get the video details
    request = youtube.videos().list(
        part='snippet',
        id=video_id
    )
    response = request.execute()

    if 'items' in response and len(response['items']) > 0:
        # Return the channel ID from the video details
        return response['items'][0]['snippet']['channelId']
    else:
        return None


def get_channel_id_from_url(video_url):
    print("run")
    api_key = 'AIzaSyA4977yDihHfx75VfgCE09v_NeSVVCiRMM'
    video_id = get_video_id_from_url(video_url)
    channel_id = get_channel_id_from_video_id(api_key,video_id)
    print(video_id,channel_id)
    return  channel_id


def get_youtube_video_info(video_id):
    api_key = 'AIzaSyA4977yDihHfx75VfgCE09v_NeSVVCiRMM'
    url = f"https://www.googleapis.com/youtube/v3/videos?id={video_id}&key={api_key}&part=snippet"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        video_info = {
            'title': data['items'][0]['snippet']['title'],
            'channel_name': data['items'][0]['snippet']['channelTitle'],
            # Add more fields as needed
        }
        return video_info
    else:
        return None


def get_live_streams(api_key, channel_id):
    youtube = googleapiclient.discovery.build('youtube', 'v3', developerKey=api_key)

    # Get the uploads playlist ID
    request = youtube.channels().list(
        part='contentDetails',
        id=channel_id
    )
    response = request.execute()
    uploads_playlist_id = response['items'][0]['contentDetails']['relatedPlaylists']['uploads']

    # Get the live stream videos from the uploads playlist
    live_streams = []
    next_page_token = None
    n= 0
    while True:
        request = youtube.playlistItems().list(
            part='snippet',
            playlistId=uploads_playlist_id,
            maxResults=50,
            pageToken=next_page_token
        )
        try:
            response = request.execute()
            if response:
                print(1)
            for item in response['items']:
                video_id = item['snippet']['resourceId']['videoId']
                video_title = item['snippet']['title']

                # Check if the video is live
                video_request = youtube.videos().list(
                    part='snippet,liveStreamingDetails',
                    id=video_id
                )
                video_response = video_request.execute()

                if 'liveStreamingDetails' in video_response['items'][0]:
                    print("appended an item",n+1)
                    live_stream_url = f'https://www.youtube.com/watch?v={video_id}'
                    live_streams.append({'title': video_title, 'url': live_stream_url})
                    n+=1
                    if n>200:
                        return live_streams
        except Exception as e:
            print(e)

        next_page_token = response.get('nextPageToken')
        if not next_page_token:
            break

    return live_streams





if __name__ == "__main__":
    api_key = 'AIzaSyA4977yDihHfx75VfgCE09v_NeSVVCiRMM'
    url = "https://www.youtube.com/watch?v=XaoNTTGN2uA&t=1s&ab_channel=UnacademyIAS%3AEnglish"
    CHANNEL_ID =  get_channel_id_from_url(url)
    streams = []
    live_streams = get_live_streams(api_key, CHANNEL_ID)
    for stream in live_streams:
        print(f"Title: {stream['title']}, URL: {stream['url']}")
        streams.append([stream['title'],stream['url']])
    save_as_csv(streams,"un_ias_eng_url",headers=["title","url"])


