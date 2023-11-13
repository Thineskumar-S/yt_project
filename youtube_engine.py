from apiclient.discovery import build
from googleapiclient.errors import HttpError
import re
"""
#Generated API key from Google Api Services
API_KEY = "AIzaSyDeazLgd1T6hUwdvraWC6BKv5L1bpB_pgU"

YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"


# creating Youtube connection Object
youtube_object = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                       developerKey = API_KEY)

#obtain channel_id from the user via user's input
#channel_id="UCjWY5hREA6FFYrthD0rZNIw"
"""

#get the channel info by this function.
def get_channel_info(channel_id):
    
    """
    function description:
    This function defined to fetch 
    the basic channel info from the youtube data api v3.

    parameters: 
    This function takes two parameters.
    1.youtube connection object via googleapiclient.discovery
    2.channel id to identify and extract the required basic information.

    returns: function retruns a list nested with dictioonary the chanel basic information as channel_data.
    
    """

    
    try:
        Channel_data=[]
        request = youtube_object.channels().list(
            part="snippet,contentDetails,statistics",
            id=channel_id)
    
        response = request.execute()
    
        for item in response["items"]:
            data={
                'Channel_Name':item['snippet']['title'],
                'Channel_id':item['id'],
                'country':item['snippet']['country'],
                'playlsit_id':item['contentDetails']['relatedPlaylists']['uploads'],
                'views':item["statistics"]['viewCount'],
                'subcribers':item['statistics']['subscriberCount'],
                'videos':item['statistics']['videoCount']
                }
            Channel_data.append(data)
    
    except HttpError as e:
        # Print the error details
        print(f"HttpError: {e}")
        print(f"Error content: {e.content}")
        print(f"Error details: {e.resp}")
    
    return Channel_data

#function calling to use the channel data variable for unpacking the playlist id
#channel_data=get_channel_info(youtube_object=youtube_object,channel_id=channel_id)
#playlist_id=channel_data[0]["playlsit_id"]

 
def get_video_ids(playlist_Id):

    """
    function description:
    This function defined to fetch 
    the channel's video id from the youtube data api v3.

    parameters: 
    This function takes two parameters.
    1.youtube connection object via googleapiclient.discovery
    2.playlist id is used to to identify and 
    extract the video ids. 
    
    Note: (the youtube api allows us to extract the 
    video id by using either the channel id or playlist id 
    which extracted from get_channel_info) 

    returns: function retruns list which contains the video id
    
    """

   
    video_ids = []  # Initialize the list to store video IDs
    
    try:
        next_page_token = None
        
        while True:
            request = youtube_object.playlistItems().list(
                part="snippet,contentDetails",
                playlistId=playlist_Id,
                maxResults=50,
                pageToken=next_page_token
            )
            response = request.execute()
            
            for item in response.get('items', []):
                video_id = item['contentDetails']['videoId']
                video_ids.append(video_id)
            
            next_page_token = response.get('nextPageToken')
            
            if not next_page_token:
                break  # No more pages to retrieve
    
    except HttpError as e:
        # Handle HTTP errors if necessary
        print(f"HttpError: {e}")
        print(f"Error content: {e.content}")
        print(f"Error details: {e.resp}")
    
    return video_ids  # Return the collected video IDs



#calling the function extract the list of video ids 
#video_ids=get_video_ids(youtube_object=youtube_object,playlist_Id=playlist_id)




#video_info=get_video_info(youtube_object=youtube_object,video_ids=video_ids)



def extract_duration_minutes_seconds(duration):
    """
    function description: 
    This func takes parameter and converts it 
    in to the desired string format.
    
    params:
    1. duration

    result:
    func returns the string in minutes and seconds.
    """

    match = re.search(r'(\d+)M(\d+)S', duration)
    if match:
        minutes = int(match.group(1))
        seconds = int(match.group(2))
        return f"{minutes} minutes {seconds} seconds"
    else:
        return None

def get_video_info(video_ids):
    
    """
    function description:
    This function defined to fetch 
    the channel's video information from the youtube data api v3.

    parameters: 
    This function takes two parameters.
    1.youtube connection object via googleapiclient.discovery
    2.video id is used to to identify and 
    extract the video info. 


    returns: function retruns list of dictionary which contains the video information.
    
    """
    all_video_info = []
    
    for i in range(0, len(video_ids), 50):
        request = youtube_object.videos().list(
            part="snippet,contentDetails,statistics",
            id=','.join(video_ids[i:i+50])
        )
        response = request.execute()
        
        for item in response['items']:
            extracted_data = {
                'snippet': ['channelTitle', 'title','description', 'publishedAt'],
                'statistics': ['viewCount', 'likeCount', 'commentCount'],
                'contentDetails': ['duration']
            }
            video_info = {}
            video_info['video_id'] = item['id']
            
            for key in extracted_data.keys():
                for value in extracted_data[key]:
                    try:
                        if key == 'contentDetails' and value == 'duration':
                            video_info[value] = extract_duration_minutes_seconds(item[key][value])
                        else:
                            video_info[value] = item[key][value]
                    except:
                        video_info[value] = None
            
            all_video_info.append(video_info)
    
    return all_video_info

# Example usage
#video_info = get_video_info(youtube_object, video_ids)

def get_comments(video_ids):
    """
    function description:
    This function defined to fetch 
    the video comments and replies from the youtube data api v3.

    parameters: 
    This function takes two parameters.
    1.youtube connection object via googleapiclient.discovery
    2.video id is used to to identify and 
    extract the video info. 


    returns: function retruns list of dictionary which contains 
    the comments and replies with their video id .
    
    """

    all_comments = []
    
    for video_id in video_ids:
        try:
            request = youtube_object.commentThreads().list(part="snippet,replies", videoId=video_id)
            response = request.execute()
            comments_and_replies = []
            
            for item in response['items']:
                extract_data_comments = {'video_id': video_id, 
                                         'comment': item['snippet']['topLevelComment']['snippet']['textOriginal'],
                                         'comment_likes': item['snippet']['topLevelComment']['snippet']['likeCount']
                                           }

                no_of_replies = item['snippet']['totalReplyCount']
                extracted_replies = []
                
                if no_of_replies:
                    for i in range(no_of_replies):
                        # Check if the index is within the valid range
                        if i < len(item['replies']['comments']):
                            reply = item['replies']['comments'][i]['snippet']
                            extracted_reply = {
                                'replies': reply['textOriginal'],
                                'reply_likes': reply['likeCount']
                            }
                            extracted_replies.append(extracted_reply)
                        else:
                            extracted_reply = {
                                'replies': 'No_reply for comment',
                                'reply_likes': 0
                            }
                            extracted_replies.append(extracted_reply)
                
                Comments_replies = {'video_id': video_id,
                    'Comments': extract_data_comments['comment'],
                    'comment_likes': extract_data_comments['comment_likes'],
                    'reply_count': no_of_replies,
                    'replies': extracted_replies
                    }
                comments_and_replies.append(Comments_replies)
            
            all_comments.append(comments_and_replies)
        
        except HttpError as e:
            # Handle the case where comments are disabled for the video
            error_message = f"Comments are disabled for video ID {video_id}"
            all_comments.append({'video_id': video_id,'Disabled_comments': error_message})
    
    return all_comments


#comments=get_comments(youtube_object=youtube_object,video_ids=video_ids)

def data(channel_id):


    """
    function description:
    This function defined to call the predefined functions to extract 
    the channel's information and comment's & replies information.

    parameters: 
    This function takes two parameters 
    1.channel_id
    2.Api key for accessing the google services.
    
    returns: function retruns list of dictionary which contains 
    the channel information, video information and comments& replies.
    
    """
    """
    API_KEY = Api_key
    YOUTUBE_API_SERVICE_NAME = "youtube"
    YOUTUBE_API_VERSION = "v3"
    #creating Youtube connection Object
    youtube_object = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                       developerKey = API_KEY)
    # obtain channel_id from the user via user's input
    
    channel_id=channel_id
    """
    channel_id=channel_id
    channel_data=get_channel_info(channel_id)
    playlist_id=channel_data[0]["playlsit_id"]
    video_ids=get_video_ids(playlist_id)
    video_info=get_video_info(video_ids)
    comments_and_replies=get_comments(video_ids)
    
    data=[channel_data,video_info,comments_and_replies]
    
    return data

# data driver
# data()