import React from "react";
import { Pressable, View, StyleSheet } from "react-native";
import { COLORS } from "../theme";

export function Toggle({ value, onChange }: { value: boolean; onChange?: (v: boolean) => void }) {
  return (
    <Pressable
      onPress={() => onChange?.(!value)}
      style={[styles.track, value && styles.trackOn]}
    >
      <View style={[styles.handle, value && styles.handleOn]} />
    </Pressable>
  );
}

const styles = StyleSheet.create({
  track: {
    width: 52,
    height: 28,
    borderRadius: 16,
    backgroundColor: "#E5E7EB",
    padding: 3
  },
  trackOn: {
    backgroundColor: "#DBEAFE"
  },
  handle: {
    width: 22,
    height: 22,
    borderRadius: 11,
    backgroundColor: COLORS.white
  },
  handleOn: {
    alignSelf: "flex-end",
    backgroundColor: COLORS.cta
  }
});
