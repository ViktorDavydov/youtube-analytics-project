import os
from googleapiclient.discovery import build


class Video:
    """Video class initializing"""

    def __init__(self, video_id):
        self.video_id = video_id
        self.video_info = self.get_video_info()
        self.title = self.video_info["items"][0]["snippet"]["title"]
        self.url = "https://www.youtube.com/watch?v=" + self.video_id
        self.video_views = self.video_info["items"][0]["statistics"]["viewCount"]
        self.video_likes_count = self.video_info["items"][0]["statistics"]["likeCount"]
        self.real_video_id = self.video_info["items"][0]["id"]

    def __str__(self):
        """str method initializing"""
        return f"{self.title}"

    @staticmethod
    def get_service():
        """Получение информации о сервисе"""
        api_key: str = os.getenv("YOUTUBE_API_KEY")
        youtube = build("youtube", "v3", developerKey=api_key)
        return youtube

    def get_video_info(self):
        """Получение информации о видео"""
        video = self.get_service().videos().list(id=self.video_id,
                                                 part="snippet,statistics").execute()
        return video


class PLVideo:
    """PLVideo class initializing"""

    def __init__(self, video_id, pl_id):
        self.pl_id = pl_id
        self.video_id = video_id
        self.pl_info = self.get_pl_items_info()
        self.video_info = self.get_video_info()
        self.title = self.video_info["items"][0]["snippet"]["title"]
        self.url = "https://www.youtube.com/watch?v=" + self.video_id
        self.video_views = self.video_info["items"][0]["statistics"]["viewCount"]
        self.video_likes_count = self.video_info["items"][0]["statistics"]["likeCount"]
        self.real_pl_id = self.pl_info["items"][0]["id"]

    def __str__(self):
        """str method initializing"""
        return f"{self.title}"

    @staticmethod
    def get_service():
        """Получение информации о сервисе"""
        api_key: str = os.getenv("YOUTUBE_API_KEY")
        youtube = build("youtube", "v3", developerKey=api_key)
        return youtube

    def get_pl_items_info(self):
        """Получение информации о плейлисте"""
        playlist_videos = self.get_service().playlistItems().list(playlistId=self.pl_id,
                                                                  part='contentDetails',
                                                                  maxResults=50,
                                                                  ).execute()
        return playlist_videos

    def get_video_info(self):
        """Получение информации о видео"""
        video = self.get_service().videos().list(id=self.video_id,
                                                 part="snippet,statistics").execute()
        return video
