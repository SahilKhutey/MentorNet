# 🌐 MentorNet: Zero-Cost Deployment Guide

Follow these steps to launch the entire MentorNet ecosystem on the live internet for **$0/month**.

---

## 🐘 Phase 1: The Database (Neon.tech)

1. **Sign Up**: Go to [Neon.tech](https://neon.tech) and create a free account.
2. **Create Project**: Name it `mentornet-prod`.
3. **Get Connection String**: 
   - In the dashboard, find the **Connection String** section.
   - Ensure it's set to `Pooled Connection`.
   - Copy the URL (it looks like `postgres://user:pass@ep-cool-name-123.aws.neon.tech/neondb`).
4. **Save this URL** for Phase 2.

---

## 🧠 Phase 2: The Backend API (Render.com)

1. **Sign Up**: Go to [Render.com](https://render.com).
2. **New Web Service**:
   - Click `New +` -> `Web Service`.
   - Connect your MentorNet GitHub repository.
3. **Configure Service**:
   - **Name**: `mentornet-api`
   - **Region**: Select the one closest to you.
   - **Language**: `Docker`
   - **Dockerfile Path**: `backend/Dockerfile.free` (Crucial!)
4. **Add Environment Variables**:
   - Click `Advanced` -> `Add Environment Variable`.
   - `DATABASE_URL`: (Paste your Neon URL from Phase 1)
   - `ENV`: `production`
5. **Deploy**: Render will build the image. Once finished, copy the provided URL (e.g., `https://mentornet-api.onrender.com`).

---

## 🎨 Phase 3: The Frontend Website (Vercel.com)

1. **Sign Up**: Go to [Vercel.com](https://vercel.com).
2. **Import Project**:
   - Click `Add New` -> `Project`.
   - Import your MentorNet GitHub repository.
3. **Configure Build**:
   - **Framework Preset**: `Next.js`
   - **Root Directory**: `apps/web` (Click `Edit` and select the folder).
4. **Add Environment Variables**:
   - `NEXT_PUBLIC_API_URL`: `https://mentornet-api.onrender.com/api/v1` (Use your Render URL from Phase 2).
5. **Deploy**: Vercel will build your "Academic Atelier" UI and provide you with a live URL (e.g., `https://mentornet-web.vercel.app`).

---

## 🧪 Phase 4: Final Connection Test

1. Visit your Vercel URL.
2. Check the **Discovery** or **Recommendations** tab.
3. If data appears, your zero-cost elite infrastructure is successfully linked!

---

### ⚠️ Pro-Tips for Free Tiers
- **Cold Starts**: Render's free tier "sleeps" after 15 mins of inactivity. The first request might take 30 seconds to wake it up.
- **RAM Limits**: If the backend crashes, it's likely hitting the 512MB limit. I've optimized the `Dockerfile.free` to avoid this.
- **Database Limits**: Neon provides 500MB. This is enough for thousands of mentors and users.

**MentorNet is now officially accessible to the world!** 🚀
