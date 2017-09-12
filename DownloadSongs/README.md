# Download Songs 
I automated the process of downloading songs from youtube and transferring them to my phone.
Follow the steps below if you want to set it up:
First make sure you have Python 2.7 installed and also install the [youtube_dl library](https://github.com/rg3/youtube-dl/blob/master/README.md#readme)

# Configuration

- YouTube playlist
    - Create a new playlist, call it something like 'Downloads' and add a few songs in it
    - Go to _Playlist Settings_ and mark the playlist privacy as '_Unlisted_'
    - '_Unlisted_' means that your playlist is not public but anyone with the link can access it
    - Copy the url of the playlist from the search bar (remove the extra url parameters like `&disable_polymer=true`

- Google Music manager:
    - Install [Google Music manager](https://play.google.com/music/listen?u=0#/manager)
    - Sign into your Google account
    - Create a new folder somewhere (in your `/home` or `~/Desktop` and call it 'Songs' or whatever you like. Remember the path
    - Assign that folder to Music Manager for automatic syncing
    - Install Google Play Music on your smartphone and in _Settings_, enable option to AutoDownload music (on WiFi)

- Script
    - Download all the files I have in this folder (`main.py`, `logger.py`, `config.txt`, `downloaded_songs.txt`)
    - Open `config.txt` and set `playlist=` to your youtube playlist url and set `path=` to the path to your Songs folder
    - Finally, run the main script like this: `python main.py` and if everything is set, you should see output like this

```Parsing the playlist now...
Song "Not Afraid..." added to cart for download
Song "Dark Horse..." added to cart for download
Song "Blank Spac..." added to cart for download
Downloading songs from the cart...
Downloading complete, converting now...
Downloaded 3 new songs
Moving songs to GooglePlay Library...
Successfully moved songs to GooglePlay Library 
```
After the setup is successful, all you need to do is 1) Add songs to your playlist and 2) Run the script. And that's it. Songs will be on your phone within minutes.

# How it works
The `main.py` python script is well commented and the code is pretty self-explanatory. In short, first I initialize some lists and objects; and then parse `config.txt` to get the playlist url and destination path. Then youtube_dl options are created in `get_download_options()` in which I specify the quality and format I'd like the songs to be downloaded.
Then I parse the playlist, iterate over each song, check if see if song is already downloaded or not, if not, then add the song to a list, and add the song id to `downloaded_songs.txt` and then start the actual download process. The songs get downloaded in current directory, so using `shutil`, the songs are transferred to the 'Songs' folder using the path you provided in config file. Google Music manager takes care of syncing your music from your local computer to your smartphone.
