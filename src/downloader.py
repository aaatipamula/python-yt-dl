from yt_dlp import YoutubeDL
from yt_dlp.utils import DownloadError, PostProcessingError
import os
import threading

class Downloader():
    def __init__(self, url: str, dirs: dict, selection: str="1"):
        self.url = url
        self.dirs = dirs
        self.selection = selection

    def run(self):

        selection_key: dict[str, tuple] = {
        "1": ("music",
            {
            'format': 'bestaudio/best',
            'outtmpl': '%(title)s.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '320',
                }],
            }),

        "2": ("video",
            {
            'outtmpl':'%(title)s.%(ext)s',
            'postprocessors': [{
                'key':'FFmpegVideoConvertor',
                'preferedformat':'mp4',
                }],
            })
        }

        if self.selection == "3":

            opts1: tuple = selection_key.get("1")
            opts2: tuple = selection_key.get("2")

            t1 = threading.Thread(target=YoutubeDL(opts1[1]).download, args=([self.url]))
            t2 = threading.Thread(target=YoutubeDL(opts2[1]).download, args=([self.url]))

            os.chdir(self.dirs.get(opts1[0] + "_dir"))
            t1.start()

            os.chdir(self.dirs.get(opts2[0] + "_dir"))
            t2.start()

        else:

            opts: tuple = selection_key.get(self.selection)

            os.chdir(self.dirs.get(opts[0] + "_dir"))

            try: 
                with YoutubeDL(opts[1]) as ydl:
                    ydl.download([self.url])

            except DownloadError:
                print("Something went wrong downloading a video.")

            except PostProcessingError:
                print("Something went wrong using ffmpeg.\nPlease make sure you have ffmpeg installed and available from the command-line.")

