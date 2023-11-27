from pytube import YouTube
from moviepy.video.io.VideoFileClip import VideoFileClip
from colorama import Fore
import os

def download_and_convert_audio(youtube_url, output_path, output_format="wav"):
    print(f"{Fore.YELLOW}Downloading video from {youtube_url}...{Fore.RESET}")

    youtube = YouTube(youtube_url)
    video = youtube.streams.filter().first()
    video.download(output_path=output_path, filename=f"temp_video.{output_format}")
    
    print(f"{Fore.YELLOW}Converting video to audio ({output_format})...{Fore.RESET}")

    video_clip = VideoFileClip(f"{output_path}/temp_video.{output_format}")
    audio_clip = video_clip.audio
    audio_clip.write_audiofile(f"{output_path}/output_audio.{output_format}")
    
    print(f"{Fore.GREEN}Successfully downloaded and converted video to audio.{Fore.RESET}")
    
    video_clip.close()
    audio_clip.close()
    os.remove(f"{output_path}/temp_video.{output_format}")