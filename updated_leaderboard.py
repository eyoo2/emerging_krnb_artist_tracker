import streamlit as st
import requests
import base64
import pandas as pd
import numpy as np

# ---------------- Variables ----------------
# REPLACE with local filepath to leaderboard csv file
csv_path = 'DUMMY_filepath.csv'
df = pd.read_csv(csv_path)
num_featured = 6

# ---------------- Get Artist Info ----------------
def add_featured(sid, name, access_token):
    artistRsp = requests.get(
                url=f"https://api.spotify.com/v1/artists/{sid}",
                headers={'Authorization': f"Bearer {access_token}"}
                )
    artist = artistRsp.json()
    st.subheader(name)
    st.image(f"{artist['images'][0]['url']}")
    st.write(artist['external_urls']['spotify'])
    randHeight = rng.integers(low=5, high=75)
    st.container(border=False, height=randHeight)

# ---------------- Access Spotify ----------------
# REPLACE with personal Spotify client info
client_id = "DUMMY_clientID"
client_secret = "DUMMY_clientSecret"

url = "https://accounts.spotify.com/api/token"

# Get Access Token
auth_str = f"{client_id}:{client_secret}"
b64_str = base64.b64encode(auth_str.encode()).decode()
auth_url = f"Basic {b64_str}"

response = requests.post(url, 
                         headers={'Authorization': auth_url}, 
                         data={'grant_type': 'client_credentials'})
access_token = response.json()["access_token"]


# ---------------- UI/UX Streamlit ----------------
st.image("https://i.pinimg.com/1200x/bd/c6/50/bdc650734a5070189d1876b50fd6e457.jpg", caption="Image Credits: https://pin.it/4FWLhsy0m (@chio on Pinterest)")
st.title("🔥 Hottest Emerging KR&B Artists")
st.markdown("<div style='text-align: center;'> 수믄 krnb 능력자들 찻기. </div>", unsafe_allow_html=True)
st.write("")
st.markdown("<div style='text-align: center;'> Love krnb? Find your next listen. Updates weekly. </div>", unsafe_allow_html=True)

st.divider()
st.header(f"❤️‍🔥 Featured Artists")
st.write("Take a look at our featured artists.")
rng = np.random.default_rng()
rands = rng.choice(15, size=num_featured, replace=False)
col1, col2 = st.columns(2)

for i in range(num_featured):
    sid = df['sid'][rands[i]]
    name = df['name'][rands[i]]
    if i % 2 == 0:
        with col1:
            add_featured(sid, name, access_token)
    else:
        with col2:
            if i == 1:
                st.container(border=False, height=10)
            add_featured(sid, name, access_token)
    

st.divider()
st.header(f"✨ Top 15 Emerging Krnb Artists")
st.write("Interactive dashboard of top 15 upcoming krnb artists.")
with st.container(border=True):
    st.dataframe(df[['name','followers','image_url','artist_url']],
                column_config={
                    "image_url": st.column_config.ImageColumn(),
                    "artist_url": st.column_config.LinkColumn()
                },
                hide_index=True,
                height=563)

st.divider()
st.subheader(f"💥 Credits:")
cafeurl = "https://www.notion.so/Erin-s-Cafe-23c3fd21bffb80ac94bae0d8f48ea1fd"
st.link_button("Erin Yoo", cafeurl)