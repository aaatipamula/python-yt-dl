import os
import json
import setup
from downloader import Downloader 

def main():

    while True:
        url = input("\nPlease input the url of the playlist/video you would like to download\n>> ")

        if url.startswith("https://www.youtube.com/"):
            break 
        else:
            print("Please enter a youtube url.")  

    while True:
        sel = input("\nPlease enter what format you would like to download in:\n1) Audio\n2) Video\n3) Both\n>> ")

        if sel in ['1', '2', '3']: 
            break
        else: 
            print("Please enter a valid option")

    Downloader(url, settings, sel).run()

if __name__ == "__main__":

    try: 

        if not('settings.json' in os.listdir('./src') and 'youtube_downloader.py' in os.listdir('./src')):
            setup.Setup().run()

        else:
            settings = json.load(open("./src/settings.json"))

            main()

    except ModuleNotFoundError:
        print("Please install required dependencies by running:\n\n'pip install -r requirements.txt'")
        print('\nPlease make sure you have FFmpeg installed and available from the command line!')

    except FileNotFoundError:
        print("Please navigate to the root directory of this project.")

    except KeyboardInterrupt:
        print("\nExited.")

