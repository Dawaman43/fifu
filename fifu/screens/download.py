"""Download screen showing progress and queue."""

import asyncio
from textual.app import ComposeResult
from textual.containers import Container, Vertical, VerticalScroll
from textual.screen import Screen
from textual.widgets import Button, Label, ProgressBar, RichLog

from fifu.services.youtube import ChannelInfo
from fifu.services.downloader import DownloadProgress


class DownloadScreen(Screen):
    """Screen for displaying download progress."""

    CSS = """
    #download-container {
        width: 100%;
        height: 100%;
        padding: 1 2;
    }

    #download-header {
        width: 100%;
        height: auto;
        margin-bottom: 1;
    }

    #channel-title {
        text-style: bold;
        color: $primary;
    }

    #channel-subtitle {
        color: $text-muted;
    }

    #total-status {
        width: 100%;
        height: auto;
        padding: 1 2;
        border: round $primary;
        background: $surface-darken-1;
        margin-bottom: 1;
    }

    #active-downloads {
        width: 100%;
        height: auto;
        max-height: 10;
        margin-bottom: 1;
    }

    .video-progress-item {
        margin-bottom: 1;
        padding: 0 1;
        border-left: double $secondary;
    }

    .video-title {
        text-style: bold;
    }

    .video-info {
        color: $text-muted;
    }

    #download-log {
        width: 100%;
        height: 1fr;
        border: round $primary;
        background: $surface-darken-1;
    }

    #download-footer {
        width: 100%;
        height: auto;
        margin-top: 1;
    }

    #stop-button {
        width: auto;
    }
    """

    def __init__(self, channel: ChannelInfo):
        super().__init__()
        self.channel = channel
        self._videos_downloaded = 0
        self._total_videos = 0
        self._active_downloads: dict[str, Vertical] = {}
        self._active_percents: dict[str, float] = {}

    def compose(self) -> ComposeResult:
        """Create the download screen layout."""
        with Container(id="download-container"):
            with Vertical(id="download-header"):
                yield Label(f"📺 {self.channel.name}", id="channel-title")
                yield Label(
                    "Downloading videos to ~/Downloads/videos/",
                    id="channel-subtitle",
                )
            
            with VerticalScroll(id="active-downloads"):
                # Active download widgets will be added here dynamically
                pass
            
            yield RichLog(id="download-log", highlight=True, markup=True)
            
            with Container(id="download-footer"):
                yield Button("⏹ Stop & Exit", id="stop-button", variant="error")

    def on_mount(self) -> None:
        """Start downloading when screen mounts."""
        self.log_message("🚀 Starting download queue...", "info")
        self.app.start_downloads(self.channel)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle stop button."""
        if event.button.id == "stop-button":
            self.app.stop_downloads()
            self.app.exit()

    def update_progress(self, progress: DownloadProgress) -> None:
        """Update the progress display for a specific video."""
        video_id = progress.video_title # Using title as ID for now
        active_container = self.query_one("#active-downloads", VerticalScroll)

        if video_id not in self._active_downloads:
            # Create new progress widget for this video
            # Note: We pass children to constructor to avoid "mount before parent mounted" error
            # Also use abs(hash) to ensure valid ID format
            safe_id = f"dl_{abs(hash(video_id))}"
            new_widget = Vertical(
                Label(f"🎬 {progress.video_title}", classes="video-title"),
                ProgressBar(total=100, show_eta=False),
                Label("Starting...", classes="video-info"),
                classes="video-progress-item",
                id=safe_id
            )
            active_container.mount(new_widget)
            self._active_downloads[video_id] = new_widget
            active_container.scroll_to_widget(new_widget)

        widget = self._active_downloads[video_id]
        pbar = widget.query_one(ProgressBar)
        info = widget.query_one(".video-info", Label)

        pbar.progress = progress.percent
        
        if progress.status == "downloading":
            self._active_percents[video_id] = progress.percent
            info_parts = [f"{progress.percent:.1f}%"]
            if progress.speed:
                info_parts.append(progress.speed)
            if progress.eta:
                info_parts.append(f"ETA: {progress.eta}")
            info.update(" • ".join(info_parts))
        elif progress.status == "finishing":
            self._active_percents[video_id] = 100.0
            info.update("Finishing (merging/cleanup)...")
        elif progress.status == "starting":
            self._active_percents[video_id] = 0.0
            info.update("Starting download...")
        
        self.update_total_progress(self._videos_downloaded, self._total_videos)

    def update_total_progress(self, current: int, total: int) -> None:
        """Update the total queue progress tracking."""
        self._total_videos = total
        self._videos_downloaded = current
        # Overall progress bar removed per user request

    def log_message(self, message: str, level: str = "info") -> None:
        """Add a message to the download log."""
        log = self.query_one("#download-log", RichLog)
        
        if level == "success":
            log.write(f"[green]{message}[/green]")
        elif level == "error":
            log.write(f"[red]{message}[/red]")
        else:
            log.write(f"[dim]{message}[/dim]")

    async def _cleanup_completed_widget(self, video_title: str) -> None:
        """Keep the completed widget visible for a moment then remove."""
        if video_title in self._active_downloads:
            widget = self._active_downloads[video_title]
            info = widget.query_one(".video-info", Label)
            info.update("[green]✓ Download Completed![/green]")
            
            await asyncio.sleep(2)
            
            if video_title in self._active_downloads:
                widget = self._active_downloads.pop(video_title)
                widget.remove()

    def on_download_complete(self, video_title: str) -> None:
        """Handle completed download."""
        self.app.run_worker(self._cleanup_completed_widget(video_title))
        
        if video_title in self._active_percents:
             self._active_percents.pop(video_title)

        self._videos_downloaded += 1
        self.log_message(f"✅ Downloaded: {video_title}", "success")
        self.update_total_progress(self._videos_downloaded, self._total_videos)

    def on_download_error(self, video_title: str, error: str) -> None:
        """Handle download error."""
        if video_title in self._active_downloads:
            widget = self._active_downloads.pop(video_title)
            widget.remove()
        
        if video_title in self._active_percents:
            self._active_percents.pop(video_title)
            
        self._videos_downloaded += 1 # Still counted as processed
        self.log_message(f"❌ Failed: {video_title} - {error}", "error")
        self.update_total_progress(self._videos_downloaded, self._total_videos)

    def on_queue_complete(self) -> None:
        """Handle when all downloads are done."""
        self.log_message(
            f"🎉 All done! Processed {self._total_videos} videos",
            "success",
        )
