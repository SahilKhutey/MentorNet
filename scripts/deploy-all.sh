#!/bin/bash

# --- MentorNet Production Deployment Script ---

echo "🚀 Starting Production Deployment for MentorNet AI..."

# 1. Backend (Docker)
echo "📦 Building and starting Backend services..."
docker-compose up -d --build

# 2. Database Migrations (Example)
echo "🗄️ Running database migrations..."
docker-compose exec backend alembic upgrade head

# 3. Web (Vercel CLI)
echo "🌐 Deploying Web App to Vercel..."
cd apps/web
vercel --prod --yes

# 4. Mobile (EAS CLI)
echo "📱 Starting Mobile Build (Android/iOS)..."
cd ../mobile
eas build --platform all --profile production --non-interactive

echo "✅ Deployment commands triggered successfully!"
