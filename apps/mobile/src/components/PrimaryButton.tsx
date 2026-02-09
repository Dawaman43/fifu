import React from "react";
import { Pressable, Text, StyleSheet, ActivityIndicator } from "react-native";
import { COLORS, RADIUS, SPACING, TYPO } from "../theme";

export function PrimaryButton({
  label,
  onPress,
  loading
}: {
  label: string;
  onPress?: () => void;
  loading?: boolean;
}) {
  return (
    <Pressable 
      style={[styles.button, loading && styles.disabled]} 
      onPress={loading ? undefined : onPress}
    >
      {loading ? (
        <ActivityIndicator color={COLORS.white} />
      ) : (
        <Text style={styles.text}>{label}</Text>
      )}
    </Pressable>
  );
}

const styles = StyleSheet.create({
  button: {
    height: 52,
    borderRadius: RADIUS.md,
    backgroundColor: COLORS.primary,
    alignItems: "center",
    justifyContent: "center",
    paddingHorizontal: SPACING.lg,
    shadowColor: COLORS.primary,
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.3,
    shadowRadius: 8,
    elevation: 4
  },
  text: {
    color: COLORS.white,
    fontWeight: "700",
    fontSize: TYPO.body,
    letterSpacing: 0.5
  },
  disabled: {
    opacity: 0.7,
    backgroundColor: COLORS.surfaceLight
  }
});
