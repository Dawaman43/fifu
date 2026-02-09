"""Search screen for channel name input."""

from textual.app import ComposeResult
from textual.containers import Container, Vertical
from textual.screen import Screen
from textual.widgets import Button, Input, Label, LoadingIndicator


class SearchScreen(Screen):
    """Screen for searching YouTube channels."""

    CSS = """
    #search-container {
        width: 100%;
        height: 100%;
        align: center middle;
    }

    #search-box {
        width: 60;
        height: auto;
        padding: 2 4;
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
        font-size: 70%;
        margin-bottom: 2;
    }

    .shoutout-link {
        color: $accent;
        text-style: italic;
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

    def on_mount(self) -> None:
        """Focus the input when screen mounts."""
        self.query_one("#search-input", Input).focus()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle search button press."""
        if event.button.id == "search-button":
            self._do_search()

    def on_input_submitted(self, event: Input.Submitted) -> None:
        """Handle enter key in input."""
        if event.input.id == "search-input":
            self._do_search()

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
        self.query_one("#search-button").display = True
        status = self.query_one("#search-status", Label)
        status.update(f"❌ {message}")

    def show_searching(self) -> None:
        """Show searching status."""
        self.query_one("#search-button").display = False
        self.query_one("#loading").display = True
        status = self.query_one("#search-status", Label)
        status.update("🔍 Searching...")
