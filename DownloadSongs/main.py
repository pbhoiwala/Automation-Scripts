import os
import shutil
import youtube_dl
from logger import MyLogger

songs_to_download = []
list_of_downloaded = []
cache_id_file = 'downloaded_songs.txt'
youtube_base_url = 'https://www.youtube.com/watch?v='
youtube_playlist = 'your-youtube-playlist-url'
pathToDestination = 'Path/To/Your/Destination/Directory'


def my_hook(d):
    """ Logger that prints when dl library is done
    with downloading and start conversion
    """
    if d['status'] == 'finished':
        print('Downloading complete, converting now...')


def read_cache_file():
    """ Reads cache file and populates list of
    songs that are already downloaded
    """
    with open(cache_id_file, 'r') as f:
        global list_of_downloaded
        return set(f.read().splitlines())


def get_download_options():
    """ Prepares download options for the dl library
    the default config is mp3 but can be changed
    :return:
    """
    return {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'logger': MyLogger(),
        'progress_hooks': [my_hook],
    }


def download_songs():
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        print("Parsing the playlist now...")
        playlist = ydl.extract_info(youtube_playlist, download=False)
        # print(list_of_downloaded)
        for song in playlist['entries']:
            if not song:
                print('ERROR: Unable to extract video information')
                continue
            song_id, song_title = song.get('id'), song.get('title')
            if song_id in list_of_downloaded:
                print('Already downloaded: ' + song_title)
                continue
            songs_to_download.append(youtube_base_url + song_id)
            cache.write(song_id + '\n')
            print('Song "' + song_title[0:10] + '..." added to cart for download')
        print('Downloading songs from the cart...')
        ydl.download(songs_to_download)


def transfer_files():
    print('Downloaded ' + str(len(songs_to_download)) + " new songs")
    print('Moving songs to GooglePlay Library...')
    try:
        for file_name in os.listdir("."):
            if file_name.endswith(".mp3"):
                destination_file = pathToDestination + '/' + file_name
                if not os.path.isfile(destination_file):
                    shutil.move(file_name, destination_file)
        print('Successfully moved songs to GooglePlay Library')
    except IOError as e:
        print('ERROR: Unable to move songs to GooglePlay Library')
        print(str(e.message))


if __name__ == "__main__":
    cache = open(cache_id_file, 'a+')
    ydl_opts = get_download_options()
    read_cache_file()
    download_songs()
    transfer_files()
