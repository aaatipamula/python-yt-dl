import re
import zipfile
import subprocess as sp
import os
import json

os.chdir(__file__.strip('install_ffmpeg.py'))
data = json.load(open('data.json'))

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