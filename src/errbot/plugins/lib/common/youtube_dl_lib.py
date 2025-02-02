import time
import uuid

from yt_dlp import YoutubeDL
from yt_dlp.utils import DownloadError


class YtdlLib:
    def __init__(self, max_length=600):
        """
        Initialize the youtube_dl library
        :param max_length: the maximum length of a video in seconds (default 600 aka 10 minutes)
        """
        self.path = "plugins/play/audio"
        self.max_length = max_length

    def video_metadata(self, url):
        """
        Get all the video metadata for a YouTube URL with youtube_dl
        :param url: the full url to the video
        :return: a dictionary with all the metadata
        """
        ydl_opts = {
            "format": "bestaudio/best",
            "noplaylist": True,
            "quiet": True,
            "prefer_ffmpeg": True,
            "audioformat": "wav",
        }
        with YoutubeDL(ydl_opts) as ydl:
            dictMeta = ydl.extract_info(url, download=False)
            return dictMeta

    def download_audio(self, url, file_name=None):
        """
        Downloads an audio file from a given youtube url
        :param url: the full url to the video
        :param file_name: optional file name to save the file as
        :return: the path to the downloaded audio file
        """
        # If the file_name was provided, use it, otherwise generate a random one
        if file_name:
            output_file = f"{self.path}/{file_name}.mp3"
        else:
            output_file = f"{self.path}/{uuid.uuid4()}.mp3"

        ydl_opts = {
            "format": "bestaudio/best",
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }
            ],
            "outtmpl": output_file,
            "quiet": True,
        }

        # Create a retry loop to download the video
        downloaded = False
        for i in range(3):
            try:
                self.downloader(ydl_opts, url)
                # If the download was successful, break out of the loop
                downloaded = True
                break
            except DownloadError:
                # If the download failed, wait and try again
                time.sleep(1 + i)

        # If the download failed, raise an exception
        if not downloaded:
            raise DownloadError

        return output_file

    def downloader(self, ydl_opts, url):
        """
        Function to download a video with youtube_dl
        :param ydl_opts: the youtube_dl options
        :param url: the full url to the video
        :return: None
        Note: The file will be downloaded to the path specified in ydl_opts
        """
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
