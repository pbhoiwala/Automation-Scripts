import os
import shutil
import youtube_dl
from logger import MyLogger

# Initialize objects
songs_to_download = []
list_of_downloaded = set()
cache_id_file = 'downloaded_songs.txt'
youtube_base_url = 'https://www.youtube.com/watch?v='

# Read values from user's config file
config = dict(l.strip().split('=', 1) for l in open('config.txt'))
youtube_playlist = config['playlist']
path_to_destination = config['path']


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
        list_of_downloaded = set(f.read().splitlines())


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
    """ Parses the playlist and iterates over every song to see if it
    is already downloaded or not. If not, then adds it to list of songs
    to  download, adds the song_id to the cache file and starts download
    """
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        print("Parsing the playlist now...")
        playlist = ydl.extract_info(youtube_playlist, download=False)
        # print(list_of_downloaded)
        for song in playlist['entries']:
            if song:
                song_id, song_title = song.get('id'), song.get('title')
                if song_id in list_of_downloaded:
                    print('Already downloaded: ' + song_title[0:10] + '...')
                else:
                    songs_to_download.append(youtube_base_url + song_id)
                    cache_file.write(song_id + '\n')
                    print('Song "' + song_title[0:10] + '..." added to cart for download')

        # make sure there are more than 0 songs to download and transfer them
        if songs_to_download:
            print('Downloading songs from the cart...')
            ydl.download(songs_to_download)
            print('Downloaded ' + str(len(songs_to_download)) + " new songs")
            transfer_files()
        else:
            print('No new songs to download. Everything is upto date')


def transfer_files():
    """ Iterates over every 'mp3' file in the current directory and
    makes sure that the file doesn't exist in the destination
    directory and then transfer the file
    """
    print('Moving songs to GooglePlay Library...')
    for file_name in os.listdir("."):
        try:
            if file_name.endswith(".mp3"):
                destination_file = path_to_destination + '/' + file_name
                if not os.path.isfile(destination_file):
                    shutil.move(file_name, destination_file)
        except IOError as e:
            print('ERROR: Unable to move songs to GooglePlay Library')
            print(str(e.message))
    print('Successfully moved songs to GooglePlay Library')


if __name__ == "__main__":
    cache_file = open(cache_id_file, 'a+')
    ydl_opts = get_download_options()
    read_cache_file()
    download_songs()
