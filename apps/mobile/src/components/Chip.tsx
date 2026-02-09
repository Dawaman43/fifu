import React from "react";
import { Pressable, Text, StyleSheet } from "react-native";
import { COLORS, RADIUS, SPACING, TYPO } from "../theme";

export function Chip({
  label,
  active,
  onPress
}: {
  label: string;
  active?: boolean;
  onPress?: () => void;
}) {
  return (
    <Pressable style={[styles.chip, active && styles.active]} onPress={onPress}>
      <Text style={[styles.text, active && styles.textActive]}>{label}</Text>
    </Pressable>
  );
}

const styles = StyleSheet.create({
  chip: {
    paddingVertical: SPACING.sm,
    paddingHorizontal: SPACING.md,
    borderRadius: RADIUS.pill,
    borderWidth: 1,
    borderColor: COLORS.border,
    backgroundColor: COLORS.surface
  },
  active: {
    borderColor: COLORS.primary,
    backgroundColor: COLORS.primary + "20" // 12% opacity
  },
  text: {
    color: COLORS.muted,
    fontSize: TYPO.small,
    fontWeight: "600"
  },
  textActive: {
    color: COLORS.primary
  }
});
