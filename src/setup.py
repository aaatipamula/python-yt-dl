import os
import json
import shutil
import subprocess as sp
import platform
from install_ffmpeg import Installer_FFmpeg

os.chdir(__file__.strip("setup.py"))
data = json.load(open('data.json'))

'''
Stuff I have to do
- if any settings want to be changed run the [insert file name].py file to remove any programs installed, or change file locations

Notes to add to readme
- Although this program will install a recent stable release of ffmpeg for you, it is reccomended that you install ffmpeg with a package manager such as choco, or homebrew (link both websites)
- Warning about windows installations, this program may alter the PATH of your command line, although it is not likely that the program will tank you PATH, make sure to check your PATH by hitting windows and typing 'edit enviornment variables' 
  an export of your original path should be stored in a plaintext file within the home folder located at $HOME/Python-YouTube-Downloader

'''

class Setup:
    def __init__(self, start = False):
        self.location_dir = __file__.strip("setup.py")
        self.home_dir = os.path.expanduser("~")
        self.program_dir = f"{self.home_dir}/Python-Youtube-Downloader"
        self.system = platform.system()
        self.user_dir = os.getcwd()

        if start == True:
            self.startup()
            self.get_directories()
            Installer_FFmpeg(self.system, self.location_dir)
            self.install_ytdlp()
            self.move_files()
            self.json_dump()

    def startup(self):

        print("\n**WARNING, IF YOU HAVE NOT RUN THIS PROGRAM AS ADMIN FOR THE FIRST USE PLEASE EXIT THE PROGRAM AND RUN AS ADMIN!**\
                \n**WARNING RUNNING ANY OPEN SOURCE PROGRAM AS ADMIN IS DANGEROUS AND YOU SHOULD BE SURE ABOUT WHAT THE PROGRAM IS DOING!**\
                \n\n**It is highly encouraged that you take a look at the source code before installing anything.\n")

        while True:
            try: 
                cont = input("Would you like to continue [y/n]: ")

                if cont in ['y', 'yes']:
                    break
                elif cont in ['n', 'no']:
                    print("\n\nAborted.")
                    exit()
                else:
                    print("Please enter a valid argument.")
            except KeyboardInterrupt:
                    print("\nPlease enter a valid argument")

        if "Python-Youtube-Downloader" in os.listdir(self.home_dir):
            raise Exception("This program is already downloaded")

        os.mkdir(self.program_dir)
        os.chdir(self.program_dir)

    def get_directories(self):

        if self.system == "Windows":
            check = "C:\\"

        else:
            check = "/"

        while True:
            self.music_dir = input(f"\nPlease copy the full path of folder you would like to use for your mp3 downloads.\
            \nYou can always change this directory by navigating to {os.getcwd} and updating the settings.json file.\n>>")

            if self.music_dir.startswith(check) is False:
                print("Please enter a valid directory/folder.\n")

            else:
                break

        while True:
            self.video_dir = input(f"\nPlease copy the full path of folder you would like to use for your mp4 downloads.\
            \nYou can always change this directory by navigating to {os.getcwd} and updating the setting.json file.\n>>")

            if self.video_dir.startswith(check) is False:
                print("Please enter a valid directory/folder.\n")

            else:
                break


    def install_ytdlp(self):
        try: 
            sp.run(["python3", "-m", "install", "yt-dlp"], check=True)

        except sp.CalledProcessError:
            input("Something went wrong installing yt-dlp. \nTry running your command for invoking python followed by '-m pip install yt-dlp' in your command line. [Enter to continue] ")
        
        except FileNotFoundError:
            try:
                sp.run(["python3", "-m", "install", "yt-dlp"], check=True)
            except Exception:
                input("Something went wrong installing yt-dlp. \nTry running your command for invoking python followed by '-m pip install yt-dlp' in your command line. [Enter to continue] ")
            

    def move_files(self):
        shutil.copytree(self.location_dir, self.program_dir)

        print('You can now delete the folder you downloaded...') 

    def json_dump(self):

        data = {
            "video_dir":self.video_dir,
            "music_dir":self.music_dir,
            "operating_system":self.system,
            "program_dir":self.program_dir,
        }

        with open("settings.json", "w") as f:
            f.write(json.dump(data))
        
        print("Setup complete!")