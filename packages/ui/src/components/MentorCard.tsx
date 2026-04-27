import React from "react";
import { View, Text, StyleSheet, TouchableOpacity, Dimensions } from "react-native";
import { tokens } from "../theme/tokens";
import { GlassCard } from "./GlassCard";

interface MentorCardProps {
  name: string;
  field: string;
  tags?: string[];
  score?: number;
  onPress?: () => void;
  style?: any;
}

export const MentorCard: React.FC<MentorCardProps> = ({
  name,
  field,
  tags,
  score,
  onPress,
  style,
}) => {
  return (
    <TouchableOpacity onPress={onPress} activeOpacity={0.8} style={style}>
      <GlassCard variant="medium" style={styles.card}>
        <View style={styles.header}>
          <View style={styles.avatar}>
            <Text style={styles.avatarText}>{name.split(' ').map(n => n[0]).join('')}</Text>
          </View>
          {score !== undefined && (
            <View style={styles.badge}>
              <Text style={styles.badgeText}>
                {(score * 100).toFixed(0)}% MATCH
              </Text>
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
      </GlassCard>
    </TouchableOpacity>
  );
};

const styles = StyleSheet.create({
  card: {
    marginBottom: tokens.spacing.md,
  },
  header: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "flex-start",
    marginBottom: 16,
  },
  avatar: {
    width: 52,
    height: 52,
    borderRadius: tokens.roundness.md,
    backgroundColor: tokens.colors.surfaceContainerHighest,
    alignItems: "center",
    justifyContent: "center",
  },
  avatarText: {
    fontSize: 18,
    fontWeight: "bold",
    color: tokens.colors.onSurface,
  },
  badge: {
    backgroundColor: "rgba(196, 193, 251, 0.1)",
    paddingHorizontal: 10,
    paddingVertical: 6,
    borderRadius: tokens.roundness.sm,
    borderWidth: 1,
    borderColor: "rgba(196, 193, 251, 0.2)",
  },
  badgeText: {
    fontSize: 10,
    fontWeight: "900",
    color: tokens.colors.primary,
    letterSpacing: 0.5,
  },
  name: {
    fontFamily: tokens.typography.heading,
    fontSize: 18,
    fontWeight: "800",
    color: tokens.colors.onSurface,
    letterSpacing: -0.4,
  },
  field: {
    fontFamily: tokens.typography.body,
    fontSize: 13,
    color: tokens.colors.onSurfaceVariant,
    marginTop: 2,
  },
  tagContainer: {
    flexDirection: "row",
    flexWrap: "wrap",
    marginTop: 16,
    gap: 8,
  },
  tag: {
    backgroundColor: tokens.colors.surfaceContainerLow,
    paddingHorizontal: 8,
    paddingVertical: 4,
    borderRadius: tokens.roundness.sm,
  },
  tagText: {
    fontSize: 9,
    fontWeight: "700",
    color: tokens.colors.onSurfaceVariant,
    textTransform: "uppercase",
  },
});
