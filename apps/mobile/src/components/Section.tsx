import React from "react";
import { View, Text, StyleSheet } from "react-native";
import { COLORS, SPACING, TYPO } from "../theme";

export function Section({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <View style={styles.section}>
      <Text style={styles.title}>{title}</Text>
      {children}
    </View>
  );
}

const styles = StyleSheet.create({
  section: {
    gap: SPACING.sm
  },
  title: {
    fontSize: TYPO.h3,
    fontWeight: "600",
    color: COLORS.text
  }
});
