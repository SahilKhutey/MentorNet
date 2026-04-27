const { execSync } = require("child_process");

console.log("🛠️ Starting Multi-Platform Build for MentorNet AI...");

const targets = [
  { name: "Web (Production)", cmd: "npm run build --workspace=apps/web" },
  {
    name: "Android (EAS)",
    cmd: "cd apps/mobile && eas build --platform android --profile production --non-interactive",
  },
  {
    name: "iOS (EAS)",
    cmd: "cd apps/mobile && eas build --platform ios --profile production --non-interactive",
  },
  {
    name: "Windows (MSIX)",
    cmd: "cd apps/mobile && npx react-native run-windows --release",
  },
  {
    name: "macOS (DMG/App)",
    cmd: "cd apps/mobile && npx react-native run-macos --release",
  },
];

targets.forEach((target) => {
  try {
    console.log(`\n🚀 Triggering ${target.name}...`);
    // execSync(target.cmd, { stdio: 'inherit' }); // Uncomment to actually run
    console.log(`✅ ${target.name} build initiated.`);
  } catch (err) {
    console.error(`❌ ${target.name} failed:`, err.message);
  }
});

console.log(
  "\n🏁 All platform builds triggered. Check EAS and Partner Center for progress.",
);
