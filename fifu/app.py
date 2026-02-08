"""Main Fifu Textual application."""

import asyncio
from pathlib import Path
from typing import Optional

from textual.app import App
from textual.binding import Binding

from fifu.screens.search import SearchScreen
from fifu.screens.channels import ChannelsScreen
from fifu.screens.download import DownloadScreen
from fifu.screens.options import OptionsScreen
from fifu.services.youtube import YouTubeService, ChannelInfo, VideoInfo, PlaylistInfo
from fifu.services.downloader import DownloadService, DownloadProgress


class FifuApp(App):
    """Fifu - YouTube Channel Video Downloader TUI."""

    TITLE = "Fifu"
    SUB_TITLE = "YouTube Channel Video Downloader"
    
    CSS_PATH = Path(__file__).parent / "styles" / "app.tcss"
    
    BINDINGS = [
        Binding("q", "quit", "Quit", show=True),
        Binding("escape", "go_back", "Back", show=True),
    ]

    def __init__(self):
        super().__init__()
        self.youtube_service = YouTubeService()
        self.download_service = DownloadService()
        self._download_task: Optional[asyncio.Task] = None
        self._stop_downloads = False
        self._current_channel: Optional[ChannelInfo] = None
        self._videos: list[VideoInfo] = []
        self._download_quality = "best"
        self._max_videos = 9999

    def on_mount(self) -> None:
        """Initialize the application."""
        self.push_screen(SearchScreen())

    def action_go_back(self) -> None:
        """Go back to the previous screen."""
        if len(self.screen_stack) > 1:
            self.pop_screen()

    def search_channels(self, query: str) -> None:
        """Search for channels and display results."""
        self.run_worker(self._search_channels_async(query), exclusive=True)

    async def _search_channels_async(self, query: str) -> None:
        """Async worker to search channels."""
        current_screen = self.screen
        if not isinstance(current_screen, SearchScreen):
            return
        
        current_screen.show_searching()
        
        channels = await asyncio.get_event_loop().run_in_executor(
            None, self.youtube_service.search_channels, query
        )
        
        if not channels:
            current_screen.show_error("No channels found. Try a different search.")
            return
        
        self.push_screen(ChannelsScreen(channels, query))

    def select_channel(self, channel: ChannelInfo) -> None:
        """Handle channel selection - show options screen."""
        self._current_channel = channel
        self.run_worker(self._load_options_screen(channel), exclusive=True)

    async def _load_options_screen(self, channel: ChannelInfo) -> None:
        """Load options screen with playlists."""
        playlists = await asyncio.get_event_loop().run_in_executor(
            None, self.youtube_service.get_channel_playlists, channel.id
        )
        self.push_screen(OptionsScreen(channel, playlists))

    def start_download_with_options(
        self,
        channel: ChannelInfo,
        max_videos: int,
        quality: str,
        playlist_url: Optional[str] = None,
    ) -> None:
        """Start downloads with user-selected options."""
        self._current_channel = channel
        self._max_videos = max_videos
        self._download_quality = quality
        self._playlist_url = playlist_url
        self.push_screen(DownloadScreen(channel))

    def start_downloads(self, channel: ChannelInfo) -> None:
        """Start downloading videos from the channel."""
        self._stop_downloads = False
        self._download_task = asyncio.create_task(self._download_loop(channel))

    async def _download_loop(self, channel: ChannelInfo) -> None:
        """Main download loop."""
        download_screen = self.screen
        if not isinstance(download_screen, DownloadScreen):
            return

        download_screen.log_message(f"📡 Fetching videos from {channel.name}...")
        
        playlist_url = getattr(self, '_playlist_url', None)
        if playlist_url:
            download_screen.log_message(f"📋 Loading playlist...")
            videos = await asyncio.get_event_loop().run_in_executor(
                None, 
                lambda: self.youtube_service.get_playlist_videos(playlist_url, self._max_videos)
            )
        else:
            videos = await asyncio.get_event_loop().run_in_executor(
                None, 
                lambda: self.youtube_service.get_channel_videos(channel.url, self._max_videos)
            )
        
        if not videos:
            download_screen.log_message("No videos found.", "error")
            download_screen.on_queue_complete()
            return
        
        videos = videos[:self._max_videos]
        download_screen.log_message(f"📋 Found {len(videos)} videos to download")
        download_screen.log_message(f"🎬 Quality: {self._download_quality}")
        
        output_dir = self.download_service.get_download_path(channel.name)
        download_screen.log_message(f"📁 Saving to: {output_dir}")
        
        downloaded_titles = self.download_service.get_downloaded_videos(output_dir)
        
        for video in videos:
            if self._stop_downloads:
                download_screen.log_message("⏹ Download stopped by user", "info")
                break
            
            if video.title in downloaded_titles:
                download_screen.log_message(f"⏭ Skipping (already downloaded): {video.title}", "info")
                continue
            
            download_screen.log_message(f"⬇ Starting: {video.title}", "info")
            
            video_url = f"https://www.youtube.com/watch?v={video.id}"
            
            def progress_callback(progress: DownloadProgress):
                self.call_from_thread(download_screen.update_progress, progress)
            
            quality = self._download_quality
            result = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: self.download_service.download_video(
                    video_url, output_dir, progress_callback, quality
                )
            )
            
            if result.success:
                download_screen.on_download_complete(result.video_title)
            else:
                download_screen.on_download_error(
                    result.video_title, result.error or "Unknown error"
                )
        
        download_screen.on_queue_complete()

    def stop_downloads(self) -> None:
        """Stop the download loop."""
        self._stop_downloads = True
        if self._download_task:
            self._download_task.cancel()
