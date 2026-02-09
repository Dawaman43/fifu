"""Channels list screen for selecting a channel."""

from textual.app import ComposeResult
from textual.containers import Container, Vertical
from textual.screen import Screen
from textual.widgets import Button, Label, ListItem, ListView, Static

from fifu.services.youtube import ChannelInfo


class ChannelListItem(ListItem):
    """A list item representing a YouTube channel."""

    def __init__(self, channel: ChannelInfo, index: int):
        super().__init__()
        self.channel = channel
        self.index = index

    def compose(self) -> ComposeResult:
        """Create the channel item layout."""
        with Vertical(classes="channel-item"):
            subs = self.channel.subscriber_count_str or "N/A"
            yield Label(
                f"#{self.index + 1}  📺 {self.channel.name}  •  {subs} subs",
                classes="channel-name",
            )
            if self.channel.description:
                yield Label(
                    self.channel.description[:80] + "...",
                    classes="channel-info",
                )


class ChannelsScreen(Screen):
    """Screen for displaying and selecting channels."""

    CSS = """
    #channels-container {
        width: 100%;
        height: 100%;
        padding: 1 2;
    }

    #channels-header {
        width: 100%;
        height: auto;
        padding: 1;
        margin-bottom: 1;
    }

    #channels-title {
        text-style: bold;
        color: $primary;
    }

    #channels-subtitle {
        color: $text-muted;
    }

    #channels-list {
        width: 100%;
        height: 1fr;
        border: round $primary;
        background: $surface-darken-1;
    }

    .channel-item {
        padding: 1 2;
    }

    .channel-name {
        text-style: bold;
    }

    .channel-info {
        color: $text-muted;
    }

    #footer-row {
        width: 100%;
        height: auto;
        margin-top: 1;
    }

    #back-button {
        width: auto;
    }

    #page-info {
        color: $text-muted;
        margin-left: 2;
    }

    ChannelListItem {
        height: auto;
    }

    ChannelListItem:hover {
        background: $primary 20%;
    }

    ChannelListItem.-highlight {
        background: $primary 40%;
    }
    """

    BINDINGS = [
        ("pageup", "prev_page", "Previous"),
        ("pagedown", "next_page", "Next"),
        ("f", "toggle_favorite", "Favorite"),
    ]

    def __init__(self, channels: list[ChannelInfo], search_query: str):
        super().__init__()
        self.channels = channels
        self.search_query = search_query
        self.page_size = 10
        self.current_page = 0
        self.total_pages = max(1, (len(channels) + self.page_size - 1) // self.page_size)

    def compose(self) -> ComposeResult:
        """Create the channels screen layout."""
        with Container(id="channels-container"):
            with Vertical(id="channels-header"):
                yield Label(
                    f"🔍 Results for \"{self.search_query}\" (sorted by subscribers)",
                    id="channels-title",
                )
                yield Label(
                    f"Found {len(self.channels)} channels • Use PageUp/PageDown to navigate",
                    id="channels-subtitle",
                )
            yield ListView(id="channels-list")
            with Vertical(id="footer-row"):
                yield Label("", id="page-info")
                yield Button("← Back to Search", id="back-button", variant="default")

    def on_mount(self) -> None:
        """Load first page when screen mounts."""
        self._load_page()
        list_view = self.query_one("#channels-list", ListView)
        list_view.focus()

    def _load_page(self) -> None:
        """Load the current page of channels."""
        list_view = self.query_one("#channels-list", ListView)
        list_view.clear()
        
        start = self.current_page * self.page_size
        end = min(start + self.page_size, len(self.channels))
        
        for i, channel in enumerate(self.channels[start:end]):
            list_view.append(ChannelListItem(channel, start + i))
        
        page_info = self.query_one("#page-info", Label)
        page_info.update(f"Page {self.current_page + 1} of {self.total_pages}")

    def action_next_page(self) -> None:
        """Go to next page."""
        if self.current_page < self.total_pages - 1:
            self.current_page += 1
            self._load_page()

    def action_prev_page(self) -> None:
        """Go to previous page."""
        if self.current_page > 0:
            self.current_page -= 1
            self._load_page()

    def action_toggle_favorite(self) -> None:
        """Toggle favorite status for selected channel."""
        list_view = self.query_one("#channels-list", ListView)
        if list_view.index is not None:
            # Calculate actual index in channels list based on page
            actual_index = self.current_page * self.page_size + list_view.index
            if actual_index < len(self.channels):
                channel = self.channels[actual_index]
                is_fav = self.app.toggle_favorite(channel)
                status = "added to" if is_fav else "removed from"
                self.notify(f"'{channel.name}' {status} favorites")

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        """Handle channel selection."""
        if isinstance(event.item, ChannelListItem):
            self.app.select_channel(event.item.channel)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle back button."""
        if event.button.id == "back-button":
            self.app.pop_screen()
