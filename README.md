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

### Standalone Binaries & Native Packages (Recommended)

You can download the latest standalone binaries and native Linux packages from the **[Releases](https://github.com/Dawaman43/fifu/releases)** page.

### Package Managers

If you have Python 3.10+ installed, you can use:

#### PyPI

```bash
pip install fifu
```

#### npm

```bash
npm install -g fifu-tui
```

#### Linux Distributions:

- **Mint / Ubuntu / Debian**: Download and install the `.deb` package.
  ```bash
  sudo dpkg -i fifu.deb
  ```
- **Fedora / RHEL**: Download and install the `.rpm` package.
  ```bash
  sudo rpm -i fifu.rpm
  ```
- **Arch / Generic Linux**: Download the `.tar.gz`, extract it, and run the `fifu` binary.
  ```bash
  tar -xzvf fifu-linux-x64.tar.gz
  ./fifu
  ```

#### Windows:

- Download the `fifu-win.exe` and run it.

#### macOS:

- Download the `fifu-macos`, make it executable, and run it.
  ```bash
  chmod +x fifu-macos
  ./fifu-macos
  ```

### From Source

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
