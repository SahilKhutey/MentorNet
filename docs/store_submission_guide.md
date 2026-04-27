# 🚀 MentorNet Store Submission Guide

This guide outlines the requirements and steps for publishing MentorNet to the major app stores.

## 1. Google Play Store (Android)

**Requirements:**

- Google Play Developer Account ($25 one-time)
- 4,000-character description
- At least 2 phone screenshots, 1 tablet screenshot
- Privacy Policy URL

**Build Command:**

```bash
eas build --platform android --profile production
```

**Submission:** Upload the `.aab` file to the Google Play Console.

---

## 2. Apple App Store (iOS)

**Requirements:**

- Apple Developer Program ($99/year)
- App Store Connect account
- 10 screenshots (iPhone & iPad)
- Support URL & Marketing URL

**Build Command:**

```bash
eas build --platform ios --profile production
```

**Submission:** Upload using Transporter or Xcode to App Store Connect.

---

## 3. Microsoft Store (Windows)

**Requirements:**

- Microsoft Partner Center Account
- Windows App SDK
- App Identity (Name, Publisher, Package Family Name)

**Build Command:**

```bash
npx react-native run-windows --release
```

**Submission:** Package as `.msix` and upload to Partner Center.

---

## 4. Universal Assets Required

- **Icon**: 1024x1024 px (PNG)
- **Splash Screen**: 2732x2732 px (PNG)
- **Feature Graphic**: 1024x500 px (Android specific)
- **Promotional Video**: (Optional but recommended)

---

## ✅ Deployment Checklist

- [ ] Version number bumped in `app.json`
- [ ] Analytics verified in production mode
- [ ] Deep linking configured for `mentornet://`
- [ ] Terms of Service & Privacy Policy hosted on [web/privacy](https://mentornet.ai/privacy)
