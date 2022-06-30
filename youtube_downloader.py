from ast import Mod
import os
import json
from setup import Setup

'''
***CHANGES TO MAKE TO THIS FILE***
'''

#os.chdir(__file__.strip("youtube_downloader.py"))
os.chdir("/home/aaatipamula/vscode_projects/youtube-downloader/")
settings = json.load(open('settings.json'))

def __init__():
    while True:
        x = input("YOU ARE STARTING THIS PROGRAM ARE YOU SURE YOU WANT TO START [y/n]: ")
        if x.lower() in ['y', 'yes']:
            break
        elif x.lower() in ['n', 'no']:
            print("\nSTOPPING PROGRAM...")
            exit()
        else:
            print("Please enter a valid option.")

    while True:
        url = input("\nPlease input the url of the playlist/video you would like to download\n>> ")
        if url.startswith("https://www.youtube.com/"):
            break 
        else:
            print("Please enter a youtube url.")  
    
    while True:
        sel = input("\nPlease enter what format you would like to download in...\nInput 1 for audio only, 2 for video, 3 for both.\n>> ")
        if sel in ['1', '2', '3']: 
            break
        else: 
            print("Please enter a valid option")

    Downloader(url, settings.get("music_dir"), settings.get("video_dir")).switcher(sel)
    

if __name__ == "__main__":
    try:
        from downloader import Downloader 

        if os.path.isdir(Setup().program_dir):
            __init__()
        else:
            Setup(start=True)

    except KeyboardInterrupt:
        print("\nExited.")
        
    except ModuleNotFoundError:
        Setup(start=True)
