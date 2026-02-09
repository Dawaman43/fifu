"""Download service for managing video downloads."""

import re
import shutil
from dataclasses import dataclass, field
import logging
from pathlib import Path
from typing import Callable, Optional
import yt_dlp


class DownloadStopped(Exception):
    """Exception raised when download is stopped by user."""
    pass


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
        self.log_file = Path.home() / ".config" / "fifu" / "downloader.log"
        self.log_file.parent.mkdir(parents=True, exist_ok=True)
        logging.basicConfig(
            filename=str(self.log_file),
            level=logging.DEBUG,
            format="%(asctime)s - %(levelname)s - %(message)s",
        )
        logging.info("Downloader service initialized")

    def get_download_path(self, channel_name: str, playlist_name: Optional[str] = None) -> Path:
        """Get the download path for a channel, optionally into a playlist subfolder."""
        safe_channel = self._sanitize_filename(channel_name)
        downloads_dir = Path.home() / "Downloads" / "videos" / safe_channel
        
        if playlist_name:
            safe_playlist = self._sanitize_filename(playlist_name)
            downloads_dir = downloads_dir / safe_playlist
            
        downloads_dir.mkdir(parents=True, exist_ok=True)
        return downloads_dir

    def _sanitize_filename(self, name: str) -> str:
        """Sanitize a string for use as a filename."""
        safe = re.sub(r'[<>:"/\\|?*]', '', name)
        safe = safe.strip('. ')
        return safe or "unknown_channel"

    def is_aria2_available(self) -> bool:
        """Check if aria2c is available on the system."""
        return shutil.which("aria2c") is not None


    def download_video(
        self,
        video_url: str,
        output_dir: Path,
        progress_callback: Optional[Callable[[DownloadProgress], None]] = None,
        quality: str = "best",
        video_id: str = "unknown",
        subtitles: bool = False,
        stop_check: Optional[Callable[[], bool]] = None
    ) -> DownloadResult:
        """Download a single video with specified quality."""
        expected_total_bytes = 0

        def progress_hook(d: dict):
            if stop_check and stop_check():
                raise DownloadStopped("User requested stop")
                
            if progress_callback:
                status = d.get("status", "unknown")
                if status == "downloading":
                    downloaded = d.get("downloaded_bytes", 0)
                    total = d.get("total_bytes") or d.get("total_bytes_estimate") or expected_total_bytes
                    
                    if total > 0:
                        percent = (downloaded / total * 100)
                    else:
                        # Fallback for when we really don't know the size
                        percent = 0.01 
                    
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
                        status="finishing",
                        percent=100.0,
                    ))

        output_template = str(output_dir / "%(title)s.%(ext)s")
        
        if quality == "best":
            format_str = "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best"
        elif quality == "bestaudio/best":
            format_str = "bestaudio/best"
        else:
            format_str = quality
        
        class YDLogger:
            def debug(self, msg):
                if msg.startswith('[debug] '): pass
                else: self.info(msg)
            def info(self, msg): logging.info(f"yt-dlp: {msg}")
            def warning(self, msg): logging.warning(f"yt-dlp: {msg}")
            def error(self, msg): logging.error(f"yt-dlp: {msg}")

        ydl_opts = {
            "format": format_str,
            "outtmpl": output_template,
            "progress_hooks": [progress_hook],
            "quiet": True,
            "no_warnings": True,
            "merge_output_format": "mp4",
            "logger": YDLogger(),
            "noprogress": False,
            "nooverwrites": True,
        }

        if self.is_aria2_available():
            ydl_opts.update({
                "external_downloader": "aria2c",
                "external_downloader_args": {
                    "default": [
                        "--min-split-size=1M",
                        "--max-connection-per-server=16",
                        "--split=16",
                        "--summary-interval=0",
                        "--quiet=true",
                        "--show-console-readout=false",
                        "--console-log-level=error",
                        "--download-result=hide",
                    ]
                }
            })
            logging.info("Using aria2c for multi-threaded downloading")

        if subtitles:
            ydl_opts.update({
                "writesubtitles": True,
                "subtitleslangs": ["en.*", ".*"],
                "embedsubs": True,
            })
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                info = ydl.extract_info(video_url, download=False)
                if info:
                    current_title = info.get("title", "Unknown")
                    expected_total_bytes = info.get("filesize") or info.get("filesize_approx") or 0
                    
                    if progress_callback:
                        progress_callback(DownloadProgress(
                            video_title=current_title,
                            status="starting",
                            percent=0.0,
                        ))
                    
                    logging.info(f"Starting download: {current_title} ({video_url})")
                    ydl.download([video_url])
                    logging.info(f"Download finished: {current_title}")
                    
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
            except DownloadStopped as e:
                logging.info(f"Download aborted for {video_url}: {str(e)}")
                return DownloadResult(
                    success=False,
                    video_title=current_title,
                    error="Stopped by user",
                )
            except Exception as e:
                logging.error(f"Download failed for {video_url}: {str(e)}")
                return DownloadResult(
                    success=False,
                    video_title=current_title,
                    error=str(e),
                )
        
        return DownloadResult(
            success=False,
            video_title=current_title,
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
