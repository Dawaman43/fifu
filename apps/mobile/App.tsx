import React from "react";
import { SafeAreaView, StyleSheet, StatusBar } from "react-native";
import { AppNavigation } from "./src/navigation";
import { COLORS } from "./src/theme";

export default function App() {
  return (
    <SafeAreaView style={styles.safeArea}>
      <StatusBar barStyle="light-content" backgroundColor={COLORS.background} />
      <AppNavigation />
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  safeArea: {
    flex: 1,
    backgroundColor: COLORS.background
  }
});
