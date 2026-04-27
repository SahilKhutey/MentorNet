/**
 * Academic Atelier Design System Tokens
 * North Star: "The Scholarly Prism"
 * 
 * Boundaries are defined through background shifts and negative space, 
 * not 1px solid borders.
 */

export const tokens = {
  colors: {
    // Core Palette
    background: "#051425",
    primary: "#c4c1fb", // Scholarly Indigo
    secondary: "#c7c4dd", // Muted Slate
    tertiary: "#ddb7ff", // AI / Innovation (Purple)
    
    // Surface Hierarchy (Scholarly Prism)
    surface: "#051425", // Base layer
    surfaceContainerLow: "#0d1c2e", // Layout sections
    surfaceContainer: "#122032", // Interactive backgrounds
    surfaceContainerHigh: "#1d2b3d", // Lifted cards
    surfaceContainerHighest: "#283648", // Floating elements (Glass)
    
    // AI Integration
    aiContainer: "#35005f", // Backdrop for AI insights
    aiGlow: "rgba(168, 85, 247, 0.3)", // Vibrant purple glow
    
    // Text & Interaction
    onSurface: "#d5e3fc", // Primary reading
    onSurfaceVariant: "#c8c5d0", // Muted data
    onPrimary: "#2d2a5b", // High contrast text on indigo
    outline: "#928f9a",
    outlineVariant: "rgba(71, 70, 79, 0.15)", // Ghost Border
    
    // Functional
    error: "#ffb4ab",
    success: "#86efac",
  },
  
  typography: {
    heading: "Manrope", // Editorial authority
    body: "Inter", // Functional precision
    
    scale: {
      display: {
        fontSize: 40,
        fontWeight: "800",
        letterSpacing: -0.8,
        lineHeight: 48,
      },
      headline: {
        fontSize: 24,
        fontWeight: "700",
        letterSpacing: -0.4,
        lineHeight: 32,
      },
      body: {
        fontSize: 16,
        fontWeight: "500",
        lineHeight: 24,
      },
      label: {
        fontSize: 12,
        fontWeight: "700",
        letterSpacing: 0.6,
        textTransform: "uppercase",
      },
    }
  },
  
  spacing: {
    xs: 4,
    sm: 8,
    md: 16,
    lg: 24,
    xl: 32,
    xxl: 48,
  },
  
  roundness: {
    sm: 8,
    md: 16,
    lg: 24,
    xl: 32,
    full: 9999,
  },
  
  blur: {
    glass: 24,
    glow: 32,
  }
};
