from airflow.decorators import dag, task
from airflow.utils.log.logging_mixin import LoggingMixin
import psycopg2
from psycopg2.extras import execute_values
import pendulum
from pendulum import datetime
import pandas as pd
import requests
import base64
import json
import os


@dag(
    start_date = datetime(2025, 8, 29),
    schedule = "@weekly",
    tags = ["krnb"],
    catchup = False
)

def find_krnb_artists():

    @task
    def get_artists():
        logger = LoggingMixin().log
        # ---------------- Access Spotify ----------------
        # REPLACE with personal Spotify client info
        client_id = "your_clientID"
        client_secret = "your_clientSecret"

        url = "https://accounts.spotify.com/api/token"

        # Get Access Token
        auth_str = f"{client_id}:{client_secret}"
        b64_str = base64.b64encode(auth_str.encode()).decode()
        auth_url = f"Basic {b64_str}"

        response = requests.post(url, 
                                headers={'Authorization': auth_url}, 
                                data={'grant_type': 'client_credentials'},
                                timeout=20)
        response.raise_for_status()
        access_token = response.json()["access_token"]

        logger.info("received token")
        # ---------------- Gather Data ----------------
        # Search krnb artists
        keyword = "%22korean%20rnb%22"

        search_q = f"q={keyword}&type=artist&limit=50"

        print(search_q)
        genreRsps = requests.get(
            url=f"https://api.spotify.com/v1/search?{search_q}",
            headers={'Authorization': f"Bearer {access_token}"},
            timeout=20
        )
        genreRsps.raise_for_status()

        krnb_json = genreRsps.json()

        logger.info("received data")

        # create python dictionary of artist info
        krnbArray = krnb_json['artists']['items']

        data = []
        for artist in krnbArray:
            data.append({
                "name": artist['name'],
                "SID": artist['id'],
                "followers": artist['followers']['total'],
                "popularity": artist['popularity'],
                "image_url": artist['images'][0]['url'] if artist['images'] else None,
                "artist_url": artist['external_urls']['spotify']
            })
        
        logger.info("created dict")

        # create dataframe from dict
        df = pd.DataFrame(data)
        df = df.sort_values(by='followers', ascending=True)
        small_df = df[df['followers'] <= 100000]

        logger.info("small_df created")

        print(small_df.head())  # log preview in Airflow
        
        # save full dataframe externally as backup
        # REPLACE with local path to store Airflow data
        data_storage_path = "DUMMY_path"
        output_folder = os.environ.get("AIRFLOW_HOME", data_storage_path)
        os.makedirs(output_folder, exist_ok=True)
        
        # REPLACE with local path to store emerging artist data
        output_path = os.path.join(output_folder, "DUMMY_path")
        small_df.to_csv(output_path, index=False)

        logger.info("file saved to output_path")

        # pass to next task using xcom
        return small_df.to_dict(orient='records')

    @task
    def artist_to_db(krnb_data):
        df = pd.DataFrame(krnb_data)
        print(f"df types: {df.dtypes}")
        
        # REPLACE with local database name, user, and password to store artist metrics
        conn = psycopg2.connect(
            dbname="DUMMY_db", user="DUMMY_user", password="DUMMY_pw", host="localhost"
        )
        cur = conn.cursor()

        rows = [tuple(x) for x in df.to_numpy()]
        execute_values(
            cur,
            "INSERT INTO krnb_artists (name, SID, followers, popularity, image_url, artist_url) VALUES %s",
            rows
        )
        conn.commit()
        cur.close()
        conn.close()

    # Pipeline
    data = get_artists()
    artist_to_db(data)

dag = find_krnb_artists()