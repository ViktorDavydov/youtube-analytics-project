# imports
import datetime
import os
import isodate
from googleapiclient.discovery import build


class PlayList:
    """Class PlayList initializing"""

    def __init__(self, pl_id):
        self.pl_id = pl_id
        self.title = self.get_pl_title()
        self.url = "https://www.youtube.com/playlist?list=" + self.pl_id

    @staticmethod
    def get_service():
        """Получение информации о сервисе"""
        api_key: str = os.getenv("YOUTUBE_API_KEY")
        youtube = build("youtube", "v3", developerKey=api_key)
        return youtube

    def get_pl_info(self):
        """Play list information getting"""
        playlist_info = self.get_service().playlistItems().list(playlistId=self.pl_id,
                                                                part="ContentDetails,snippet",
                                                                maxResults=50,
                                                                ).execute()

        return playlist_info

    def get_pl_title(self):
        """Play list title getting"""
        channel_id = self.get_pl_info()["items"][0]["snippet"]["channelId"]

        playlists = self.get_service().playlists().list(channelId=channel_id, part='snippet',
                                                        maxResults=50).execute()

        for item in playlists["items"]:
            if self.pl_id == item["id"]:
                pl_title = item["snippet"]["title"]
                break

        return pl_title

    def get_video_stats(self):
        """Videos from play list statistics getting"""
        video_ids: list[str] = [video['contentDetails']['videoId'] for video in
                                self.get_pl_info()['items']]

        video_response = self.get_service().videos().list(part='contentDetails,statistics',
                                                          id=','.join(video_ids)
                                                          ).execute()

        return video_response

    @property
    def total_duration(self):
        """Total durations of videos in play list counting"""
        total_time = []
        for video in self.get_video_stats()['items']:
            # YouTube video duration is in ISO 8601 format
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            total_time.append(duration)
            result_time = sum(total_time, datetime.timedelta())

        return result_time

    def show_best_video(self):
        """The URL of most liked video of play list getting"""
        video_likes = []
        for likes in self.get_video_stats()["items"]:
            video_likes.append(int(likes["statistics"]["likeCount"]))
        max_likes_video = max(video_likes)
        for likes in self.get_video_stats()["items"]:
            if int(likes["statistics"]["likeCount"]) == max_likes_video:
                most_liked_video = "https://youtu.be/" + likes["id"]

        return most_liked_video
