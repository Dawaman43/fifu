# Fifu

A cross-platform TUI for downloading YouTube videos from channels.

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Textual](https://img.shields.io/badge/TUI-Textual-green)
![yt-dlp](https://img.shields.io/badge/Download-yt--dlp-red)

## Features

- 🔍 **Search YouTube channels** - Find channels by name
- 📊 **Sorted by subscribers** - Most popular channels shown first
- 📄 **Pagination** - Browse through all search results
- ⚙️ **Quality selection** - Choose 1080p, 720p, 480p, or audio only
- 🔢 **Video count** - Download all or a specific number of videos
- 📋 **Playlist support** - Download from channel playlists
- ⬇️ **Auto-download** - Continuously downloads latest videos
- 💾 **Organized storage** - Saves to `~/Downloads/videos/{channelname}/`

## Installation

```bash
cd /path/to/fifu
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

## Usage

```bash
fifu
```

### Workflow

1. **Search** - Enter a channel name
2. **Select** - Choose a channel from results (sorted by subscribers)
3. **Configure** - Set video count, quality, and optionally select a playlist
4. **Download** - Watch videos download automatically

### Controls

| Key           | Action           |
| ------------- | ---------------- |
| `Enter`       | Select / Confirm |
| `PageUp/Down` | Navigate pages   |
| `Escape`      | Go back          |
| `q`           | Quit             |

## Screenshots

```
┌─────────────────────────────────────────────┐
│              🎬 FIFU                        │
│    YouTube Channel Video Downloader         │
│                                             │
│    Enter channel name...                    │
│    [Search Channels]                        │
└─────────────────────────────────────────────┘
```

## License

MIT
