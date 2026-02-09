"""Download service for managing video downloads."""

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Optional
import yt_dlp


@dataclass
class DownloadProgress:
    """Progress information for a download."""
    video_title: str
    status: str
    downloaded_bytes: int = 0
    total_bytes: int = 0
    speed: Optional[str] = None
    eta: Optional[str] = None
    percent: float = 0.0


@dataclass
class DownloadResult:
    """Result of a download operation."""
    success: bool
    video_title: str
    file_path: Optional[Path] = None
    error: Optional[str] = None


@dataclass
class DownloadQueue:
    """Queue of videos to download."""
    channel_name: str
    videos: list = field(default_factory=list)
    current_index: int = 0
    downloaded_ids: set = field(default_factory=set)


class DownloadService:
    """Service for downloading YouTube videos."""

    def __init__(self):
        pass

    def get_download_path(self, channel_name: str) -> Path:
        """Get the download path for a channel."""
        safe_name = self._sanitize_filename(channel_name)
        downloads_dir = Path.home() / "Downloads" / "videos" / safe_name
        downloads_dir.mkdir(parents=True, exist_ok=True)
        return downloads_dir

    def _sanitize_filename(self, name: str) -> str:
        """Sanitize a string for use as a filename."""
        safe = re.sub(r'[<>:"/\\|?*]', '', name)
        safe = safe.strip('. ')
        return safe or "unknown_channel"


    def download_video(
        self,
        video_url: str,
        output_dir: Path,
        progress_callback: Optional[Callable[[DownloadProgress], None]] = None,
        quality: str = "best",
        video_id: str = "unknown"
    ) -> DownloadResult:
        """Download a single video with specified quality."""
        current_title = "Loading..."

        def progress_hook(d: dict):
            if progress_callback:
                status = d.get("status", "unknown")
                if status == "downloading":
                    downloaded = d.get("downloaded_bytes", 0)
                    total = d.get("total_bytes") or d.get("total_bytes_estimate", 0)
                    percent = (downloaded / total * 100) if total > 0 else 0
                    
                    progress_callback(DownloadProgress(
                        video_title=current_title,
                        status="downloading",
                        downloaded_bytes=downloaded,
                        total_bytes=total,
                        speed=d.get("_speed_str", ""),
                        eta=d.get("_eta_str", ""),
                        percent=percent,
                    ))
                elif status == "finished":
                    progress_callback(DownloadProgress(
                        video_title=current_title,
                        status="processing",
                        percent=100.0,
                    ))

        output_template = str(output_dir / "%(title)s.%(ext)s")
        
        if quality == "best":
            format_str = "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best"
        elif quality == "bestaudio/best":
            format_str = "bestaudio/best"
        else:
            format_str = quality
        
        ydl_opts = {
            "format": format_str,
            "outtmpl": output_template,
            "progress_hooks": [progress_hook],
            "quiet": True,
            "no_warnings": True,
            "merge_output_format": "mp4",
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                info = ydl.extract_info(video_url, download=False)
                if info:
                    nonlocal current_title
                    current_title = info.get("title", "Unknown")
                    
                    if progress_callback:
                        progress_callback(DownloadProgress(
                            video_title=current_title,
                            status="starting",
                            percent=0.0,
                        ))
                    
                    ydl.download([video_url])
                    
                    filename = ydl.prepare_filename(info)
                    file_path = Path(filename)
                    
                    if not file_path.exists():
                        mp4_path = file_path.with_suffix('.mp4')
                        if mp4_path.exists():
                            file_path = mp4_path
                    
                    return DownloadResult(
                        success=True,
                        video_title=current_title,
                        file_path=file_path if file_path.exists() else None,
                    )
            except Exception as e:
                return DownloadResult(
                    success=False,
                    video_title=current_title,
                    error=str(e),
                )
        
        return DownloadResult(
            success=False,
            video_title=self._current_title,
            error="Unknown error",
        )

    def get_downloaded_videos(self, output_dir: Path) -> set[str]:
        """Get set of already downloaded video titles (without extension)."""
        downloaded = set()
        if output_dir.exists():
            for file in output_dir.iterdir():
                if file.is_file() and file.suffix in ('.mp4', '.mkv', '.webm', '.m4a', '.mp3'):
                    downloaded.add(file.stem)
        return downloaded
