# YouTube API Extractor

## Overview
This project retrieves information about videos from a specified YouTube playlist, including video titles, descriptions, statistics (likes, views, comments), and thumbnails.
The data is then processed and uploaded to a table in Google BigQuery for further analysis.

## Features
- Fetches video data from a specified YouTube playlist using the YouTube Data API v3.
- Retrieves statistics for each video using the same API.
- Stores the data in a pandas DataFrame.
- Uploads the DataFrame to Google BigQuery.
- Outputs the result to a CSV file.

## Usage
1. Clone this repository.
2. Install the required Python libraries.
3. Set up your Google Cloud Platform project and enable the YouTube Data API v3.
4. Replace the `youTube_api_key` and `playlist_id` variables in the code with your own API key and playlist ID.
5. Adjust the project_id, dataset_id, and table_id variables based on your Google BigQuery project setup.
6. Run the script by executing `python script.py` in your terminal.

## Challenge Details
The project aims to tackle the challenge of collecting and storing content from a YouTube playlist, focusing on extracting essential information from the videos included in the playlist. 
The solution involves the development of a Python script that utilizes the YouTube Data API to fetch data, performs necessary data processing, and generates an output file in CSV format.
Additionally, the collected data can be stored in a BigQuery table for further analysis.

## Note
- The solution provides an efficient way to gather and organize data from a YouTube playlist, facilitating further analysis and exploration of the content.
Additionally, the option to store the data in BigQuery enhances the scalability and accessibility of the collected information for future use.
- Ensure that you have enabled the YouTube Data API v3 and obtained the necessary API key before running the script.

## Author
Maria Alice Albuquerque
