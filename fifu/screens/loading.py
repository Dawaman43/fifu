"""Engaging loading screen with rotating jokes."""

from textual.app import ComposeResult
from textual.containers import Container, Vertical
from textual.screen import Screen
from textual.widgets import Label, LoadingIndicator

from fifu.services.joke import JokeService


class LoadingScreen(Screen):
    """A screen with a loading indicator and rotating jokes."""

    CSS = """
    #loading-container {
        width: 100%;
        height: 100%;
        align: center middle;
        background: $surface-darken-1 80%;
    }

    #loading-box {
        width: 60;
        height: auto;
        padding: 2 4;
        border: round $primary;
        background: $surface;
        align: center middle;
    }

    #loading-message {
        margin-bottom: 1;
        text-style: bold;
    }

    #loading-joke {
        height: auto;
        text-align: center;
        margin-top: 1;
        color: $text-muted;
    }
    """

    def __init__(self, message: str = "Loading..."):
        super().__init__()
        self.message = message
        self._joke_timer = None

    def compose(self) -> ComposeResult:
        """Create the loading screen layout."""
        with Container(id="loading-container"):
            with Vertical(id="loading-box"):
                yield Label(f"⏳ {self.message}", id="loading-message")
                yield LoadingIndicator()
                yield Label(f"[i]{JokeService.get_random_joke()}[/i]", id="loading-joke")

    def on_mount(self) -> None:
        """Start joke rotation on mount."""
        self._joke_timer = self.set_interval(4, self._update_joke)

    def _update_joke(self) -> None:
        """Update the joke in the status label."""
        joke_label = self.query_one("#loading-joke", Label)
        joke_label.update(f"[i]{JokeService.get_random_joke()}[/i]")
