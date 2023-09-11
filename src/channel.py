import json
import os
from googleapiclient.discovery import build
import isodate


class Channel:
    """Класс для ютуб - канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала.
        Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id
        self.channel_info = self.get_channel_info()
        self.title = self.channel_info["items"][0]["snippet"]["title"]
        self.desc = self.channel_info["items"][0]["snippet"]["description"]
        self.url = "https://www.youtube.com/" + self.channel_info["items"][0]["snippet"][
            "customUrl"]
        self.channel_subs_count = self.channel_info["items"][0]["statistics"]["subscriberCount"]
        self.video_count = self.channel_info["items"][0]["statistics"]["videoCount"]
        self.channel_views = self.channel_info["items"][0]["statistics"]["viewCount"]

    def __str__(self):
        """Magic method __str__ initializing"""
        return f"{self.title} ({self.url})"

    def __add__(self, other):
        """Magic + method"""
        return int(self.channel_subs_count) + int(other.channel_subs_count)

    def __sub__(self, other):
        """Magic - method"""
        return int(self.channel_subs_count) - int(other.channel_subs_count)

    def __gt__(self, other):
        """Magic > method"""
        return int(self.channel_subs_count) > int(other.channel_subs_count)

    def __ge__(self, other):
        """Magic >= method"""
        return int(self.channel_subs_count) >= int(other.channel_subs_count)

    def __lt__(self, other):
        """Magic < method"""
        return int(self.channel_subs_count) < int(other.channel_subs_count)

    def __le__(self, other):
        """Magic <= method"""
        return int(self.channel_subs_count) <= int(other.channel_subs_count)

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        channel = self.get_service().channels().list(id=self.channel_id,
                                                     part="snippet,statistics").execute()
        print(json.dumps(channel, indent=2, ensure_ascii=False))

    def to_json(self, json_name):
        """Запись информации о канале в файл json"""
        data = {"channel_id": self.channel_id,
                "channel_title": self.title,
                "channel_description": self.desc,
                "channel_url": self.url,
                "channel_subscribers_count": self.channel_subs_count,
                "channel_video_count": self.video_count,
                "channel_views": self.channel_views}
        with open(json_name, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=2, ensure_ascii=False)

    @property
    def channel_id(self):
        """Channel ID getter"""
        return self.__channel_id

    @classmethod
    def get_service(cls):
        """Получение информации о сервисе"""
        api_key: str = os.getenv("YOUTUBE_API_KEY")
        youtube = build("youtube", "v3", developerKey=api_key)
        return youtube

    def get_channel_info(self):
        """Получение информации о канале"""
        channel = self.get_service().channels().list(id=self.__channel_id,
                                                     part="snippet,statistics").execute()
        return channel
