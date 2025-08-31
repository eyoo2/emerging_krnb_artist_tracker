from airflow.sdk import dag, task
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.utils.log.logging_mixin import LoggingMixin
from pendulum import datetime
import pandas as pd
import os

@dag(
    start_date = datetime(2025, 8, 29),
    schedule = "@weekly",
    tags = ["krnb"],
    catchup = False
)

def analyze_krnb_db():
    @task
    def process_db():
        # REPLACE with local filepath to leaderboard csv file
        csv_path = 'DUMMY_filepath.csv'
        if os.path.exists(csv_path):
            os.remove(csv_path)
        
        # connect to Postgres
        # return sorted list of artists and metrics
        # REPLACE with connection id to local PostgreSQL database
        hook = PostgresHook(postgres_conn_id="DUMMY_connectionID")
        # REPLACE line 56 with local filepath to leaderboard csv file
        sql = """ COPY (
        WITH growth AS (
            SELECT name,                                  
                sid,
                followers,
                image_url,
                artist_url,
                LAG(followers, 1, NULL) OVER (PARTITION BY sid ORDER BY date) AS prev_fl,
                followers - LAG(followers, 1, NULL) OVER (PARTITION BY sid ORDER BY date) AS f_diff
            FROM krnb_artists
        ),
        artists AS (
            SELECT DISTINCT sid,
                            name
                FROM krnb_artists
        )
        SELECT K.sid,
                        K.name,
                G.followers,
                G.f_diff,
                G.image_url,
                G.artist_url
            FROM artists K
            JOIN growth G ON K.sid = G.sid
            WHERE G.f_diff IS NOT NULL
            ORDER BY G.f_diff DESC
            LIMIT 15
        )
        TO 'DUMMY_filepath.csv'
        DELIMITER ','
        CSV HEADER;
        """
        hook.run(sql)
        
        return csv_path

    # Pipeline
    process_db()

#analyze_krnb_db()
dag = analyze_krnb_db()