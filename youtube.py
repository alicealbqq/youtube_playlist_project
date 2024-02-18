from googleapiclient.discovery import build
import pandas as pd
from google.oauth2 import service_account

# YouTube API key
youTube_api_key="AIzaSyCesV6nmHSZRkNRDpDCOI1wwqeRdoyaMuI"
# Build the YouTube service
youtube_service = build('youtube', 'v3', developerKey=youTube_api_key)
playlist_id = 'PLMC9KNkIncKvYin_USF1qoJQnIyMAfRxl'
playlist_name = 'Best Pop Songs of All Time'

def fetch_playlist_videos(playlist_id):
    playlist_videos = []
    next_page_token = None

    try:
        # Loop to retrieve all videos in the playlist
        while True:
            res = youtube_service.playlistItems().list(part='snippet', playlistId = playlist_id, maxResults=50, pageToken=next_page_token).execute()
            if 'items' in res:
                # Add fetched videos to the playlist_videos list
                playlist_videos += res['items']
            else:
                print("Erro ao buscar vídeos da playlist: ", res)

            # Get next page token for pagination
            next_page_token = res.get('nextPageToken')
            if next_page_token is None:
                break

    except Exception as e:
        print("Erro durante a execução: ", e)
    
    return playlist_videos

def fetch_video_statistics(video_ids):
    stats = {}

    for video_id in video_ids:
        res = youtube_service.videos().list(part='statistics', id=video_id).execute()
        stats[video_id] = res['items'][0]

    return stats

def extract_data(playlist_videos, stats):
    data = []

    for video in playlist_videos:
        snippet = video['snippet']
        video_id = snippet['resourceId']['videoId']

        # Find statistics information for the current video
        stats_info = stats[video_id]
        # Extract relevant data
        data.append({
            'video_id': video_id,
            'title': snippet['title'],
            'video_description': snippet['description'],
            'published_date': str(snippet['publishedAt']),
            'thumbnail': snippet['thumbnails']['high']['url'],
            'likes': int(stats_info['statistics']['likeCount']) if stats_info else None,
            'views': int(stats_info['statistics']['viewCount']) if stats_info else None,
            'comments': int(stats_info['statistics']['commentCount']) if stats_info else None,
        })
    
    return data

def upload_to_bigquery(data):
    # BigQuery Configuration
    project_id = 'mindful-coder-414613'
    dataset_id = 'playlist_youtube'
    table_id = 'dados_youtube'

    table_path = f'{project_id}.{dataset_id}.{table_id}'
    key_path = './mindful-coder-414613-16c0481c6d17.json'

    credentials = service_account.Credentials.from_service_account_file(key_path, scopes=['https://www.googleapis.com/auth/cloud-platform'])

    try:
        # Convert data to a pandas DataFrame
        df = pd.DataFrame(data)
        # Load the DataFrame to BigQuery using to_gbq
        df.to_gbq(destination_table=table_path, project_id=project_id, if_exists='replace', credentials=credentials)
        print(f'DataFrame loaded to BigQuery: {table_path}')
    except Exception as e:
        print("Error uploading DataFrame to BigQuery:", e)

def save_to_csv(data, playlist_data):
    try:
        # Convert data to a pandas DataFrame
        df = pd.DataFrame(data)
        # Save DataFrame to a CSV file
        df.to_csv(playlist_data, index=False)
        print(f'Data saved to CSV: {playlist_data}')
    except Exception as e:
        print("Error saving DataFrame to CSV:", e)

def main():
    # Fetch playlist videos
    playlist_videos = fetch_playlist_videos(playlist_id)
    # Extract video IDs from the playlist
    video_ids = [video['snippet']['resourceId']['videoId'] for video in playlist_videos]
    # Fetch statistics for the videos
    stats = fetch_video_statistics(video_ids)
    # Extract relevant data from videos and their statistics
    data = extract_data(playlist_videos, stats)
    # Upload the extracted data to BigQuery
    upload_to_bigquery(data)
    # Save the extracted data to CSV
    save_to_csv(data, 'playlist_data.csv')

if __name__ == "__main__":
    main()