"""YouTube service using yt-dlp for channel search and video extraction."""

from dataclasses import dataclass
from typing import Optional
import yt_dlp


@dataclass
class ChannelInfo:
    """YouTube channel information."""
    id: str
    name: str
    url: str
    subscriber_count: Optional[int] = None
    subscriber_count_str: Optional[str] = None
    video_count: Optional[int] = None
    description: Optional[str] = None


@dataclass
class VideoInfo:
    """YouTube video information."""
    id: str
    title: str
    url: str
    duration: Optional[int] = None
    upload_date: Optional[str] = None
    thumbnail: Optional[str] = None


@dataclass
class PlaylistInfo:
    """YouTube playlist information."""
    id: str
    title: str
    url: str
    video_count: Optional[int] = None


class YouTubeService:
    """Service for interacting with YouTube via yt-dlp."""

    def __init__(self):
        self._ydl_opts = {
            "quiet": True,
            "no_warnings": True,
            "extract_flat": True,
        }

    def search_channels(self, query: str, max_results: int = 30) -> list[ChannelInfo]:
        """Search for YouTube channels by name, sorted by subscriber count."""
        # Search for a few more videos than requested to find distinct channels
        search_url = f"ytsearch{max_results + 10}:{query}"
        
        with yt_dlp.YoutubeDL(self._ydl_opts) as ydl:
            try:
                result = ydl.extract_info(search_url, download=False)
                channels = []
                seen_channels = set()
                
                if result and "entries" in result:
                    for entry in result["entries"]:
                        if entry and entry.get("channel_id"):
                            channel_id = entry["channel_id"]
                            if channel_id not in seen_channels:
                                seen_channels.add(channel_id)
                                # Handle different metadata layouts in yt-dlp results
                                sub_count = (
                                    entry.get("channel_follower_count") or 
                                    entry.get("uploader_follower_count") or 
                                    entry.get("follower_count") or 
                                    entry.get("subscribers")
                                )
                                channels.append(ChannelInfo(
                                    id=channel_id,
                                    name=entry.get("channel", entry.get("uploader", "Unknown")),
                                    url=f"https://www.youtube.com/channel/{channel_id}/videos",
                                    subscriber_count=sub_count if isinstance(sub_count, int) else None,
                                    subscriber_count_str=self._format_count(sub_count) if sub_count else None,
                                    description=entry.get("description", "")[:100] if entry.get("description") else None,
                                ))
                
                # Optimization: Only fetch detailed sub counts for top 5 results to keep search fast (< 5s)
                # and reuse the ydl instance if possible (but _get_channel_details creates its own)
                # Modern yt-dlp often gets subscriber_count in the search result for most major channels
                for channel in channels[:5]:
                    if channel.subscriber_count is None:
                        details = self._get_channel_details(channel.id)
                        if details:
                            channel.subscriber_count = details.get("subs", 0)
                            channel.subscriber_count_str = self._format_count(details.get("subs"))
                
                channels.sort(key=lambda c: c.subscriber_count or 0, reverse=True)
                return channels[:max_results]
            except Exception:
                return []

    def _get_channel_details(self, channel_id: str) -> Optional[dict]:
        """Fetch detailed channel info including subscriber count."""
        channel_url = f"https://www.youtube.com/channel/{channel_id}"
        opts = {
            "quiet": True,
            "no_warnings": True,
            "extract_flat": True,
            "playlist_items": "0",
        }
        
        try:
            with yt_dlp.YoutubeDL(opts) as ydl:
                info = ydl.extract_info(channel_url, download=False)
                if info:
                    return {
                        "subs": info.get("channel_follower_count") or info.get("follower_count") or 0,
                        "name": info.get("channel") or info.get("uploader"),
                    }
        except Exception:
            pass
        return None

    def _format_count(self, count: Optional[int]) -> str:
        """Format a number as human readable (e.g., 1.2M)."""
        if not count:
            return "N/A"
        if count >= 1_000_000:
            return f"{count / 1_000_000:.1f}M"
        if count >= 1_000:
            return f"{count / 1_000:.1f}K"
        return str(count)

    def get_channel_videos(self, channel_url: str, max_videos: int = 50) -> list[VideoInfo]:
        """Get videos from a YouTube channel, sorted by most recent."""
        opts = {
            **self._ydl_opts,
            "playlistend": max_videos,
        }
        
        with yt_dlp.YoutubeDL(opts) as ydl:
            try:
                result = ydl.extract_info(channel_url, download=False)
                videos = []
                
                if result and "entries" in result:
                    for entry in result["entries"]:
                        if entry:
                            videos.append(VideoInfo(
                                id=entry.get("id", ""),
                                title=entry.get("title", "Unknown"),
                                url=entry.get("url", f"https://www.youtube.com/watch?v={entry.get('id', '')}"),
                                duration=entry.get("duration"),
                                upload_date=entry.get("upload_date"),
                                thumbnail=entry.get("thumbnail"),
                            ))
                
                return videos
            except Exception:
                return []

    def get_channel_playlists(self, channel_id: str) -> list[PlaylistInfo]:
        """Get playlists from a YouTube channel."""
        playlist_url = f"https://www.youtube.com/channel/{channel_id}/playlists"
        
        with yt_dlp.YoutubeDL(self._ydl_opts) as ydl:
            try:
                result = ydl.extract_info(playlist_url, download=False)
                playlists = []
                
                if result and "entries" in result:
                    for entry in result["entries"]:
                        if entry:
                            playlists.append(PlaylistInfo(
                                id=entry.get("id", ""),
                                title=entry.get("title", "Unknown"),
                                url=entry.get("url", f"https://www.youtube.com/playlist?list={entry.get('id', '')}"),
                                video_count=entry.get("playlist_count"),
                            ))
                
                return playlists
            except Exception:
                return []

    def get_playlist_videos(self, playlist_url: str, max_videos: int = 100) -> list[VideoInfo]:
        """Get videos from a playlist."""
        opts = {
            **self._ydl_opts,
            "playlistend": max_videos,
        }
        
        with yt_dlp.YoutubeDL(opts) as ydl:
            try:
                result = ydl.extract_info(playlist_url, download=False)
                videos = []
                
                if result and "entries" in result:
                    for entry in result["entries"]:
                        if entry:
                            videos.append(VideoInfo(
                                id=entry.get("id", ""),
                                title=entry.get("title", "Unknown"),
                                url=f"https://www.youtube.com/watch?v={entry.get('id', '')}",
                                duration=entry.get("duration"),
                            ))
                
                return videos
            except Exception:
                return []

    def get_video_info(self, video_url: str) -> Optional[VideoInfo]:
        """Get detailed info for a single video."""
        opts = {
            "quiet": True,
            "no_warnings": True,
        }
        
        with yt_dlp.YoutubeDL(opts) as ydl:
            try:
                result = ydl.extract_info(video_url, download=False)
                if result:
                    return VideoInfo(
                        id=result.get("id", ""),
                        title=result.get("title", "Unknown"),
                        url=video_url,
                        duration=result.get("duration"),
                        upload_date=result.get("upload_date"),
                        thumbnail=result.get("thumbnail"),
                    )
            except Exception:
                pass
        return None

    def get_playlist_metadata(self, playlist_url: str) -> Optional[tuple[str, str]]:
        """Fetch metadata (title, uploader) for a playlist URL."""
        opts = {
            "quiet": True,
            "no_warnings": True,
            "extract_flat": True,
        }
        with yt_dlp.YoutubeDL(opts) as ydl:
            try:
                info = ydl.extract_info(playlist_url, download=False)
                if info:
                    title = info.get("title", "Unknown Playlist")
                    uploader = info.get("uploader", info.get("channel", "YouTube"))
                    return title, uploader
            except Exception:
                pass
        return None
