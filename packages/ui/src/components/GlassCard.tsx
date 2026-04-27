import React from "react";
import { View, StyleSheet, ViewProps, Platform } from "react-native";
import { tokens } from "../theme/tokens";

interface GlassCardProps extends ViewProps {
  intensity?: number;
  variant?: "low" | "medium" | "high";
  children: React.ReactNode;
}

/**
 * GlassCard: A premium glassmorphic container for the Academic Atelier system.
 * Uses background shifts and negative space for boundaries.
 */
export const GlassCard: React.FC<GlassCardProps> = ({ 
  intensity = 20, 
  variant = "medium", 
  children, 
  style, 
  ...props 
}) => {
  const getBackgroundColor = () => {
    switch (variant) {
      case "low": return tokens.colors.surfaceContainerLow;
      case "high": return tokens.colors.surfaceContainerHighest;
      default: return tokens.colors.surfaceContainer;
    }
  };

  return (
    <View 
      style={[
        styles.container, 
        { backgroundColor: getBackgroundColor() },
        style
      ]} 
      {...props}
    >
      {children}
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    borderRadius: tokens.roundness.lg,
    padding: tokens.spacing.lg,
    // Note: In a real Expo environment, we would use <BlurView> here.
    // We simulate depth using elevated surface tokens and subtle shadows.
    ...Platform.select({
      ios: {
        shadowColor: tokens.colors.onPrimary,
        shadowOffset: { width: 0, height: 8 },
        shadowOpacity: 0.1,
        shadowRadius: 12,
      },
      android: {
        elevation: 4,
      },
      web: {
        backdropFilter: "blur(24px)",
        boxShadow: "0 8px 32px 0 rgba(0, 0, 0, 0.37)",
      }
    }),
  },
});
