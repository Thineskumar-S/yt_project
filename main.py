import streamlit as st
import mysql.connector
from youtube_engine import get_channel_info
from mongodb_engine import load
from sql_engine import *
from apiclient.discovery import build
import pymongo
import time
import pandas as pd

def run():

    API_KEY = "AIzaSyDeazLgd1T6hUwdvraWC6BKv5L1bpB_pgU"

    YOUTUBE_API_SERVICE_NAME = "youtube"
    YOUTUBE_API_VERSION = "v3"


    # creating Youtube connection Object
    youtube_object = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                        developerKey = API_KEY)
    
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

    connection_string="mongodb+srv://thineshkumar:Thinesh1234@practicecluster.kddvjwc.mongodb.net/"
    client = pymongo.MongoClient(connection_string)

    #App Title

    st.set_page_config(page_title="Youtube Analytics", page_icon='📶', layout="centered")


    st.title(':red[Youtube] Channel Analytics')
    st.header(' ')
    with st.container():   
        st.subheader("Validating the Channel info in Data Warehouse", divider='rainbow')
        channel_id = st.text_input(label="Enter/ Paste the channel Id here")
        submit_button = st.button(label=':blue[Submit]')

        #extraction message
        if submit_button:
            st.write('Fetching Channel information from Data warehouse')
            channel_data=get_channel_info(channel_id)
            channel_name=channel_data[0]['Channel_Name']   
            cursor_object.execute('select Channel_Name from channel_info')
            databases=cursor_object.fetchall()

            
            if channel_name in  databases:
                #streamlit output
                st.success('Successfully checked', icon="✅")
                st.write(f"The Channel Name '{channel_name}' is already in the data warehouse.")
            

            else:
                tab1, tab2,tab3 = st.tabs(["check","Load to Data Lake","From Data Lake to Data Warehouse"])

                with st.container():
                    with tab1:
                        st.write(f"The Channel Name '{channel_name}' is not in the database.")
                        st.write("Automatically Adding to Data lake")
                    with tab2:
                        with st.spinner ('Started to fetch for loading data in to Data Lake....'):
                            st.write('')
                            start_time = time.time()
                            loaded=load(channel_id,client)
                            end_time = time.time()
                            final_time=end_time-start_time
                            with st.expander("Update Info"):
                                st.success('Successfully updated', icon="✅")
                                st.write('Output from the loader function: ',loaded)
                                st.write(f"Total time taken to run this process '{final_time}' ")
                                st.success(f"'{channel_name}' has been added to the data lake !")
                    
                with tab3:
                    with st.spinner('fetching from Data Lake to load it in Data Warehouse'):
                        st.write('')
                        st.success('done !')
                        channel_name=channel_name.split(' ')
                        channel_name='_'.join(channel_name)
                        start_time = time.time()
                        loaded=transfer_to_sql(channel_name,cursor_object,client,connection_object)
                        end_time = time.time()
                        final_time=end_time-start_time
                        with st.expander("Update Info"):
                            st.success('Successfully updated', icon="✅")
                            st.write('Output from the loader function: ',loaded)
                            st.write(f"Total time taken to run this process '{final_time}' ")
                            st.success(f"'{channel_name}' has been added to the Data Warehouse !") 
    
    st.header("List of channels in the Data Warehouse", divider='rainbow')
    with st.container():
            col1,col2=st.columns(2)
            with col1:
                list_of_channel=list_of_channels(cursor_object)
                opted=st.radio("Choose a Channel to view it's Channel Data",list_of_channel,index=0)
            with col2:
                st.subheader('Channel Info')
                with st.expander(' '):
                    query='select * from channel_info where channel_name =%s'
                    cursor_object.execute(query,(opted,))
                    dynamic_info=cursor_object.fetchall()
                    df=pd.DataFrame(dynamic_info)
                    st.table(df) 
            
    #query output for faster execution:
    st.header("Analtical queries and results ", divider='rainbow')
    query_output=query_outputs(cursor_object)
    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            option = st.selectbox("Click on a button to view 👇",
                              Query_lists,
                              index=0,label_visibility="visible")
        with col2:
            st.subheader('output Result')
            with st.expander(' '):
                dynamic=dynamic_display(option,query_output)
                st.table(dynamic)

if __name__ == '__main__':
    run()