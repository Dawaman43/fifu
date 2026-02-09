"use client";

import { useEffect, useState } from "react";
import { Download } from "lucide-react";

export function DownloadCounter() {
  const [downloads, setDownloads] = useState<number | null>(null);

  useEffect(() => {
    fetch("https://api.npmjs.org/downloads/point/last-year/fifu-tui")
      .then((res) => res.json())
      .then((data) => {
        if (data.downloads) {
          setDownloads(data.downloads);
        }
      })
      .catch((err) => console.error("Failed to fetch downloads", err));
  }, []);

  if (downloads === null) return null;

  return (
    <div className="flex items-center gap-2 text-sm text-muted-foreground mt-2">
      <Download className="size-4" />
      <span>{downloads.toLocaleString()} downloads last year</span>
    </div>
  );
}
