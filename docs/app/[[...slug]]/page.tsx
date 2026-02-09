import { notFound } from "next/navigation";
import { DocsPage, DocsBody, DocsTitle, DocsDescription } from "fumadocs-ui/page";
import { docs } from "@/lib/source";
import defaultMdxComponents from "fumadocs-ui/mdx";
import { Card, Cards } from "fumadocs-ui/components/card";
import { Tab, Tabs } from "fumadocs-ui/components/tabs";
import { Activity, Terminal, Zap, Layers, ChevronRight, Globe, Github } from "lucide-react";
import { DownloadCounter } from "@/app/components/download-counter";

export default async function DocsPageRoute(props: {
  params: Promise<{ slug?: string[] }>;
}) {
  const params = await props.params;
  const page = await docs.getPage(params.slug ?? []);
  if (!page) {
    notFound();
  }

  const MDX = page.data.body;

  return (
    <DocsPage toc={page.data.toc} full={page.data.full}>
      <DocsTitle>{page.data.title}</DocsTitle>
      <DocsDescription>{page.data.description}</DocsDescription>
      <DocsBody>
        <MDX 
          components={{ 
            ...defaultMdxComponents,
            Card,
            Cards,
            Tab,
            Tabs,
            DownloadCounter,
            Activity,
            Terminal,
            Zap,
            Layers,
            ChevronRight,
            Globe,
            Github
          }} 
        />
      </DocsBody>
    </DocsPage>
  );
}

export async function generateStaticParams() {
  return docs.generateParams();
}

