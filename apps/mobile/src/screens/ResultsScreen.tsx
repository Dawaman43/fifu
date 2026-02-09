import React from "react";
import { View, Text, StyleSheet, ScrollView, Pressable } from "react-native";
import { COLORS, SPACING, TYPO } from "../theme";
import { Card } from "../components/Card";
import { ListRow } from "../components/ListRow";
import { MOCK_RESULTS } from "../mock";

export function ResultsScreen({ route, navigation }: { route: any; navigation: any }) {
  const { channels = [] } = route.params || {};

  return (
    <ScrollView style={styles.screen} contentContainerStyle={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>Results</Text>
        <Text style={styles.subtitle}>Found {channels.length} channels</Text>
      </View>

      {channels.length === 0 ? (
        <Card>
          <Text style={styles.desc}>No channels found for your search.</Text>
        </Card>
      ) : (
        channels.map((item: any) => (
          <Pressable 
            key={item.id} 
            onPress={() => navigation.push("Options", { channel: item })}
          >
            <Card>
              <ListRow
                title={item.name}
                meta={item.subs}
                hint="Select"
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
