"""Service for managing persistent configuration and history."""

import json
from pathlib import Path
from typing import Any


class ConfigService:
    """Manages application configuration, history, and favorites."""

    def __init__(self):
        self.config_dir = Path.home() / ".config" / "fifu"
        self.config_file = self.config_dir / "data.json"
        self._data = {
            "history": [],
            "favorites": []
        }
        self._load()

    def _load(self) -> None:
        """Load data from JSON file."""
        if self.config_file.exists():
            try:
                with open(self.config_file, "r") as f:
                    loaded_data = json.load(f)
                    # Merge with defaults to handle schema changes
                    self._data.update(loaded_data)
            except Exception:
                pass

    def _save(self) -> None:
        """Save data to JSON file."""
        self.config_dir.mkdir(parents=True, exist_ok=True)
        try:
            with open(self.config_file, "w") as f:
                json.dump(self._data, f, indent=4)
        except Exception:
            pass

    def get_history(self) -> list[str]:
        """Get search history."""
        return self._data.get("history", [])

    def add_history(self, query: str) -> None:
        """Add a query to history, ensuring unique and limited to 10 items."""
        if not query:
            return
            
        history = self.get_history()
        # Remove if already exists to move to top
        if query in history:
            history.remove(query)
            
        history.insert(0, query)
        self._data["history"] = history[:10]
        self._save()

    def clear_history(self) -> None:
        """Clear search history."""
        self._data["history"] = []
        self._save()

    def get_favorites(self) -> list[dict[str, Any]]:
        """Get favorite channels."""
        return self._data.get("favorites", [])

    def is_favorite(self, channel_id: str) -> bool:
        """Check if a channel is in favorites."""
        return any(f.get("id") == channel_id for f in self.get_favorites())

    def toggle_favorite(self, channel_info_dict: dict[str, Any]) -> bool:
        """Add/remove channel from favorites. Returns True if now a favorite."""
        favorites = self.get_favorites()
        channel_id = channel_info_dict.get("id")
        
        existing = next((f for f in favorites if f.get("id") == channel_id), None)
        
        if existing:
            favorites.remove(existing)
            result = False
        else:
            favorites.insert(0, channel_info_dict)
            result = True
            
        self._data["favorites"] = favorites
        self._save()
        return result
