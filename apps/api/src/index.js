import { Hono } from "hono";
import { exec } from "child_process";
import { promisify } from "util";

const execAsync = promisify(exec);
const app = new Hono();

// Helper to format large numbers (mimics the Python implementation)
const formatCount = (count) => {
  if (!count) return "N/A";
  if (count >= 1000000) return `${(count / 1000000).toFixed(1)}M`;
  if (count >= 1000) return `${(count / 1000).toFixed(1)}K`;
  return count.toString();
};

app.get("/health", (c) => c.json({ ok: true }));

app.post("/api/search", async (c) => {
  const body = await c.req.json().catch(() => ({}));
  const query = body.query || "";
  const type = body.type || "channel"; // "channel" or "video"

  if (!query) return c.json({ query: "", channels: [], videos: [] });

  try {
    const searchPrefix = type === "video" ? "ytsearch50" : "ytsearch50"; 
    const { stdout } = await execAsync(
      `yt-dlp "${searchPrefix}:${query}" --flat-playlist --dump-single-json --quiet --no-warnings`
    );
    const data = JSON.parse(stdout);
    
    const results = { query, type };

    if (type === "video") {
      results.videos = (data.entries || []).map(entry => ({
        id: entry.id,
        title: entry.title || "Unknown",
        url: `https://www.youtube.com/watch?v=${entry.id}`,
        duration: entry.duration,
        uploader: entry.uploader || entry.channel || "Unknown",
        thumbnail: entry.thumbnail
      }));
    } else {
      const channels = [];
      const seenIds = new Set();
      if (data.entries) {
        for (const entry of data.entries) {
          if (entry.channel_id && !seenIds.has(entry.channel_id)) {
            seenIds.add(entry.channel_id);
            const subCount = entry.channel_follower_count || entry.follower_count || 0;
            channels.push({
              id: entry.channel_id,
              name: entry.channel || entry.uploader || "Unknown",
              url: `https://www.youtube.com/channel/${entry.channel_id}`,
              subs: formatCount(subCount),
              subCount: subCount,
              description: entry.description ? entry.description.slice(0, 100) : ""
            });
          }
        }
      }
      channels.sort((a, b) => b.subCount - a.subCount);
      results.channels = channels;
    }

    return c.json(results);
  } catch (error) {
    console.error("Search error:", error);
    return c.json({ query, channels: [], error: "Failed to fetch channels" }, 500);
  }
});

app.post("/api/options", async (c) => {
  const body = await c.req.json().catch(() => ({}));
  const channelId = body.channelId;

  if (!channelId) return c.json({ error: "Missing channelId" }, 400);

  try {
    // Fetch playlists for the channel
    const { stdout } = await execAsync(
      `yt-dlp "https://www.youtube.com/channel/${channelId}/playlists" --flat-playlist --dump-single-json --quiet --no-warnings`
    );
    const data = JSON.parse(stdout);
    
    const playlists = (data.entries || []).map(p => ({
      id: p.id,
      title: p.title || "Unknown Playlist",
      url: p.url || `https://www.youtube.com/playlist?list=${p.id}`,
      count: p.playlist_count || 0
    }));

    return c.json({
      channelId,
      name: data.uploader || data.channel || "Unknown Channel",
      playlists,
      totalVideos: data.playlist_count || 0
    });
  } catch (error) {
    console.error("Options error:", error);
    return c.json({ error: "Failed to fetch channel options" }, 500);
  }
});

// Mock job tracking for the mobile UI
app.get("/api/jobs/:id", (c) => {
  const jobIds = ["job_demo", "a1", "a2"];
  const id = c.req.param("id");
  
  if (!jobIds.includes(id) && !id.startsWith("job_")) {
    return c.json({ error: "Job not found" }, 404);
  }

  return c.json({
    id,
    status: id === "a1" ? "downloading" : "completed",
    total: 10,
    completed: id === "a1" ? 6 : 10,
    progress: id === "a1" ? 60 : 100,
    speed: id === "a1" ? "4.2 MB/s" : "0 B/s",
    eta: id === "a1" ? "1m 20s" : "Done",
    active: id === "a1" ? ["Video metadata...", "Part 2 of 10"] : []
  });
});

export default app;

// Node server bootstrap
if (process.env.NODE_ENV !== "test") {
  const port = Number(process.env.PORT ?? 8787);
  const { serve } = await import("@hono/node-server");
  serve({ fetch: app.fetch, port });
  console.log(`API running on http://localhost:${port}`);
}
