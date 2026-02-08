"""Download screen showing progress and queue."""

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

    #download-status {
        width: 100%;
        height: auto;
        padding: 1 2;
        border: round $secondary;
        background: $surface-darken-1;
        margin-bottom: 1;
    }

    #current-video {
        text-style: bold;
        margin-bottom: 1;
    }

    #progress-bar {
        width: 100%;
        margin-bottom: 1;
    }

    #progress-info {
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
        self._current_video = ""
        self._videos_downloaded = 0

    def compose(self) -> ComposeResult:
        """Create the download screen layout."""
        with Container(id="download-container"):
            with Vertical(id="download-header"):
                yield Label(f"📺 {self.channel.name}", id="channel-title")
                yield Label(
                    "Downloading videos to ~/Downloads/videos/",
                    id="channel-subtitle",
                )
            
            with Vertical(id="download-status"):
                yield Label("Preparing...", id="current-video")
                yield ProgressBar(id="progress-bar", total=100, show_eta=False)
                yield Label("", id="progress-info")
            
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
        """Update the progress display."""
        video_label = self.query_one("#current-video", Label)
        progress_bar = self.query_one("#progress-bar", ProgressBar)
        progress_info = self.query_one("#progress-info", Label)
        
        if progress.video_title != self._current_video:
            self._current_video = progress.video_title
            video_label.update(f"🎬 {progress.video_title}")
        
        progress_bar.progress = progress.percent
        
        if progress.status == "downloading":
            info_parts = [f"{progress.percent:.1f}%"]
            if progress.speed:
                info_parts.append(progress.speed)
            if progress.eta:
                info_parts.append(f"ETA: {progress.eta}")
            progress_info.update(" • ".join(info_parts))
        elif progress.status == "processing":
            progress_info.update("Processing...")
        elif progress.status == "starting":
            progress_info.update("Starting download...")

    def log_message(self, message: str, level: str = "info") -> None:
        """Add a message to the download log."""
        log = self.query_one("#download-log", RichLog)
        
        if level == "success":
            log.write(f"[green]{message}[/green]")
        elif level == "error":
            log.write(f"[red]{message}[/red]")
        else:
            log.write(f"[dim]{message}[/dim]")

    def on_download_complete(self, video_title: str) -> None:
        """Handle completed download."""
        self._videos_downloaded += 1
        self.log_message(f"✅ Downloaded: {video_title}", "success")

    def on_download_error(self, video_title: str, error: str) -> None:
        """Handle download error."""
        self.log_message(f"❌ Failed: {video_title} - {error}", "error")

    def on_queue_complete(self) -> None:
        """Handle when all downloads are done."""
        self.log_message(
            f"🎉 All done! Downloaded {self._videos_downloaded} videos",
            "success",
        )
        video_label = self.query_one("#current-video", Label)
        video_label.update("✓ All videos downloaded!")
        progress_info = self.query_one("#progress-info", Label)
        progress_info.update("Press 'Stop & Exit' to close")
