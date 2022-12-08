# spotiShare
 Automatically tweet what songs you like on Spotify!

# Setup  
1. Go to https://developer.spotify.com/dashboard/applications and click "Create an App". Name and describe it however you want.
2. Click on "edit settings" and set the redirect URI to http://localhost:8080.
3. Open config.ini and fill in your client ID and client secret, both which can be obtained from the application page. If you don't like this, feel free to change the redirect URI in the config.ini, but make sure that matches the redirect URI in the spotify application settings. Note that removing a port will make it so you will manually need to paste in the token.
4. Go to https://developer.twitter.com, (more specifically https://developer.twitter.com/en/portal/projects/new) do their setup, and make an app. What you need will be in the keys and tokens tab of your app. You will need consumer/api key and consumer/api key secret, as well as access token and access token secret. Now fill out the TWITTER section of config.ini

# Usage  
Either just double-click main.py or run with `python main.py`, and the loop will start. 