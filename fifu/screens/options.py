"""Download options screen for video count and quality selection."""

from textual.app import ComposeResult
from textual.containers import Container, Vertical, Horizontal, VerticalScroll
from textual.screen import Screen
from textual.widgets import Button, Input, Label, Select, RadioSet, RadioButton, Checkbox

from fifu.services.youtube import ChannelInfo, PlaylistInfo


QUALITY_OPTIONS = [
    ("Best Quality", "best"),
    ("1080p", "bestvideo[height<=1080]+bestaudio/best[height<=1080]"),
    ("720p", "bestvideo[height<=720]+bestaudio/best[height<=720]"),
    ("480p", "bestvideo[height<=480]+bestaudio/best[height<=480]"),
    ("Audio Only", "bestaudio/best"),
]


class OptionsScreen(Screen):
    """Screen for download options: count, quality, playlist."""

    CSS = """
    #options-container {
        width: 100%;
        height: 100%;
        align: center middle;
        overflow: auto;
    }

    #options-scroll {
        width: 80;
        max-height: 80vh;
        border: round $primary;
        background: $surface-darken-1;
    }

    #options-box {
        width: 100%;
        height: auto;
        padding: 1 4;
    }

    #options-title {
        width: 100%;
        text-align: center;
        text-style: bold;
        color: $primary;
        margin-bottom: 1;
    }

    #channel-name {
        width: 100%;
        text-align: center;
        color: $text-muted;
        margin-bottom: 2;
    }

    .option-label {
        margin-top: 1;
        margin-bottom: 0;
        color: $text;
    }

    #video-count-input {
        width: 100%;
        margin-bottom: 1;
    }

    #quality-select {
        width: 100%;
        margin-bottom: 1;
    }

    #playlist-section {
        margin-top: 1;
        margin-bottom: 1;
    }

    #playlist-select {
        width: 100%;
    }

    #button-row {
        margin-top: 1;
        padding: 1 4 2 4;
        width: 80;
        background: $surface-darken-1;
        border-right: round $primary;
        border-left: round $primary;
        border-bottom: round $primary;
        align: center middle;
    }

    #start-button {
        margin-right: 2;
    }

    #back-button {
        margin-left: 2;
    }

    RadioSet {
        width: 100%;
        height: auto;
        margin-bottom: 1;
    }
    """

    def __init__(self, channel: ChannelInfo, playlists: list[PlaylistInfo] = None):
        super().__init__()
        self.channel = channel
        self.playlists = playlists or []
        self.selected_quality = "best"
        self.video_count = "all"
        self.selected_playlist = None
        self.download_subtitles = False

    def compose(self) -> ComposeResult:
        """Create the options screen layout."""
        with Container(id="options-container"):
            with VerticalScroll(id="options-scroll"):
                with Vertical(id="options-box"):
                    yield Label("⚙️ Download Options", id="options-title")
                    yield Label(f"📺 {self.channel.name}", id="channel-name")
                    
                    yield Label("How many videos?", classes="option-label")
                    yield Input(
                        placeholder="Enter number or 'all'",
                        value="all",
                        id="video-count-input",
                    )
                    
                    yield Label("Video Quality", classes="option-label")
                    yield Select(
                        [(name, value) for name, value in QUALITY_OPTIONS],
                        value="best",
                        id="quality-select",
                    )
                    
                    yield Label("Additional Options", classes="option-label")
                    yield Checkbox("Download & Embed Subtitles", id="subtitles-check")
                    
                    yield Label("Download from Playlist (optional)", classes="option-label")
                    if self.playlists:
                        playlist_options = [("📹 Channel Videos (default)", None)]
                        playlist_options.extend([(f"📋 {p.title}", p.url) for p in self.playlists])
                        yield Select(
                            playlist_options,
                            value=None,
                            id="playlist-select",
                        )
                    else:
                        yield Label("No playlists found - downloading from channel videos", id="no-playlists")
            
            with Horizontal(id="button-row"):
                yield Button("▶ Start Download", id="start-button", variant="success")
                yield Button("← Back", id="back-button", variant="default")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        if event.button.id == "start-button":
            self._start_download()
        elif event.button.id == "back-button":
            self.app.pop_screen()

    def on_select_changed(self, event: Select.Changed) -> None:
        """Handle select changes."""
        if event.select.id == "quality-select":
            self.selected_quality = event.value
        elif event.select.id == "playlist-select":
            self.selected_playlist = event.value

    def on_checkbox_changed(self, event: Checkbox.Changed) -> None:
        """Handle checkbox changes."""
        if event.checkbox.id == "subtitles-check":
            self.download_subtitles = event.value

    def on_input_changed(self, event: Input.Changed) -> None:
        """Handle input changes."""
        if event.input.id == "video-count-input":
            self.video_count = event.value

    def _start_download(self) -> None:
        """Start the download with selected options."""
        count_input = self.query_one("#video-count-input", Input)
        count_str = count_input.value.strip().lower()
        
        if count_str == "all":
            max_videos = 9999
        else:
            try:
                max_videos = int(count_str)
            except ValueError:
                max_videos = 10
        
        quality_select = self.query_one("#quality-select", Select)
        quality = quality_select.value
        
        playlist_url = None
        if self.playlists:
            try:
                playlist_select = self.query_one("#playlist-select", Select)
                playlist_url = playlist_select.value
            except Exception:
                pass
        
        subtitles = self.query_one("#subtitles-check", Checkbox).value
        
        self.app.start_download_with_options(
            channel=self.channel,
            max_videos=max_videos,
            quality=quality,
            playlist_url=playlist_url,
            subtitles=subtitles
        )
