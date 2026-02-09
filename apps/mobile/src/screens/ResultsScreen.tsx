import React from "react";
import { View, Text, StyleSheet, ScrollView, Pressable } from "react-native";
import { COLORS, SPACING, TYPO } from "../theme";
import { Card } from "../components/Card";
import { ListRow } from "../components/ListRow";
import { MOCK_RESULTS } from "../mock";

export function ResultsScreen({ route, navigation }: { route: any; navigation: any }) {
  const { channels = [], videos = [], type = "channel" } = route.params || {};
  const data = type === "video" ? videos : channels;

  return (
    <ScrollView style={styles.screen} contentContainerStyle={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>{type === "video" ? "Videos" : "Channels"}</Text>
        <Text style={styles.subtitle}>Found {data.length} {type}s</Text>
      </View>

      {data.length === 0 ? (
        <Card>
          <Text style={styles.desc}>No {type}s found for your search.</Text>
        </Card>
      ) : (
        data.map((item: any) => (
          <Pressable 
            key={item.id} 
            onPress={() => {
              if (type === "video") {
                // For direct video search, we skip to options but with single video selected
                navigation.push("Options", { 
                  video: item, 
                  isSingleVideo: true 
                });
              } else {
                navigation.push("Options", { channel: item });
              }
            }}
          >
            <Card>
              <ListRow
                title={item.title || item.name}
                meta={type === "video" ? item.uploader : item.subs}
                hint={type === "video" ? (item.duration ? `${Math.floor(item.duration / 60)}m` : "Select") : "Select"}
              />
              {item.description ? (
                <Text style={styles.desc} numberOfLines={2}>{item.description}</Text>
              ) : null}
            </Card>
          </Pressable>
        ))
      )}
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    padding: SPACING.lg,
    gap: SPACING.md
  },
  screen: {
    backgroundColor: COLORS.background
  },
  header: {
    gap: SPACING.xs,
    marginBottom: SPACING.sm
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
  desc: {
    marginTop: SPACING.md,
    fontSize: TYPO.body,
    color: COLORS.text
  }
});
