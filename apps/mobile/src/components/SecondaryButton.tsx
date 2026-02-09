import React from "react";
import { Pressable, Text, StyleSheet } from "react-native";
import { COLORS, RADIUS, SPACING, TYPO } from "../theme";

export function SecondaryButton({
  label,
  onPress
}: {
  label: string;
  onPress?: () => void;
}) {
  return (
    <Pressable style={styles.button} onPress={onPress}>
      <Text style={styles.text}>{label}</Text>
    </Pressable>
  );
}

const styles = StyleSheet.create({
  button: {
    height: 48,
    borderRadius: RADIUS.md,
    borderWidth: 1.5,
    borderColor: COLORS.surfaceLight,
    backgroundColor: "transparent",
    alignItems: "center",
    justifyContent: "center",
    paddingHorizontal: SPACING.lg
  },
  text: {
    color: COLORS.text,
    fontSize: TYPO.body,
    fontWeight: "600",
    letterSpacing: 0.3
  }
});
