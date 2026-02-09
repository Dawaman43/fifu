import React from "react";
import { View, Text, StyleSheet, ScrollView } from "react-native";
import { COLORS, SPACING, TYPO } from "../theme";
import { Card } from "../components/Card";
import { SecondaryButton } from "../components/SecondaryButton";

export function SettingsScreen() {
  return (
    <ScrollView style={styles.screen} contentContainerStyle={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>Settings</Text>
        <Text style={styles.subtitle}>Defaults and storage</Text>
      </View>

      <Card>
        <Text style={styles.sectionTitle}>Defaults</Text>
        <Text style={styles.meta}>Quality: Best</Text>
        <Text style={styles.meta}>Subtitles: Off</Text>
        <Text style={styles.meta}>Concurrency: 3</Text>
      </Card>

      <Card>
        <Text style={styles.sectionTitle}>Storage</Text>
        <Text style={styles.meta}>Download path: /Downloads/Fifu</Text>
      </Card>

      <Card>
        <Text style={styles.sectionTitle}>Maintenance</Text>
        <Text style={styles.meta}>Clear logs and history</Text>
        <View style={styles.actions}>
          <SecondaryButton label="Clear Logs" onPress={() => {}} />
          <SecondaryButton label="Clear History" onPress={() => {}} />
        </View>
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
    fontSize: TYPO.h2,
    fontWeight: "700",
    color: COLORS.text
  },
  subtitle: {
    fontSize: TYPO.small,
    color: COLORS.muted
  },
  sectionTitle: {
    fontSize: TYPO.h3,
    fontWeight: "600",
    color: COLORS.text,
    marginBottom: SPACING.sm
  },
  actions: {
    gap: SPACING.sm,
    marginTop: SPACING.sm
  },
  meta: {
    color: COLORS.muted,
    fontSize: TYPO.small,
    marginTop: SPACING.xs
  }
});
