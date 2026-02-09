import React from "react";
import { View, Text, StyleSheet } from "react-native";
import { COLORS, SPACING, TYPO } from "../theme";

export function ListRow({
  title,
  meta,
  hint
}: {
  title: string;
  meta?: string;
  hint?: string;
}) {
  return (
    <View style={styles.row}>
      <Text style={styles.title}>{title}</Text>
      {meta ? <Text style={styles.meta}>{meta}</Text> : null}
      {hint ? <Text style={styles.hint}>{hint}</Text> : null}
    </View>
  );
}

const styles = StyleSheet.create({
  row: {
    gap: SPACING.xs
  },
  title: {
    color: COLORS.text,
    fontSize: TYPO.body,
    fontWeight: "600"
  },
  meta: {
    color: COLORS.muted,
    fontSize: TYPO.small
  },
  hint: {
    color: COLORS.cta,
    fontSize: TYPO.small,
    fontWeight: "600"
  }
});
