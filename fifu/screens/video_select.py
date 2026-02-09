"""Screen for manually selecting videos to download."""

from textual.app import ComposeResult
from textual.containers import Container, Vertical, Horizontal, VerticalScroll
from textual.screen import Screen
from textual.widgets import Button, Input, Label, Checkbox, Header, Footer
from textual.binding import Binding

from fifu.services.youtube import VideoInfo


class VideoSelectScreen(Screen):
    """Screen for selecting specific videos from a channel or playlist."""

    CSS_PATH = "../styles/app.tcss"
    
    BINDINGS = [
        Binding("escape", "go_back", "Back"),
    ]

    def __init__(self, videos: list[VideoInfo]):
        super().__init__()
        self.all_videos = videos
        self.filtered_videos = videos
        self.selected_urls = set()  # Track selected video URLs
        self.filter_query = ""

    def compose(self) -> ComposeResult:
        """Create the video selection layout."""
        with Container(id="video-select-container"):
            yield Label("Select Videos to Download", id="video-select-title")
            
            # Search/Filter section
            yield Input(placeholder="Search videos...", id="video-filter-input")
            
            with Horizontal(id="selection-controls"):
                yield Button("Select All", id="select-all-btn", variant="primary", classes="control-btn")
                yield Button("Deselect All", id="deselect-all-btn", variant="error", classes="control-btn")
                yield Label(f"Selected: 0/{len(self.all_videos)}", id="selection-count")

            # Video list
            with VerticalScroll(id="video-list-scroll"):
                with Vertical(id="video-list"):
                    # Items will be added dynamically
                    pass

            # Footer actions
            with Horizontal(id="video-select-actions"):
                yield Button("Confirm Selection", id="confirm-selection-btn", variant="success")
                yield Button("Back", id="back-btn", variant="default")

    def on_mount(self) -> None:
        """Populate the list on mount."""
        self._populate_list()
        self._update_selection_count()

    def _populate_list(self) -> None:
        """Populate the video list based on current filter."""
        video_list = self.query_one("#video-list", Vertical)
        video_list.remove_children()
        
        checkboxes = []
        for video in self.filtered_videos:
            is_checked = video.url in self.selected_urls
            checkbox = Checkbox(
                f"{video.title} ({self._format_duration(video.duration)})", 
                value=is_checked
            )
            checkbox.video_info = video
            checkboxes.append(checkbox)
            
        if checkboxes:
            video_list.mount_all(checkboxes)

    def _format_duration(self, seconds: float | int | None) -> str:
        """Format seconds into MM:SS or HH:MM:SS."""
        if not seconds:
            return "N/A"
        
        seconds = int(seconds)
        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)
        if h > 0:
            return f"{h}:{m:02d}:{s:02d}"
        return f"{m}:{s:02d}"

    def on_input_changed(self, event: Input.Changed) -> None:
        """Handle search input changes."""
        if event.input.id == "video-filter-input":
            self.filter_query = event.value.lower()
            if self.filter_query:
                self.filtered_videos = [
                    v for v in self.all_videos 
                    if self.filter_query in v.title.lower()
                ]
            else:
                self.filtered_videos = self.all_videos
            
            self._populate_list()

    def on_checkbox_changed(self, event: Checkbox.Changed) -> None:
        """Handle individual video selection."""
        video = getattr(event.checkbox, "video_info", None)
        if video:
            if event.value:
                self.selected_urls.add(video.url)
            else:
                self.selected_urls.discard(video.url)
            self._update_selection_count()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        if event.button.id == "select-all-btn":
            self._select_all_visible(True)
        elif event.button.id == "deselect-all-btn":
            self._select_all_visible(False)
        elif event.button.id == "confirm-selection-btn":
            self._fullfil_selection()
        elif event.button.id == "back-btn" or event.button.id == "go_back":
            self.action_go_back()

    def action_go_back(self) -> None:
        """Return to previous screen."""
        self.app.pop_screen()

    def _select_all_visible(self, select: bool) -> None:
        """Select or deselect all currently visible (filtered) videos."""
        video_list = self.query_one("#video-list", Vertical)
        for checkbox in video_list.children:
            if isinstance(checkbox, Checkbox):
                checkbox.value = select
                # Event handler will update self.selected_urls

    def _update_selection_count(self) -> None:
        """Update the selection count label."""
        count_label = self.query_one("#selection-count", Label)
        count_label.update(f"Selected: {len(self.selected_urls)}/{len(self.all_videos)}")

    def _fullfil_selection(self) -> None:
        """Collect selected videos and call app method."""
        selected_videos = [v for v in self.all_videos if v.url in self.selected_urls]
        if not selected_videos:
            self.app.notify("No videos selected!", severity="warning")
            return
            
        self.app.on_video_selection_confirmed(selected_videos)
