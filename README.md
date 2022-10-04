# Simple YTDL CLI

A Simple CLI for the YTDL project. 

## Project Info

**Author**: Aniketh Aatipamula <br>
**Project Start Date**: February 4, 2022 <br>
**Contributors**: N/A <br>

**Project Origin**: I wanted a simpler way to use the yt-dlp project that wouldn't require typing out long commands in the terminal and either navigating or specifying folders I would like content to be downloaded into. 

**Project Description**: This project simplifies the entire process by giving the user 3 predetermined download options. Option one downloads audio in the highest possible quality and then converts it to mp3 before storing it in a specified folder. Option two does the same for video with the content being converted to mp4 instead of mp3. Option three does both simultaneously. 

## Project Notes

**Module Dependencies**: This project requires that a handful of non-standard python modules be installed. <br>
This includes:
- yt-dlp

## Running This Project

1. **Install FFmpeg**: This project requires that you install a third-party application called [FFmpeg](https://ffmpeg.org/). If you already have this application installed you can skip this step. If you need to install FFmpeg please refer to [this](https://github.com/aaatipamula/ffmpeg-install) guide.

2. Navigate to the root folder of the project (The folder which you downloaded this project) and run `python3 ./src/youtube_downloader.py` This will put you into setup mode and you will enter a folder you would like to store audio and video in. *Put in the entire path of the folder you would like to save your music/videos in.*

3. Run the previous command again and you should be put into the main program. Follow the directions to download and enjoy your content!