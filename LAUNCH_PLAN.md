# 🚀 MentorNet: Master Launch Plan

This document outlines the strategic roadmap for transitioning MentorNet from a hardened development state to a global production environment.

## 📅 Timeline: T-Minus 24 Hours

### Phase 0: Infrastructure Ignition (T-24h)
- [ ] **Secret Injection**: Inject production `SECRET_KEY`, `FIELD_ENCRYPTION_KEY`, and `SENTRY_DSN` into the production environment.
- [ ] **DB Initialization**: Run `python scripts/init_db.py` on the production Postgres cluster.
- [ ] **Vector Index Warming**: Ensure the FAISS index is synced with the production DB.
- [ ] **SSL Verification**: Confirm Let's Encrypt certificates are active for `api.mentornet.ai` and `mentornet.ai`.

### Phase 1: Soft Launch (T-12h)
- [ ] **Internal Testing**: Invite the "Alpha 100" users (internal team and stakeholders).
- [ ] **Audit Review**: Monitor `audit.log` for any anomalies during the first 100 signups.
- [ ] **Rate Limit Tuning**: Verify that the tiered rate limits are not blocking legitimate internal users.

## 🚀 The Launch Sequence (T-0)

### 1. Deployment Execution
- [ ] **Docker Ignition**: `docker-compose -f docker-compose.prod.yml up -d --scale backend=3 --scale worker=2`
- [ ] **Nginx Reload**: Verify load balancing is distributing traffic across all 3 replicas.

### 2. Growth Engine Activation
- [ ] **Referral Loop Live**: Enable the `ReferralSystem` for all new signups.
- [ ] **Public Profiles Public**: Release the sitemap for mentor profiles to Google Search Console for SEO indexing.
- [ ] **Initial Social Burst**: Post the first "Insight Sharing" card from the founder's account.

## 📊 Post-Launch Monitoring (First 24 Hours)

### Observability Benchmarks
- **Error Rate**: < 0.1% (Sentry)
- **API Latency**: < 150ms P95 (Prometheus)
- **DB Pool Health**: < 50% utilization (Grafana)
- **AI Task Queue**: < 2s backlog (Flower)

## 🛡️ Contingency & Safety (Circuit Breakers)

- **AI Failure**: If FAISS latency exceeds 500ms, the system will automatically fallback to "Simple Keyword Ranking."
- **DB Pressure**: If Postgres CPU > 80%, Nginx will temporarily enable "Queue Mode" for non-critical requests.
- **Security Breach**: If 10+ failed login attempts from a single IP, the IP is blacklisted in Redis for 24 hours.

## 🏁 Future Milestones (Next 30 Days)
1. **Mobile App Release**: Submit `@mentornet/mobile` to App Store/Play Store.
2. **Stripe Integration**: Activate the premium mentor booking payments.
3. **Enterprise Dashboard**: Launch the organization-level insights for universities.

---

**MentorNet is officially ready for liftoff.**
