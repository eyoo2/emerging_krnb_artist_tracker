# emerging_krnb_artist_tracker
The Emerging KR&amp;B Artist Tracker is a dashboard that displays the top 15 emerging Korean R&amp;B artists based on weekly Spotify follower count and popularity score data. The dashboard is run via 2 Python DAGs (directed acyclic graph) which are executed using Apache Airflow and the Spotify WebAPI on your local machine.

Weekly Spotify “measurements” are taken and stored in a PostgreSQL database. The top 15 artists with the fastest recent growth are identified from the database, then displayed on the dashboard through Streamlit. The feature section randomly chooses to display 6 artists from the top 15.

## DIRECTIONS
* To recreate on your local machine, find all comments with the keyword "REPLACE" in the Python files to create the correct setup on your local machine.
* You must also create a PostgreSQL database with the necessary columns using the provided SQL file.
