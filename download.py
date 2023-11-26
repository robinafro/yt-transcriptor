from pytube import YouTube
from moviepy.video.io.VideoFileClip import VideoFileClip
import os

def download_and_convert_audio(youtube_url, output_path, output_format="wav"):
    # Download YouTube video
    youtube = YouTube(youtube_url)
    video = youtube.streams.filter().first()
    video.download(output_path=output_path, filename=f"temp_video.{output_format}")
    
    # Convert to the specified audio format
    video_clip = VideoFileClip(f"{output_path}/temp_video.{output_format}")
    audio_clip = video_clip.audio
    audio_clip.write_audiofile(f"{output_path}/output_audio.{output_format}")

    # Clean up temporary files
    video_clip.close()
    audio_clip.close()
    os.remove(f"{output_path}/temp_video.{output_format}")

# Example usage
youtube_url = "https://www.youtube.com/watch?v=vXYzoFJOS1U"
output_path = "C:/Users/actul/Documents/TEST"
download_and_convert_audio(youtube_url, output_path)
