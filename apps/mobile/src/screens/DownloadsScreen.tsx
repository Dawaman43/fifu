import React from "react";
import { View, Text, StyleSheet, ScrollView } from "react-native";
import { COLORS, SPACING, TYPO } from "../theme";
import { Card } from "../components/Card";
import { SecondaryButton } from "../components/SecondaryButton";
import { ProgressBar } from "../components/ProgressBar";
import { MOCK_ACTIVE } from "../mock";

import { apiGet } from "../api/client";

export function DownloadsScreen({ route }: { route: any }) {
  const { channel, isSingleVideo = false } = route.params || {};
  const [job, setJob] = React.useState<any>(null);
  const [loading, setLoading] = React.useState(true);

  React.useEffect(() => {
    // Initial fetch
    fetchJob();
    
    // Polling interval
    const interval = setInterval(fetchJob, 2000);
    return () => clearInterval(interval);
  }, []);

  const fetchJob = async () => {
    try {
      // We use a demo ID if none provided
      const id = "a1"; 
      const data = await apiGet(`/api/jobs/${id}`);
      setJob(data);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <View style={[styles.screen, { justifyContent: "center", alignItems: "center" }]}>
        <Text style={styles.title}>Loading Status...</Text>
      </View>
    );
  }

  return (
    <ScrollView style={styles.screen} contentContainerStyle={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>Downloads</Text>
        <Text style={styles.subtitle}>{isSingleVideo ? "Individual Video" : (channel?.name || "Queue")}</Text>
      </View>

      <Card>
        <Text style={styles.label}>Overall Progress</Text>
        <ProgressBar value={job?.progress || 0} />
        <Text style={styles.meta}>
          {job?.completed || 0} / {job?.total || 0} videos downloaded ({job?.status || "queued"})
        </Text>
      </Card>

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Active Threads</Text>
        {job?.active && job.active.length > 0 ? (
          job.active.map((text: string, idx: number) => (
            <Card key={idx}>
              <Text style={styles.listTitle}>{text}</Text>
              <ProgressBar value={job?.progress} />
              <Text style={styles.meta}>{job?.speed} • {job?.eta}</Text>
            </Card>
          ))
        ) : (
          <Card>
            <Text style={styles.meta}>No active downloads</Text>
          </Card>
        )}
      </View>

      <Card>
        <Text style={styles.sectionTitle}>Recent Log</Text>
        <Text style={styles.meta}>[SYSTEM] Connected to backend...</Text>
        <Text style={styles.meta}>[STATUS] Job {job?.id} is {job?.status}</Text>
        {job?.status === "completed" && <Text style={styles.meta}>[DONE] All tasks finished.</Text>}
      </Card>

      <SecondaryButton label="Stop Queue" onPress={() => {}} />
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
  label: {
    fontSize: TYPO.body,
    fontWeight: "600",
    color: COLORS.text,
    marginBottom: SPACING.sm
  },
  section: {
    gap: SPACING.sm
  },
  sectionTitle: {
    fontSize: TYPO.h3,
    fontWeight: "600",
    color: COLORS.text
  },
  listTitle: {
    color: COLORS.text,
    fontSize: TYPO.body,
    fontWeight: "600",
    marginBottom: SPACING.sm
  },
  meta: {
    color: COLORS.muted,
    fontSize: TYPO.small,
    marginTop: SPACING.xs
  }
});
