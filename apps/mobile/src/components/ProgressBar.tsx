import React from "react";
import { View, StyleSheet } from "react-native";
import { COLORS } from "../theme";

export function ProgressBar({ value }: { value: number }) {
  const width = `${Math.max(0, Math.min(100, value))}%`;
  return (
    <View style={styles.track}>
      <View style={[styles.fill, { width }]} />
    </View>
  );
}

const styles = StyleSheet.create({
  track: {
    height: 10,
    borderRadius: 6,
    backgroundColor: "#F3DDE1",
    overflow: "hidden"
  },
  fill: {
    height: 10,
    borderRadius: 6,
    backgroundColor: COLORS.cta
  }
});
