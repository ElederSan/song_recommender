
import sys
# Make sure that your config.py Python file with your credentials is located
# in the same folder as your Jupyter notebook.
from config import *

import spotipy
import json
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import numpy as np
import time

#Initialize SpotiPy with user credentias #
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=Client_ID,
                                                           client_secret=Client_Secret))

def search_song(title:str, artist:str=None,lim: int = 5):
    query = f"tracks:{title} artist: {artist}"
    try:
        results = sp.search(q=query)
        tracks = results['tracks']['items']
        track_id = tracks[0]['id']
        return track_id
    except:
        print("Song",title,"from",artist,"not found!")
        return ""

def get_audio_features_for_chunks(sp, list_of_song_ids, chunk_size=50, sleep_time=20):

    # Split the list_of_song_ids into chunks of size chunk_size
    song_id_chunks = [list_of_song_ids[i:i + chunk_size] for i in range(0, len(list_of_song_ids), chunk_size)]

    # Create an empty DataFrame to store the audio features
    df_audio_features = pd.DataFrame()

    # Iterate through each chunk
    for chunk in song_id_chunks:

        #print("Collecting audio features for chunk...")
        time.sleep(sleep_time) 
        my_dict = sp.audio_features(chunk)

        # Check if my_dict is not None and contains elements before creating a DataFrame
        if my_dict and isinstance(my_dict, list) and len(my_dict) > 0:
            # Create a new dictionary with a more structured format
            my_dict_new = {key: [item[key] for item in my_dict] for key in my_dict[0]}

            # Create a DataFrame from the audio features and append it to df_audio_features
            df_chunk = pd.DataFrame(my_dict_new)
            df_audio_features = pd.concat([df_audio_features, df_chunk], ignore_index=True)

    return df_audio_features


def merge_and_remove_duplicates(df, audio_features_df, merge_column='id'):
    """
    Merge a given DataFrame with the audio features DataFrame based on a specified column and remove all duplicates.

    Parameters:
    - df: Original DataFrame
    - audio_features_df: DataFrame containing audio features
    - merge_column: Column to merge on (default is 'id')

    Returns:
    - Merged and de-duplicated DataFrame
    """
   
    # Merge DataFrames
    merged_df = pd.merge(df, audio_features_df, on=merge_column, how='inner')

    

    # Remove all duplicates from the merged DataFrame
    merged_df = merged_df.drop_duplicates()

    return merged_df
def search_song_five(title:str, artist:str=None, lim: int = 5):
    if artist:
        query = f"track:{title} artist:{artist}"
    else:
        query = f"track:{title}"

    try:
        results = sp.search(q=query)
        tracks = results['tracks']['items']

        if not tracks:
            print("Song", title, "from", artist, "not found!")
            return pd.DataFrame()

        # Extract relevant information from each track
        records = []
        for track in tracks[:lim]:
            record = {
                'title': track['name'],
                'artist': ', '.join([artist['name'] for artist in track['artists']]),
                'id': track['id']
            }
            records.append(record)

        # Create DataFrame from the list of records
        df = pd.DataFrame(records)
        return df

    except Exception as e:
        print(f"Error: {e}")
        return pd.DataFrame()


def get_records_by_id_and_cluster(df, target_id, cluster_variable):
    # Check if the target_id is present in the ID column with the "hot" tag
    hot_records = df[(df['id'] == target_id) & (df['tag'] == 'hot')]

    if not hot_records.empty:
        # If "hot" records exist, return 5 records from the specific cluster
        hot_cluster_records = df[(df['tag'] == 'hot') & (df['dbscan_cluster'] == cluster_variable)].sample(5)
        return hot_cluster_records
    else:
        # If "not_hot" records, return 5 records from the specific cluster
        not_hot_cluster_records = df[(df['tag'] == 'not_hot') & (df['dbscan_cluster'] == cluster_variable)].sample(5)
        return not_hot_cluster_records


def scale_and_save(X, filename="scaler_v1.pickle"):
    """
    Scale the input data using StandardScaler, save the scaler object,
    and return the scaled data as a DataFrame.

    Parameters:
    - X: Input data (DataFrame or array-like)
    - filename: Path to save the scaler object (default: "scaler_v1.pickle")

    Returns:
    - X_scaled_df: Scaled data as a DataFrame
    """

    # Initialize StandardScaler
    scaler = StandardScaler()

    # Fit and transform the data
    X_scaled = scaler.fit_transform(X)

    # Save the scaler object to a file
    with open(filename, "wb") as file:
        pickle.dump(scaler, file)

    # Convert the scaled data to a DataFrame with column names
    X_scaled_df = pd.DataFrame(X_scaled, columns=X.columns)

    return X_scaled_df