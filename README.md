# 🎬 Fifu

**The Ultra-Fast, Cross-Platform TUI for Downloading YouTube Channel Content.**

[![Build Status](https://github.com/Dawaman43/fifu/actions/workflows/publish.yml/badge.svg)](https://github.com/Dawaman43/fifu/actions) [![PyPI version](https://img.shields.io/pypi/v/fifu.svg)](https://pypi.org/project/fifu/) [![npm version](https://img.shields.io/npm/v/fifu-tui.svg)](https://www.npmjs.com/package/fifu-tui) [![AUR version](https://img.shields.io/aur/version/fifu)](https://aur.archlinux.org/packages/fifu) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) [![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

Fifu (Fetch It For Us) is a high-performance Terminal User Interface (TUI) designed for power users who want to download entire YouTube channels or playlists with zero friction. Built with **Textual** and powered by **yt-dlp**.

---

## ✨ Key Features

- 🚀 **Asynchronous Performance** - Multi-threaded metadata fetching and concurrent downloads (3 at a time).
- 🔍 **Smart Search** - Find any channel instantly, sorted by popularity (subscriber count).
- 📋 **Playlist Intelligence** - Direct support for downloading entire playlists or specific channel sections.
- ⚙️ **Custom Quality Profiles** - 1080p, 720p, 480p, or high-fidelity Audio (MP3/M4A).
- 💬 **Subtitle Support** - Automatically download and embed subtitles into your videos.
- 💾 **Safe History & Favorites** - One-click access to your most-visited channels.
- 🏁 **Graceful UX** - Beautiful progress bars, keyboard-first navigation, and instant shutdown.

---

## 🚀 Quick Start

The fastest way to run Fifu instantly is using **npx**:

```bash
npx fifu-tui
```

Alternatively, you can install it via **pipx**:

```bash
pipx install git+https://github.com/Dawaman43/fifu.git
```

---

## 📦 Installation Options

### 📦 npm (JavaScript Wrapper)

If you prefer using npm, you can install Fifu globally:

```bash
npm install -g fifu-tui
```

### 🐧 Linux

#### Arch Linux (AUR)

```bash
yay -S fifu
```

#### Debian / Ubuntu / Mint

Download the latest `.deb` from [Releases](https://github.com/Dawaman43/fifu/releases) and run:

```bash
sudo dpkg -i fifu.deb
```

#### Fedora / RHEL

Download the latest `.rpm` from [Releases](https://github.com/Dawaman43/fifu/releases) and run:

```bash
sudo rpm -i fifu.rpm
```

### 🪟 Windows

1. Download `fifu-win.exe` from [Releases](https://github.com/Dawaman43/fifu/releases).
2. Run it from your terminal or double-click to start.

### 🍎 macOS

```bash
curl -L -o fifu https://github.com/Dawaman43/fifu/releases/latest/download/fifu-macos
chmod +x fifu
./fifu
```

---

## ⌨️ Controls

| Key             | Action                     |
| :-------------- | :------------------------- |
| `Enter`         | Select / Confirm / Start   |
| `f`             | Toggle Channel as Favorite |
| `PageUp / Down` | Navigate search results    |
| `Escape`        | Go back                    |
| `q`             | Quit Safely                |

---

## 🛠️ Tech Stack

- **[Textual](https://textual.textualize.io/)** - Stunning TUI framework.
- **[yt-dlp](https://github.com/yt-dlp/yt-dlp)** - The industry standard for video extraction.
- **[Asyncio](https://docs.python.org/3/library/asyncio.html)** - Powering concurrent downloads.

---

## 📜 License

Fifu is released under the **MIT License**. See [LICENSE](LICENSE) for details.

---

_Made with ❤️ by [Dawaman43](https://github.com/Dawaman43)_
