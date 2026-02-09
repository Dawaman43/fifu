"use client";

import { useEffect, useState } from "react";

const STORAGE_KEY = "fifu-theme";

type Theme = "dark" | "light";

function resolveTheme(): Theme {
  if (typeof window === "undefined") {
    return "dark";
  }

  const stored = window.localStorage.getItem(STORAGE_KEY) as Theme | null;
  if (stored === "light" || stored === "dark") {
    return stored;
  }

  return window.matchMedia("(prefers-color-scheme: light)").matches ? "light" : "dark";
}

export function ThemeToggle() {
  const [theme, setTheme] = useState<Theme>("dark");

  useEffect(() => {
    const nextTheme = resolveTheme();
    setTheme(nextTheme);
    document.documentElement.setAttribute("data-theme", nextTheme);
  }, []);

  const toggleTheme = () => {
    const nextTheme: Theme = theme === "dark" ? "light" : "dark";
    setTheme(nextTheme);
    document.documentElement.setAttribute("data-theme", nextTheme);
    window.localStorage.setItem(STORAGE_KEY, nextTheme);
  };

  return (
    <button
      type="button"
      onClick={toggleTheme}
      className="focus-ring inline-flex items-center gap-2 rounded-full border border-ink-700/40 bg-ink-900/70 px-3 py-2 text-xs font-semibold uppercase tracking-[0.24em] text-ink-300 transition duration-200 hover:border-ink-700/60 hover:text-ink-100"
      aria-pressed={theme === "light"}
      aria-label="Toggle color theme"
    >
      <span className="h-2 w-2 rounded-full bg-accent-500 shadow-glow" />
      {theme === "light" ? "Light" : "Dark"}
    </button>
  );
}
