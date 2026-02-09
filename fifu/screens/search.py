"""Search screen for channel name input."""

from textual.app import ComposeResult
from textual.containers import Container, Vertical, Horizontal
from textual.screen import Screen
from textual.widgets import Button, Input, Label, LoadingIndicator, ListItem, ListView
from fifu.services.youtube import ChannelInfo


class SearchScreen(Screen):
    """Screen for searching YouTube channels."""

    CSS = """
    #search-container {
        width: 100%;
        height: 100%;
        align: center middle;
    }

    #search-box {
        width: 70;
        height: auto;
        padding: 1 2;
        border: round $primary;
        background: $surface-darken-1;
    }

    #search-title {
        width: 100%;
        text-align: center;
        text-style: bold;
        color: $primary;
        margin-bottom: 1;
    }

    #search-subtitle {
        width: 100%;
        text-align: center;
        color: $text-muted;
        margin-bottom: 2;
    }

    #search-input {
        width: 100%;
        margin-bottom: 1;
    }

    #search-button {
        width: 100%;
        margin-top: 1;
    }

    #search-status {
        width: 100%;
        text-align: center;
        color: $warning;
        margin-top: 1;
        height: 3;
    }

    #loading {
        width: 100%;
        height: 3;
        margin-top: 1;
        display: none;
    }

    #shoutouts {
        width: 100%;
        text-align: center;
        color: $text-muted;
        margin-bottom: 1;
    }

    .shoutout-link {
        color: $accent;
        text-style: italic;
    }

    #lists-container {
        width: 100%;
        height: auto;
        margin-top: 1;
    }

    .list-section {
        width: 1fr;
        height: auto;
        padding: 0 1;
    }

    .section-title {
        text-style: bold;
        color: $primary;
        margin-bottom: 1;
    }

    #history-list, #favorites-list {
        background: $surface;
        border: none;
        height: auto;
        min-height: 3;
        max-height: 8;
    }

    ListItem {
        padding: 0 1;
    }

    ListItem:hover {
        background: $accent 20%;
    }
    """

    def compose(self) -> ComposeResult:
        """Create the search screen layout."""
        with Container(id="search-container"):
            with Vertical(id="search-box"):
                yield Label("🎬 FIFU", id="search-title")
                yield Label("YouTube Channel or Playlist Downloader", id="search-subtitle")
                yield Label(
                    "Shout out to [b]The PrimeTime[/b] & [b]Devtopia[/b] ⚡", 
                    id="shoutouts"
                )
                yield Input(
                    placeholder="Enter channel name or paste playlist URL...",
                    id="search-input",
                )
                yield Button("Search / Process URL", id="search-button", variant="primary")
                yield LoadingIndicator(id="loading")
                yield Label("", id="search-status")

                with Horizontal(id="lists-container"):
                    with Vertical(classes="list-section"):
                        yield Label(" Recent", classes="section-title")
                        yield ListView(id="history-list")
                    
                    with Vertical(classes="list-section"):
                        yield Label("⭐ Favorites", classes="section-title")
                        yield ListView(id="favorites-list")

    def on_mount(self) -> None:
        """Initialize the screen."""
        self.query_one("#search-input", Input).focus()
        self._refresh_lists()

    def on_screen_resume(self) -> None:
        """Refresh lists when returning to this screen."""
        self._refresh_lists()

    def _refresh_lists(self) -> None:
        """Reload history and favorites from config."""
        history_list = self.query_one("#history-list", ListView)
        fav_list = self.query_one("#favorites-list", ListView)
        
        history_list.clear()
        for item in self.app.config_service.get_history():
            li = ListItem(Label(item))
            li.history_query = item  # Store original query safely
            history_list.append(li)
            
        fav_list.clear()
        for fav in self.app.config_service.get_favorites():
            fav_list.append(ListItem(
                Label(f"📺 {fav['name']} ({fav.get('sub_count_str', 'N/A')})"), 
                id=f"fav-{fav['id']}"
            ))

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle search button press."""
        if event.button.id == "search-button":
            self._do_search()

    def on_input_submitted(self, event: Input.Submitted) -> None:
        """Handle enter key in input."""
        if event.input.id == "search-input":
            self._do_search()

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        """Handle selection in history or favorites."""
        item = event.item
        if hasattr(item, "history_query"):
            query = item.history_query
            self.query_one("#search-input", Input).value = query
            self._do_search()
        elif item.id and item.id.startswith("fav-"):
            channel_id = item.id[4:]
            favorites = self.app.config_service.get_favorites()
            fav = next((f for f in favorites if f["id"] == channel_id), None)
            if fav:
                channel = ChannelInfo(
                    id=fav["id"],
                    name=fav["name"],
                    url=fav["url"]
                )
                self.app.select_channel(channel)

    def _do_search(self) -> None:
        """Perform the channel search."""
        input_widget = self.query_one("#search-input", Input)
        query = input_widget.value.strip()
        
        if not query:
            status = self.query_one("#search-status", Label)
            status.update("Please enter a channel name")
            return
        
        status = self.query_one("#search-status", Label)
        status.update("Searching...")
        
        self.app.search_channels(query)

    def show_error(self, message: str) -> None:
        """Display an error message."""
        self.query_one("#loading").display = False
        try:
            self.query_one("#search-button").display = True
        except Exception:
            pass
        status = self.query_one("#search-status", Label)
        status.update(f"❌ {message}")

    def show_searching(self) -> None:
        """Show searching status."""
        try:
            self.query_one("#search-button").display = False
        except Exception:
            pass
        self.query_one("#loading").display = True
        status = self.query_one("#search-status", Label)
        status.update("🔍 Searching...")
