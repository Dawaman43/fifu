"use client";

import { useEffect, useState } from "react";
import { Area, AreaChart, ResponsiveContainer, Tooltip, XAxis } from "recharts";
import { Download, TrendingUp } from "lucide-react";

interface DownloadData {
  day: string;
  downloads: number;
}

export function DownloadStats() {
  const [data, setData] = useState<DownloadData[]>([]);
  const [total, setTotal] = useState<number>(0);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Fetch last year's data
    fetch("https://api.npmjs.org/downloads/range/last-year/fifu-tui")
      .then((res) => res.json())
      .then((json) => {
        if (json.downloads && Array.isArray(json.downloads)) {
          const downloads = json.downloads.map((item: any) => ({
            day: item.day,
            downloads: item.downloads,
          }));
          setData(downloads);
          
          const sum = downloads.reduce((acc: number, curr: any) => acc + curr.downloads, 0);
          setTotal(sum);
        }
      })
      .catch((err) => console.error("Failed to fetch stats", err))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div className="animate-pulse h-32 w-full bg-muted/20 rounded-lg"></div>;

  return (
    <div className="border rounded-xl p-6 bg-card text-card-foreground shadow-sm my-8 relative overflow-hidden">
      <div className="absolute inset-0 bg-linear-to-br from-primary/5 to-transparent pointer-events-none" />
      <div className="flex flex-col md:flex-row justify-between gap-8 relative z-10">
        <div className="flex flex-col justify-between">
          <div>
             <h3 className="text-lg font-medium flex items-center gap-2 text-muted-foreground">
              <Download className="w-4 h-4" />
              Downloads (Last Year)
            </h3>
            <p className="text-4xl font-bold mt-2 tracking-tight">
              {total.toLocaleString()}
            </p>
          </div>
          <div className="mt-4 flex items-center text-sm text-green-500 font-medium">
            <TrendingUp className="w-4 h-4 mr-1" />
            Active Community
          </div>
        </div>

        <div className="h-[120px] w-full md:w-[60%] min-w-[200px]">
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart data={data}>
              <defs>
                <linearGradient id="colorDownloads" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="currentColor" stopOpacity={0.3} className="text-primary"/>
                  <stop offset="95%" stopColor="currentColor" stopOpacity={0} className="text-primary"/>
                </linearGradient>
              </defs>
              <Tooltip 
                contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 4px 12px rgba(0,0,0,0.1)' }}
                labelStyle={{ color: '#666' }}
              />
              <Area 
                type="monotone" 
                dataKey="downloads" 
                stroke="currentColor" 
                strokeWidth={2}
                fillOpacity={1} 
                fill="url(#colorDownloads)" 
                className="text-primary"
              />
            </AreaChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
}
