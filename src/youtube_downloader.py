import os
import json
from setup import Setup
from downloader import Downloader 

def main():
    while True:
        x = input("Start YouTube Downloader? [y/n]: ")
        if x.lower() in ['y', 'yes']:
            break
        elif x.lower() in ['n', 'no']:
            print("\nSTOPPING PROGRAM...")
            exit()
        else:
            print("\nPlease enter a valid option.")

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
        settings = json.load(open('./src/settings.json'))

        if 'settings.json' not in os.listdir('./src') and 'youtube_downloader.py' in os.listdir('./src'):
            main()
        else:
            Setup(start=True)

    except KeyboardInterrupt:
        print("\nExited.")
        
    except FileNotFoundError:
        print('Exception: Please navigate to the root directory of this project to run it!')

else: print('Please run this as main file!')