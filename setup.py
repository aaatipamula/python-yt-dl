import os
import json
import shutil
import subprocess as sp
import platform
import re
import zipfile

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
class Installer_FFmpeg:

    def __init__(self, system, origin_dir):

        self.system = system
        self.origin_dir = origin_dir

        print("**WARNING, THIS PROGRAM REQUIRES THAT FFMPEG, AN OPEN SOURCE AUDIO/VIDEO CONVERSION TOOL, BE INSTALLED IN ORDER TO WORK PROPERLY!**\
        \n\nYou have the option to manually install ffmpeg, which is a required program for this program to run, or have this program install ffmpeg for you.")

        while True:
            option = input("\nIf you would like to skip the install of ffmpeg entirely please input 'n' or 'no', if you would like to continue with the install of ffmpeg input 'y' or 'yes' \n>> ")

            if option in ['y', 'yes']:
                self.switcher()
                break

            elif option in ['n', 'no']:
                print("\nSkipping install of ffmpeg...")
                break

            else:
                print("Please enter a valid argument.")        

    def win_install(self):

        print(f"**WARNING, THIS PROGRAM IS GOING TO ALTER THE PATH VARIABLE, THIS CAN POTENTIALLY BE DESTRUCTIVE SO A COPY OF YOUR PATH VARIABLE WILL BE STORED IN {self.origin_dir}.\
        IF YOUR PATH IS DESTROYED OR YOU EXPERIENCE ANY PROBLEMS IN THE COMMAND LINE REFER TO THE README AT https://github.com/aaatipamula/python-youtube-downloader.")

        win_path = sp.run("%path%", shell=True, capture_output=True, text=True)

        with open('win_path_backup.txt', 'w') as f:
            f.write(win_path.stdout)

        os.chdir('C:/')

        try:

            get_url = sp.run(['curl', data.get("ffmpeg_win")], capture_output=True, text=True, check=True)

            url = re.search(r"(https.+zip)", get_url.stdout).group()

            file = url.split("packages/")[1]

            sp.run(['curl', url, '-o', file], check=True)

        except sp.CalledProcessError:
            print("Something went wrong trying to download ffmpeg, please try running this program again, if that has failed again, refer to manual installation instructions.")

        try:
            with zipfile.ZipFile(file, "r") as z:
                z.extractall()
        except Exception:
            print("Something went wrong trying to unzip ffmpeg, navigate to 'C:\\' and try and manually unzip the file.")

        os.remove(file)

        ffmpeg_path = os.path.join(os.getcwd(), file.strip(".zip")) + "\\bin"

        sp.run(f'setx path "%path%;{ffmpeg_path}', shell=True)

        os.chdir(self.origin_dir)

    def mac_install(self):

        os.chdir("/usr/local/bin")

        try:
            sp.run(['curl', data.get("ffmpeg_mac"), '-o', 'ffmpeg.zip'], check=True)
        except sp.CalledProcessError:
            print("Something went wrong trying to download ffmpeg, please try running this program again, if that has failed again, refer to manual installation instructions.")

        try:
            with zipfile.ZipFile("ffmpeg.zip") as z:
                z.extract()
        except Exception:
            print(f"Something went wrong trying to unzip ffmpeg, please navigate to '{os.getcwd()}' and try to manually unzip the file.")

        os.remove("ffmpeg.zip")

        os.chmod("ffmpeg", 0o500)

        os.chdir(self.origin_dir)

    def linux_install(self):
            
        while True:

            pacman = input("Input the name of your package manager followed by a space.\n>> ")

            pacman.split(" ")

            if pacman[0] not in data.get("distros"):
                print("This package manager is not recognized, if anything goes wrong during this install please make sure you entered the right package manager and option for install.")
                break

            else:
                sp.run([pacman[0], pacman[1], "ffmpeg"])
                break
                
    def switcher(self):
        
        key = {
        "Windows":"win",
        "Darwin":"mac",
        "Linux":"linux",
        }
        
        method_name = f"{key.get(self.system, '.')}_install"
        method = getattr(self, method_name, "This is not a supported Operating System! Please use this program with either Windows, macOSX, or Linux.")
        if type(method) is str:
            return print(method)
        return method()


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
            self.music_dir = input(f"Please copy the full path of folder you would like to use for your mp3 downloads.\
            \nYou can always change this directory by navigating to {os.getcwd} and updating the setting.json file.\n>>")

            if self.music_dir.startswith(check) is False:
                print("Please enter a valid directory/folder.\n")

            else:
                break

        while True:
            self.video_dir = input(f"Please copy the full path of folder you would like to use for your mp4 downloads.\
            \nYou can always change this directory by navigating to {os.getcwd} and updating the setting.json file.\n>>")

            if self.video_dir.startswith(check) is False:
                print("Please enter a valid directory/folder.\n")

            else:
                break


    def install_ytdlp(self):
        try: 
            sp.run(["py", "-m", "install", "yt-dlp"], check=True)

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
            f.write(json.dumps(data))
        
        print("Setup complete!")

