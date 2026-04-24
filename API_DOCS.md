# API Documentation Overview

MentorNet provides a production-hardened REST API with real-time Socket.io capabilities.

## 🔐 Authentication
All private endpoints require a Bearer JWT in the `Authorization` header.

### Login / Signup
- `POST /api/v1/auth/signup`
- `POST /api/v1/auth/login`
- `POST /api/v1/auth/refresh` (Uses HttpOnly Cookies)

## 🧠 Discovery & AI
- `GET /api/v1/search/semantic?q=AI Expert`
- `GET /api/v1/recommendation/trending` (Aggregated ranking)

## 📅 Bookings & Sessions
- `POST /api/v1/booking/create`
- `GET /api/v1/session/{id}/meeting-link`

## 🛡️ Privacy (GDPR)
- `GET /api/v1/user/me/export`: Export personal data.
- `DELETE /api/v1/user/me/purge`: Permanently delete account.

## 📊 Monitoring
- `GET /metrics`: Prometheus metrics.
- `GET /health`: Deep system health (DB, Redis).

Full interactive documentation is available at `/docs` when running the backend.
