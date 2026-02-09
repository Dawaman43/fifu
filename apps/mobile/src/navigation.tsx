import React from "react";
import { NavigationContainer } from "@react-navigation/native";
import { createNativeStackNavigator } from "@react-navigation/native-stack";
import { createBottomTabNavigator } from "@react-navigation/bottom-tabs";
import { HomeScreen } from "./screens/HomeScreen";
import { ResultsScreen } from "./screens/ResultsScreen";
import { OptionsScreen } from "./screens/OptionsScreen";
import { DownloadsScreen } from "./screens/DownloadsScreen";
import { LibraryScreen } from "./screens/LibraryScreen";
import { SettingsScreen } from "./screens/SettingsScreen";
import { COLORS } from "./theme";

const Stack = createNativeStackNavigator();
const Tabs = createBottomTabNavigator();

function HomeStack() {
  return (
    <Stack.Navigator screenOptions={{ headerShown: false }}>
      <Stack.Screen name="Home" component={HomeScreen} />
      <Stack.Screen name="Results" component={ResultsScreen} />
      <Stack.Screen name="Options" component={OptionsScreen} />
    </Stack.Navigator>
  );
}

function RootTabs() {
  return (
    <Tabs.Navigator
      screenOptions={{
        headerShown: false,
        tabBarActiveTintColor: COLORS.cta,
        tabBarInactiveTintColor: COLORS.muted,
        tabBarStyle: {
          borderTopColor: COLORS.border,
          backgroundColor: COLORS.surface
        }
      }}
    >
      <Tabs.Screen name="Search" component={HomeStack} />
      <Tabs.Screen name="Downloads" component={DownloadsScreen} />
      <Tabs.Screen name="Library" component={LibraryScreen} />
      <Tabs.Screen name="Settings" component={SettingsScreen} />
    </Tabs.Navigator>
  );
}

export function AppNavigation() {
  return (
    <NavigationContainer>
      <RootTabs />
    </NavigationContainer>
  );
}
