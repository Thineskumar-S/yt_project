#import mysql.connector
from mongodb_engine import extract_from_mongodb
import pandas as pd 
"""
connection_string='youtubeproject.cwoakibr9oeh.ap-south-1.rds.amazonaws.com'
user_name='ThineshKumar'
password='Thinesh1234'

connection_object = mysql.connector.connect(
host=connection_string,
user=user_name,
password=password)

cursor_object=connection_object.cursor()
cursor_object.execute("use youtube_project")
connection_object.commit()
"""

# button to click on to load from warehouse to sql through streamlit
def transfer_to_sql(channel_name,cursor_object,client,connection_object):
     client=client
     channel_name=channel_name
     channel_name=channel_name.split(' ')
     channel_name='_'.join(channel_name)
     a_,b_,c_=extract_from_mongodb(channel_name,client)
     #channel_name=a_['channel_name']

     #a- channel_info
     #b- video_info
     #c-comments_info

     # extract channel_info
     channel_id = a_[0].get("Channel_id")
     channel_Name = a_[0].get("Channel_Name")
     country = a_[0].get("country")
     playlist_id = a_[0].get("playlsit_id")
     views = a_[0].get("views")
     subscribers = a_[0].get("subcribers")  
     videos = a_[0].get("videos")

     sql = "INSERT INTO channel_info (channel_id, channel_Name, country, playlsit_id, views, subcribers, videos) VALUES (%s, %s, %s, %s, %s, %s, %s)"

     values = (channel_id, channel_Name, country, playlist_id, views, subscribers, videos)

     cursor_object.execute(sql, values)
     connection_object.commit()

     # video_info extraction
     for b in b_:
          video_id=b.get('video_id')
          video_Title=b.get('channelTitle')
          video_Title=b.get('title')
          description_of_video=b.get('description')
          publishedAt=b.get('publishedAt')
          viewCount=b.get('viewCount')
          likeCount=b.get('likeCount')
          commentCount=b.get('commentCount')
          duration=b.get('duration')
          sql = "INSERT INTO video_info (video_id,channel_Title,video_Title,description_of_video,publishedAt,viewCount,likeCount,commentCount,duration) VALUES (%s, %s, %s, %s,%s,%s,%s,%s)"
          values = (video_id,channel_Title,video_Title,description_of_video,publishedAt,viewCount,likeCount,commentCount,duration)
          cursor_object.execute(sql, values)
          connection_object.commit()
     

    #comments extraction

     for c in c_:    
          video_id = c.get("video_id")
          comments = c.get("Comments")
          comment_likes = c.get("comment_likes",0).get("$numberInt", 0)
          reply_count = c.get("reply_count",0).get("$numberInt", 0)
          sql = "INSERT INTO comments_and_replies (video_id, Comments, comment_likes, reply_count) VALUES (%s, %s, %s, %s)"
          values = (video_id, comments, comment_likes, reply_count)
          cursor_object.execute(sql, values)
          connection_object.commit()
     return f"Succesfully loaded the {channel_Name} Data from the Data Lake to Data Warehouse"

# 2part
def list_of_channels(cursor_object):
     cursor_object=cursor_object
     cursor_object.execute("select channel_name from channel_info")
     list_of_channels=cursor_object.fetchall()
     return list_of_channels

Query_lists=[
     "1. What are the names of all the videos and their corresponding channels?",
     "2. Which channels have the most number of videos, and how many videos do they have?",
     "3. What are the top 10 most viewed videos and their respective channels?",
     "4. How many comments were made on each video, and what are their corresponding video names?",
     "5. Which videos have the highest number of likes, and what are their corresponding channel names?",
     "6. What is the total number of likes for the channel in the video",
     "7. What is the total number of views for each channel, and what are their corresponding channel names?",
     "8. What are the names of all the channels that have published videos in the year 2022?",
     "9. What is the average duration of all videos in each channel, and what are their corresponding channel names?",
     "10. Which videos have the highest number of comments, and what are their corresponding channel names?"
     ]
#Query_lists=np.array(Query_lists)

#3rd part
def q1(cursor_object):
     # What are the names of all the videos and their corresponding channels?
     #must use join
     cursor_object.execute('select channel_Title,video_Title from video_info limit 20')
     video_titles=cursor_object.fetchall()
     df=pd.DataFrame(video_titles)
     return df
          
def q2(cursor_object):
     # Which channels have the most number of videos, and how many videos do they have?
     cursor_object.execute('select channel_Name, videos as Maximum_videos from channel_info order by channel_Name desc limit 1')
     x=cursor_object.fetchall()
     df=pd.DataFrame(x)
     return df

def q3(cursor_object):
     
     # What are the top 10 most viewed videos and their respective channels?
     cursor_object.execute('select channel_Title,video_Title,viewCount from video_info order by viewCount desc limit 10')
     cursor_object.fetchall()
     x=cursor_object.fetchall()
     df=pd.DataFrame(x)
     return df
     


def q4(cursor_object):
     # How many comments were made on each video, and what are their corresponding video names?
     cursor_object.execute('select video_Title, commentCount from video_info ')
     cursor_object.fetchall()
     x=cursor_object.fetchall()
     df=pd.DataFrame(x)
     return df



def q5(cursor_object):
     # Which videos have the highest number of likes, and what are their corresponding channel names?
     cursor_object.execute('select video_title,likeCount from video_info order by likecount desc limit 1 ')
     cursor_object.fetchall()
     x=cursor_object.fetchall()
     df=pd.DataFrame(x)
     return df



def q6(cursor_object):
     # What is the total number of likes for the channel in the video
     cursor_object.execute('select channel_Title as channel_name, sum(likeCount) Total_likes from video_info group by channel_Title ')
     cursor_object.fetchall()
     x=cursor_object.fetchall()
     df=pd.DataFrame(x)
     return df


def q7(cursor_object):
     # What is the total number of views for each channel, and what are their corresponding channel names?
     cursor_object.execute(' select channel_Title as channel_name, sum(viewCount) as Total_views from video_info group by channel_Title')
     cursor_object.fetchall()
     x=cursor_object.fetchall()
     df=pd.DataFrame(x)
     return df


def q8(cursor_object):
     #  What are the names of all the channels that have published videos in the year 2022?
     #might use regexp
     """
     cursor_object.execute('select channel_title, publishedAt from video_info where publishedAt>2022 ')
     cursor_object.fetchall()
     x=cursor_object.fetchall()
     df=pd.DataFrame(x)
     """
     return 'done'


def q9(cursor_object):
     # What is the average duration of all videos in each channel, and what are their corresponding channel names?
     cursor_object.execute('select channel_Title, avg(duration)from video_info group by channel_title ')
     cursor_object.fetchall()
     x=cursor_object.fetchall()
     df=pd.DataFrame(x)
     return df


def q10(cursor_object):
     # Which videos have the highest number of comments, and what are their corresponding channel names?
     cursor_object.execute('select channel_Title,video_Title,commentcount from video_info order by commentCount desc limit 1')
     cursor_object.fetchall()
     x=cursor_object.fetchall()
     df=pd.DataFrame(x)
     return df

def query_outputs(cursor_object):
     cursor_object=cursor_object
     a=q1(cursor_object)
     b=q2(cursor_object)
     c=q3(cursor_object)
     d=q4(cursor_object)
     e=q5(cursor_object)
     f=q6(cursor_object)
     g=q7(cursor_object)
     h=q8(cursor_object)
     i=q9(cursor_object)
     j=q10(cursor_object)
     output=[a,b,c,d,e,f,g,h,i,j]
     return output

def dynamic_display(value,output):
     if Query_lists[0]==value:
          return output[0]
     elif Query_lists[1]==value:
          return output[1]
     
     elif Query_lists[2]==value:
          return output[2]
     
     elif Query_lists[3]==value:
          return output[3]
     
     elif Query_lists[4]==value:
          return output[4]
     
     elif Query_lists[5]==value:
          return output[5]
     
     elif Query_lists[6]==value:
          return output[6]
     
     elif Query_lists[7]==value:
          return output[7]
     
     elif Query_lists[8]==value:
          return output[8]
     
     elif Query_lists[9]==value:
          return output[9]
     else:
          return output[10]

