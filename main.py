import spotipy
import spotipy.util as sp_util
import tweepy 
import os 
import configparser 
from time import sleep
import sqlite3

# database
db = sqlite3.connect('spotishare.db')
db_cursor = db.cursor()
db_cursor.execute("CREATE TABLE IF NOT EXISTS SAVEDTRACKS (uri text)")
db.commit()

# load config file 
config = configparser.ConfigParser()
config.read('config.ini')
scope = "user-library-read"

# set up env vars for spotipy 
os.environ["SPOTIPY_CLIENT_ID"] = config['SPOTIFY']['client_id']
os.environ["SPOTIPY_CLIENT_SECRET"] = config['SPOTIFY']['client_secret']
os.environ["SPOTIPY_REDIRECT_URI"] = config['SPOTIFY']['redirect_uri']

# auth code
###### for spotify
try:
    print("Attempting automatic Spotify authentication, please wait")
    token = sp_util.prompt_for_user_token(config['SPOTIFY']['username'], scope)
    spotify = spotipy.Spotify(auth=token)
except Exception as e:
    print(f"Spotify auth was not successful :( \n({str(e)})")
    exit()

###### for twitter
try:
    print("Attempting Twitter auth...")
    twitter_auth = tweepy.OAuth1UserHandler(config['TWITTER']['consumer_key'], config['TWITTER']['consumer_secret'], config['TWITTER']['access_token'], config['TWITTER']['access_token_secret'])
    twitter_api = tweepy.API(twitter_auth)
except Exception as e:
    print(f"Twitter auth was not successful :( \n({str(e)})")
    exit()

print("Everything authenticated successfully! Starting loop...")

while True:
    results = spotify.current_user_saved_tracks(1, 0)
    item = results['items'][0]['track']
    results = db_cursor.execute("SELECT * FROM SAVEDTRACKS WHERE uri = ?", (item['uri'],))
    results = results.fetchall()
    track_name = item['name']
    track_artists = item['artists'][0]['name']
    if not results:
        tweet_text = f'I just liked \"{track_name}\" by {track_artists} on Spotify:\n' + item['external_urls']['spotify']
        # this track has not been in our favorites before. run the tweet code.
        print("New track has been added to your library and is now being tweeted:\n", tweet_text)
        twitter_api.update_status(tweet_text)
        db_cursor.execute("INSERT INTO SAVEDTRACKS VALUES (?)", (item['uri'],))
        db.commit()
    # check every 10 seconds
    sleep(10)