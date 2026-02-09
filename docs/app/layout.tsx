import "./globals.css";
import { IBM_Plex_Sans, JetBrains_Mono } from "next/font/google";
import { RootProvider } from "fumadocs-ui/provider/next";
import { DocsLayout } from "fumadocs-ui/layouts/docs";
import { docs } from "@/lib/source";

const plexSans = IBM_Plex_Sans({
  subsets: ["latin"],
  variable: "--font-sans",
  display: "swap",
  weight: ["400", "500", "600", "700"],
});

const jetBrainsMono = JetBrains_Mono({
  subsets: ["latin"],
  variable: "--font-mono",
  display: "swap",
  weight: ["400", "500", "600", "700"],
});

export const metadata = {
  title: "Fifu Docs",
  description: "Documentation for Fifu, the ultra-fast YouTube channel downloader TUI.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html
      lang="en"
      data-theme="dark"
      suppressHydrationWarning
      className={`${plexSans.variable} ${jetBrainsMono.variable}`}
    >
      <body className="font-sans">
        <RootProvider
          search={{
            links: [
              ["Quickstart", "/quickstart"],
              ["Installation", "/installation"],
              ["Troubleshooting", "/troubleshooting"],
            ],
          }}
        >
          <DocsLayout
            tree={docs.pageTree}
            nav={{
              title: "Fifu Docs",
              url: "/",
            }}
            githubUrl="https://github.com/Dawaman43/fifu"
          >
            {children}
          </DocsLayout>
        </RootProvider>
      </body>
    </html>
  );
}
