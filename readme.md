# Streamlit Channel Analytics App :rocket:

## Project Description :page_facing_up:

The Streamlit Channel Analytics App is a powerful tool that simplifies the process of checking, collecting, and analyzing data related to YouTube channels. It offers a seamless workflow consisting of three main stages:

1. **Channel Data Validation** :mag_right:
   
   - **Validation**: The app checks if a given channel ID is already present in the data warehouse.
   - **Data Retrieval**: If the channel is not found, it sources the channel's information from the YouTube Data API.
   - **Data Lake**: After retrieval, the data is stored in a data lake, specifically a MongoDB database.

2. **Data Transfer to Data Warehouse** :floppy_disk:

   - **Warehouse Load**: The user can trigger the app to move the necessary data from the data lake (MongoDB) to the data warehouse (MySQL). This step ensures that the channel data is readily available for analysis.

3. **Channel Analytics** :bar_chart:

   - **Channel List**: The app displays a list of channels currently available in the data warehouse.
   - **Analytical Questions**: Users can choose from a list of analytical questions, selecting one to visualize as a table. These tables help users make informed decisions about the channels.

## Learning Experience :bulb:

This project has been a fantastic learning opportunity, offering a wide range of experiences and challenges:

1. **API Integration** :computer:

   - **API Interaction**: The project involved interacting with the YouTube Data API to fetch data in JSON format.
   - **Data Transformation**: Had to work with JSON data, which was a new experience for me.

2. **Database Setup** :floppy_disk:

   - **Database Configuration**: successfully configured and deployed two databases: MongoDB for the Data Lake and MySQL for the Data Warehouse, both hosted on the cloud. MongoDB Atlas a manged service provided by MongoDB inc, MySQL engine was hosted in AWS.
   - **Data Migration**: The project required transferring data from MongoDB to MySQL, which helped gain valuable experience in database management.
   - **Schema Design**: Carefully designed and configured schemas for both databases, optimizing data storage.
   - **Data Preprocessing**: Data transferred to the databases undergoes further preprocessing, including schema configuration.



3. **Modular Code** :gear:

   - **Code Organization**: implemented a modular code structure, organizing functions and methods efficiently.
   - **Reusability**: Modular code promotes code reusability and maintainability.

4. **User Experience Optimization** :star2:

   - **User-Centric Design**: prioritized providing an excellent user experience, focusing on optimizing user interactions and feedback.

## How to Run the App :computer:

1. Clone this repository to your local machine.

2. Navigate to the project directory.

3. Create a virtual environment (optional but recommended):
 ```bash
    
   python -m venv venv
   source venv/bin/activate  # On Windows, use: venv\Scripts\activate
   ```
   ```Terminal/cmd/bash
   pip install -r requirements.txt
   streamlit run main.py
```
## Project Structure :file_folder:

The project's file structure is organized as follows:
   ```bash
          my_streamlit_app/
          ├── main.py
          ├── mongo_engine.py
          ├── sql_engine.py
          ├── youtube_engine.py
          ├── requirements.txt
```
This structure provides a clear organization of the project's files and modules.


Thank you for using the Streamlit Channel Analytics App! :rocket: If you have any questions or feedback, please feel free to reach out.

Happy analyzing! :chart_with_upwards_trend:





