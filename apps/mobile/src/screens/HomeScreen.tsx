import React from "react";
import { View, Text, TextInput, StyleSheet, ScrollView } from "react-native";
import { COLORS, RADIUS, SPACING, TYPO } from "../theme";
import { Section } from "../components/Section";
import { Card } from "../components/Card";
import { PrimaryButton } from "../components/PrimaryButton";
import { SecondaryButton } from "../components/SecondaryButton";
import { Chip } from "../components/Chip";
import { ListRow } from "../components/ListRow";
import { MOCK_HISTORY, MOCK_FAVORITES } from "../mock";

import { apiPost } from "../api/client";

export function HomeScreen({ navigation }: { navigation: any }) {
  const [query, setQuery] = React.useState("");
  const [loading, setLoading] = React.useState(false);
  const [status, setStatus] = React.useState("");
  const [searchType, setSearchType] = React.useState<"channel" | "video">("channel");

  const runSearch = async () => {
    if (!query.trim()) {
      setStatus("Enter a channel name or playlist URL.");
      return;
    }
    
    setLoading(true);
    setStatus("Searching YouTube...");
    
    try {
      const response: any = await apiPost("/api/search", { query, type: searchType });
      setLoading(false);
      setStatus("");
      navigation.push("Results", { 
        query, 
        channels: response.channels || [], 
        videos: response.videos || [],
        type: searchType 
      });
    } catch (error) {
      setLoading(false);
      setStatus(`Error fetching ${searchType}s. Try again.`);
      console.error(error);
    }
  };

  return (
    <ScrollView style={styles.screen} contentContainerStyle={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>Fifu</Text>
        <Text style={styles.subtitle}>Fast channel and playlist downloads</Text>
      </View>

      <Card>
        <Text style={styles.label}>Search YouTube</Text>
        
        <View style={styles.searchTypeRow}>
          <Chip 
            label="Channels" 
            active={searchType === "channel"} 
            onPress={() => setSearchType("channel")} 
          />
          <Chip 
            label="Videos" 
            active={searchType === "video"} 
            onPress={() => setSearchType("video")} 
          />
        </View>

        <TextInput
          placeholder={searchType === "channel" ? "Enter channel name or playlist URL" : "Enter video title"}
          placeholderTextColor={COLORS.muted}
          style={styles.input}
          value={query}
          onChangeText={setQuery}
        />
        <PrimaryButton label={`Search ${searchType === "channel" ? "Channels" : "Videos"}`} onPress={runSearch} loading={loading} />
        {status ? <Text style={styles.status}>{status}</Text> : null}
      </Card>

      <Section title="Recent">
        {MOCK_HISTORY.length === 0 ? (
          <Card>
            <ListRow title="No recent searches yet" meta="Your history will appear here" />
          </Card>
        ) : (
          MOCK_HISTORY.map((item) => (
            <Card key={item.id}>
              <ListRow title={item.name} meta={`${item.subs} subscribers`} hint="Search again" />
            </Card>
          ))
        )}
      </Section>

      <Section title="Favorites">
        {MOCK_FAVORITES.length === 0 ? (
          <Card>
            <ListRow title="No favorites yet" meta="Star channels to pin them here" />
          </Card>
        ) : (
          MOCK_FAVORITES.map((item) => (
            <Card key={item.id}>
              <ListRow title={item.name} meta={`${item.subs} subscribers`} hint="Open options" />
            </Card>
          ))
        )}
      </Section>

      <Section title="Quick Options">
        <View style={styles.chipRow}>
          {"Best 1080p 720p Audio".split(" ").map((label) => (
            <Chip key={label} label={label} />
          ))}
        </View>
      </Section>

      <Card>
        <Text style={styles.listTitle}>Downloads</Text>
        <Text style={styles.listMeta}>
          Start a job to see progress, speed, and logs.
        </Text>
        <SecondaryButton label="Go to Downloads" onPress={() => navigation.navigate("Downloads")} />
      </Card>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    padding: SPACING.lg,
    gap: SPACING.lg
  },
  screen: {
    backgroundColor: COLORS.background
  },
  header: {
    gap: SPACING.xs
  },
  title: {
    fontSize: TYPO.h1,
    fontWeight: "700",
    color: COLORS.text
  },
  subtitle: {
    fontSize: TYPO.body,
    color: COLORS.muted
  },
  label: {
    fontSize: 14,
    color: COLORS.muted,
    marginBottom: SPACING.sm
  },
  input: {
    height: 48,
    borderRadius: RADIUS.sm,
    paddingHorizontal: SPACING.md,
    borderWidth: 1,
    borderColor: COLORS.surfaceLight,
    backgroundColor: COLORS.surface,
    color: COLORS.text,
    marginBottom: SPACING.md
  },
  searchTypeRow: {
    flexDirection: "row",
    gap: SPACING.sm,
    marginBottom: SPACING.md
  },
  status: {
    color: COLORS.muted,
    fontSize: TYPO.small
  },
  chipRow: {
    flexDirection: "row",
    flexWrap: "wrap",
    gap: SPACING.sm
  },
  listTitle: {
    fontSize: TYPO.h3,
    fontWeight: "700",
    color: COLORS.text,
    marginBottom: SPACING.xs
  },
  listMeta: {
    fontSize: TYPO.small,
    color: COLORS.muted,
    marginBottom: SPACING.md
  }
});
