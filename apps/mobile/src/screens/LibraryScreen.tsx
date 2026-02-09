import React from "react";
import { View, Text, StyleSheet, ScrollView, Pressable } from "react-native";
import { COLORS, SPACING, TYPO } from "../theme";
import { Card } from "../components/Card";
import { ListRow } from "../components/ListRow";
import { MOCK_FAVORITES, MOCK_HISTORY } from "../mock";

export function LibraryScreen() {
  const [tab, setTab] = React.useState<"history" | "favorites">("history");
  const items = tab === "history" ? MOCK_HISTORY : MOCK_FAVORITES;

  return (
    <ScrollView style={styles.screen} contentContainerStyle={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>Library</Text>
        <Text style={styles.subtitle}>History and favorites</Text>
      </View>

      <View style={styles.segment}>
        <Pressable
          style={[styles.segmentButton, tab === "history" && styles.segmentActive]}
          onPress={() => setTab("history")}
        >
          <Text style={tab === "history" ? styles.segmentTextActive : styles.segmentText}>
            History
          </Text>
        </Pressable>
        <Pressable
          style={[styles.segmentButton, tab === "favorites" && styles.segmentActive]}
          onPress={() => setTab("favorites")}
        >
          <Text style={tab === "favorites" ? styles.segmentTextActive : styles.segmentText}>
            Favorites
          </Text>
        </Pressable>
      </View>

      {items.length === 0 ? (
        <Card>
          <ListRow
            title={tab === "history" ? "No history yet" : "No favorites yet"}
            meta={tab === "history" ? "Search for channels to build your history." : "Star a channel to pin it here."}
          />
        </Card>
      ) : (
        items.map((item) => (
          <Card key={item.id}>
            <ListRow title={item.name} meta={`${item.subs} subscribers`} hint="Open options" />
          </Card>
        ))
      )}
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
  segment: {
    flexDirection: "row",
    gap: SPACING.sm
  },
  segmentButton: {
    flex: 1,
    height: 40,
    borderRadius: 12,
    borderWidth: 1,
    borderColor: COLORS.border,
    alignItems: "center",
    justifyContent: "center",
    backgroundColor: COLORS.surface
  },
  segmentActive: {
    borderColor: COLORS.cta,
    backgroundColor: "#EEF2FF"
  },
  segmentText: {
    color: COLORS.muted,
    fontWeight: "600"
  },
  segmentTextActive: {
    color: COLORS.cta,
    fontWeight: "700"
  },
});
