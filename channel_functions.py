from tqdm import tqdm
import time

def get_channel_ids(youtube, channel_list):
    """
    Channel IDs are required to uniquely identify channels
    Plus, these are required by some functions later.
    """
    channel_dict = {}  # Dictionary to store channel names and IDs

    for channel in channel_list:
        # Search for the channel using the channel name
        search_response = youtube.search().list(
            q=channel,
            part='id',
            type='channel',
            maxResults=1
        ).execute()

        # Extract the channel ID from the search results
        channel_id = search_response['items'][0]['id']['channelId']
        channel_dict[channel] = channel_id
        time.sleep(0.7)

    return channel_dict


def get_channel_stats(youtube, unique_channel_ids):
    all_channel_data = []
    for i in range(len(unique_channel_ids)):
        request = youtube.channels().list(
            part = 'snippet, contentDetails, statistics',
            id = unique_channel_ids)
        response = request.execute()

        for i in range(len(response['items'])):
            channel_data = dict(Channel_name = response['items'][i]['snippet']['title'], 
                            Channel_playlist =  response['items'][i]['contentDetails']['relatedPlaylists']['uploads'],
                            Subscriber_count = response['items'][i]['statistics']['subscriberCount'],
                            Video_count = response['items'][i]['statistics']['videoCount'])
            all_channel_data.append(channel_data)
            
    return all_channel_data


#creating a function to extract all the videos from the channels
def get_all_videos(youtube, playlists):
    all_video_ids = []
    for playlist_id in playlists:
        playlist_videos = []
        next_page_token = None

        while True:
            request = youtube.playlistItems().list(
                part = 'contentDetails',
                playlistId = playlist_id,
                maxResults = 50,
                pageToken=next_page_token
            )                
            response = request.execute()

            for i in range(len(response['items'])):
                video_id = response['items'][i]['contentDetails']['videoId']
                playlist_videos.append(video_id)
                    
            next_page_token = response.get('nextPageToken')               
            if not next_page_token:
                 break  

        all_video_ids.append(playlist_videos)
    return all_video_ids
                
#creating a function to extract video data from video ids
def get_video_details(youtube, videos):
    video_details = []
    for items in tqdm(videos):
        page_token = None

        while True:
            request = youtube.videos().list(
                part = 'snippet, contentDetails, statistics',
                id = items,
                maxResults = 50,
                pageToken = page_token
            )
            response = request.execute()

            video_details.extend(response['items'])
            page_token = response.get('nextPageToken')

            if not page_token:
                break

        all_details = {'video_ids': [],
            'descriptions': [],
            'titles': [],
            'view_counts': [],
            'channel_ids': [],
            'publish_dates': [],
            'tags': [],
            'thumbnails': []
        }
    
        for video in video_details:
            video_id = video['id']
            snippet = video['snippet']
            statistics = video['statistics']

            description = snippet.get('description', '')
            title = snippet.get('title', '')
            view_count = statistics.get('viewCount', '')
        #like_count = statistics.get('likeCount', '')
        #dislike_count = statistics.get('dislikeCount', '')
            channel_id = snippet.get('channelId', '')
            publish_date = snippet.get('publishedAt', '')
            tag = snippet.get('tags','')
            thumbnail = snippet['thumbnails'].get('default', '')

            all_details['video_ids'].append(video_id)
            all_details['descriptions'].append(description)
            all_details['titles'].append(title)
            all_details['view_counts'].append(view_count)
            all_details['channel_ids'].append(channel_id)
            all_details['publish_dates'].append(publish_date)
            all_details['tags'].append(tag)
            all_details['thumbnails'].append(thumbnail)

    return all_details
    

