import React from "react";
import { View, Text, StyleSheet, TouchableOpacity } from "react-native";

interface MentorCardProps {
  name: string;
  field: string;
  tags?: string[];
  score?: number;
  onPress?: () => void;
}

export const MentorCard: React.FC<MentorCardProps> = ({ name, field, tags, score, onPress }) => {
  return (
    <TouchableOpacity onPress={onPress} style={styles.card}>
      <View style={styles.header}>
        <View style={styles.avatar}>
          <Text style={styles.avatarText}>{name.charAt(0)}</Text>
        </View>
        {score !== undefined && (
          <View style={styles.badge}>
            <Text style={styles.badgeText}>{(score * 100).toFixed(0)}% Match</Text>
          </View>
        )}
      </View>
      
      <Text style={styles.name}>{name}</Text>
      <Text style={styles.field}>{field}</Text>
      
      <View style={styles.tagContainer}>
        {tags?.slice(0, 3).map((tag) => (
          <View key={tag} style={styles.tag}>
            <Text style={styles.tagText}>{tag}</Text>
          </View>
        ))}
      </View>
    </TouchableOpacity>
  );
};

const styles = StyleSheet.create({
  card: {
    padding: 24,
    backgroundColor: "#ffffff",
    borderRadius: 28,
    marginBottom: 20,
    borderWidth: 1,
    borderColor: "#f8fafc",
    shadowColor: "#1e293b",
    shadowOffset: { width: 0, height: 10 },
    shadowOpacity: 0.05,
    shadowRadius: 20,
    elevation: 4,
    flexDirection: "column",
  },
  header: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "flex-start",
    marginBottom: 20,
  },
  avatar: {
    width: 64,
    height: 64,
    borderRadius: 20,
    backgroundColor: "#f1f5f9",
    alignItems: "center",
    justifyContent: "center",
    borderWidth: 2,
    borderColor: "#ffffff",
    shadowColor: "#000",
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
  },
  avatarText: {
    fontSize: 26,
    fontWeight: "900",
    color: "#4f46e5",
  },
  badge: {
    backgroundColor: "#f5f3ff",
    paddingHorizontal: 14,
    paddingVertical: 8,
    borderRadius: 14,
    borderWidth: 1,
    borderColor: "#e0e7ff",
  },
  badgeText: {
    fontSize: 10,
    fontWeight: "900",
    color: "#6366f1",
    textTransform: "uppercase",
    letterSpacing: 1,
  },
  name: {
    fontSize: 22,
    fontWeight: "900",
    color: "#0f172a",
    letterSpacing: -0.8,
  },
  field: {
    fontSize: 14,
    color: "#64748b",
    fontWeight: "600",
    marginTop: 2,
  },
  tagContainer: {
    flexDirection: "row",
    flexWrap: "wrap",
    marginTop: 20,
    gap: 8,
  },
  tag: {
    backgroundColor: "#f8fafc",
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 10,
    borderWidth: 1,
    borderColor: "#f1f5f9",
  },
  tagText: {
    fontSize: 10,
    fontWeight: "700",
    color: "#475569",
    textTransform: "uppercase",
  },
});
