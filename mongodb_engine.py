import  pymongo
from youtube_engine import data


#connecting the necessary database with the mongodb server

# obtain the connection string from the server to connect via python

"""
connection_string="mongodb+srv://thineshkumar:Thinesh1234@practicecluster.kddvjwc.mongodb.net/"
client = pymongo.MongoClient(connection_string)
"""

def load(channel_id,client):

    """
    Inputs data to the mongo db.

    returns: the string as data loaded iside the mongodb.
    """



    channel_id=channel_id
    result = data(channel_id)
    channel_name = result[0][0]['Channel_Name']
    channel_name=channel_name.split(' ')
    channel_name='_'.join(channel_name)
    client=client
    db=client[channel_name]
    
    
    # Insert channel info
    channel_info = result[0][0]
    collection = db['channel_info']
    collection.insert_one(channel_info)
    
    # Insert video info
    video_info = result[1]
    collection= db['video_info']
    collection.insert_many(video_info)
    
    comments = result[2].copy()
    flat_comments = [comment for sublist in comments for comment in sublist]
    
    # Assuming 'flat_comments' is a list of dictionaries
    fixed_comments = []

    for comment in flat_comments:
        if isinstance(comment, dict):
            # Process dictionary items as before
            if 'video_id' not in comment:
                # Create a new dictionary with the missing key and value
                missing_data = {'video_id': 'Unknown'}
                complete_comment = {
                    **missing_data,
                    'Comments': comment['Comments'],
                    'comment_likes': comment.get('comment_likes', 0),
                    'reply_count': comment.get('reply_count', 0),
                    'replies': comment.get('replies', [])
                }
                fixed_comments.append(complete_comment)
            elif 'Disabled_comments' in comment:
                # Add default values for Disabled_comments documents
                missing_data = {
                    'Comments': 'Comments are disabled for this video',
                    'comment_likes': 0,
                    'reply_count': 0,
                    'replies': []
                }
                complete_comment = {
                    **missing_data,
                    'video_id': comment.get('video_id', 'Unknown')
                }
                fixed_comments.append(complete_comment)
            else:
                # If the comment is already complete, just append it as is
                fixed_comments.append(comment)

    # Now 'fixed_comments' contains only valid dictionary items with consistent keys and values
    collection=db['comments']
    collection.insert_many(fixed_comments)
    return 'The data is loaded in to the mongo db'


def extract_from_mongodb(channel_name,client):
    """
      Extracting data from the mongo db

      returns: channel, video info and comment.
      
      """


    a=[]
    b=[]
    c=[]
    channel_name=channel_name
    client = client
    db=client[channel_name]
    collection=db['channel_info']
    channel_info=collection.find()
    for channel in channel_info:
        a.append(channel)
    collection=db['video_info']
    video_info=collection.find()
    for video in video_info :
        b.append(video)
    collection=db['comments']
    comments=collection.find()
    for comment in comments:
        c.append(comment)
    return [a,b,c]






