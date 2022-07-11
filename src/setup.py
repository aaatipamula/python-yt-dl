import os
import json
import subprocess as sp
import platform
from tokenize import tabsize

class Setup:
    def __init__(self, start = False):
        
        if platform.system() == 'Windows':
            self.check = "C:\\"
        else:
            self.check = "/"

        if start == True:
            try:
                self.startup()
                self.install_ytdlp()
                self.json_dump()
            except KeyboardInterrupt:
                print("Exited.")
                exit()

    def startup(self):

        print("This program is entering inital setup. If you have already gone through this process, make sure you have not deleted your settings.json file in the ./src folder.\
            \n**WARNING RUNNING ANY OPEN SOURCE PROGRAM IS DANGEROUS AND YOU SHOULD BE SURE ABOUT WHAT THE PROGRAM IS DOING!**\
                \n\nIt is highly encouraged that you take a look at the source code before installing anything.\n")

        while True:
            try: 
                cont = input("Would you like to continue [y/n]: ")

                if cont in ['y', 'yes']:
                    break
                elif cont in ['n', 'no']:
                    print("\nAborted.")
                    exit()
                else:
                    print("\nPlease enter a valid argument.")
            except KeyboardInterrupt:
                    print("\nPlease enter a valid argument")

        while True:
            self.music_dir = input(f"\nPlease copy the full path of folder you would like to use for your mp3 downloads.\
            \nYou can always change this directory by navigating to the root folder of the project and updating the ./src/settings.json file.\n>>")

            if self.music_dir.startswith(self.check) is False:
                print("\nPlease enter a valid directory/folder.")

            else:
                break

        while True:
            self.video_dir = input(f"\nPlease copy the full path of folder you would like to use for your mp4 downloads.\
            \nYou can always change this directory by navigating to the root directory of the project and updating the ./src/settings.json file.\n>>")

            if self.video_dir.startswith(self.check) is False:
                print("\nPlease enter a valid directory/folder.")

            else:
                break

    def install_ytdlp(self):
        try: 
            sp.run(["python3", "-m", "pip", "install", "yt-dlp"], check=True)

        except sp.CalledProcessError:
            input("Something went wrong installing yt-dlp. \nTry running your command for invoking python followed by '-m pip install yt-dlp' in your command line. [Enter to continue] ")
        
        except FileNotFoundError:
            try:
                sp.run(["py", "-m", "pip", "install", "yt-dlp"], check=True)
            except Exception:
                input("Something went wrong installing yt-dlp. \nTry running your command for invoking python followed by '-m pip install yt-dlp' in your command line. [Enter to continue] ")

    def json_dump(self):

        data = {
            "video_dir":self.video_dir,
            "music_dir":self.music_dir,
        }

        with open("./src/settings.json", "w") as f:
            f.write(json.dumps(data, tabsize=4))
        
        print("Setup complete!")
        
if __name__ == "__main__":
    print("Please do not run as main file!")