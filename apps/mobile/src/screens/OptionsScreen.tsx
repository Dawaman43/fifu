import React from "react";
import { View, Text, StyleSheet, ScrollView, TextInput } from "react-native";
import { COLORS, RADIUS, SPACING, TYPO } from "../theme";
import { Card } from "../components/Card";
import { PrimaryButton } from "../components/PrimaryButton";
import { Chip } from "../components/Chip";
import { Toggle } from "../components/Toggle";

const QUALITYS = ["Best", "1080p", "720p", "480p", "Audio"];
const COUNTS = ["5", "10", "25", "All"];

import { apiPost } from "../api/client";

export function OptionsScreen({ route, navigation }: { route: any; navigation: any }) {
  const { channel } = route.params || {};
  const [selectedQuality, setSelectedQuality] = React.useState("Best");
  const [selectedCount, setSelectedCount] = React.useState("All");
  const [selectedPlaylist, setSelectedPlaylist] = React.useState<any>(null);
  const [subtitles, setSubtitles] = React.useState(false);
  const [playlists, setPlaylists] = React.useState<any[]>([]);
  const [loading, setLoading] = React.useState(true);

  React.useEffect(() => {
    if (channel?.id) {
      loadOptions();
    }
  }, [channel]);

  const loadOptions = async () => {
    try {
      const resp: any = await apiPost("/api/options", { channelId: channel.id });
      setPlaylists(resp.playlists || []);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  const startDownload = async () => {
    // In a real app, this would hit /api/download or similar
    // For this polish, we navigate to Downloads which shows mock progress for this channel
    navigation.navigate("Downloads", { 
      channel, 
      quality: selectedQuality, 
      count: selectedCount,
      playlist: selectedPlaylist
    });
  };

  return (
    <ScrollView style={styles.screen} contentContainerStyle={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>Download Options</Text>
        <Text style={styles.subtitle}>{channel?.name || "Unknown Channel"}</Text>
      </View>

      <Card>
        <Text style={styles.label}>How many videos?</Text>
        <View style={styles.chipRow}>
          {COUNTS.map((label) => (
            <Chip
              key={label}
              label={label}
              active={selectedCount === label}
              onPress={() => setSelectedCount(label)}
            />
          ))}
        </View>
        <TextInput
          placeholder="Custom count (e.g. 50)"
          placeholderTextColor={COLORS.muted}
          style={styles.input}
          value={selectedCount === "All" ? "" : selectedCount}
          onChangeText={setSelectedCount}
          keyboardType="numeric"
        />
      </Card>

      <Card>
        <Text style={styles.label}>Video quality</Text>
        <View style={styles.chipRow}>
          {QUALITYS.map((label) => (
            <Chip
              key={label}
              label={label}
              active={selectedQuality === label}
              onPress={() => setSelectedQuality(label)}
            />
          ))}
        </View>
      </Card>

      <Card>
        <Text style={styles.label}>Subtitles</Text>
        <View style={styles.toggleRow}>
          <Text style={styles.meta}>Download and embed subtitles</Text>
          <Toggle value={subtitles} onChange={setSubtitles} />
        </View>
      </Card>

      <Card>
        <Text style={styles.label}>Select Playlist (optional)</Text>
        {loading ? (
          <Text style={styles.meta}>Loading playlists...</Text>
        ) : playlists.length === 0 ? (
          <Text style={styles.meta}>No playlists found</Text>
        ) : (
          <View style={styles.chipRow}>
            <Chip 
              label="All Videos" 
              active={!selectedPlaylist} 
              onPress={() => setSelectedPlaylist(null)} 
            />
            {playlists.map((p) => (
              <Chip
                key={p.id}
                label={`${p.title} (${p.count})`}
                active={selectedPlaylist?.id === p.id}
                onPress={() => setSelectedPlaylist(p)}
              />
            ))}
          </View>
        )}
      </Card>

      <PrimaryButton label="Start Download" onPress={startDownload} />
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
    fontSize: TYPO.h2,
    fontWeight: "700",
    color: COLORS.text
  },
  subtitle: {
    fontSize: TYPO.small,
    color: COLORS.muted
  },
  label: {
    fontSize: TYPO.body,
    fontWeight: "600",
    color: COLORS.text,
    marginBottom: SPACING.sm
  },
  input: {
    height: 48,
    borderRadius: RADIUS.sm,
    paddingHorizontal: SPACING.md,
    borderWidth: 1,
    borderColor: COLORS.border,
    backgroundColor: COLORS.white,
    color: COLORS.text,
    marginTop: SPACING.md
  },
  chipRow: {
    flexDirection: "row",
    flexWrap: "wrap",
    gap: SPACING.sm
  },
  meta: {
    fontSize: TYPO.small,
    color: COLORS.muted
  },
  toggleRow: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-between"
  }
});
