---
type: project
status: active
git_path: projects/altery-tools
github: https://github.com/oronculzac/altery-tools
neon_project_id: orange-boat-25857106
created: 2026-01-24
---

# Altery Organic Tools Suite

SEO-driven utility tools for organic traffic to altery.com, starting with Coverage & Rails Finder.

## 🔗 Links
- [[Local Folder]]: `projects/altery-tools`
- [GitHub](https://github.com/oronculzac/altery-tools) (private)
- [Neon Console](https://console.neon.tech/app/projects/orange-boat-25857106)

## 🏗️ Tech Stack
- **Frontend**: Next.js 14 (App Router)
- **Database**: Neon Postgres (Serverless)
- **Automation**: n8n (self-hosted)
- **Deployment**: Vercel

## 📊 MVP: Coverage & Rails Finder

**User Story**: "Can I send/receive money between X and Y with Altery, and via which rails?"

### Inputs
- Customer type: personal | business
- Send country, Receive country
- Optional: currency, route type preference

### Outputs
- Verdict: available / limited / not available
- Routes list (ranked)
- "What you'll need" checklist
- Deep links to Help Centre

## 📝 Progress Notes

### 2026-01-24 - Project Initialized
- Created folder structure and Git repo
- Created private GitHub repo
- Created Neon database with schema:
  - `sources` - track data origins
  - `country_eligibility` - personal/business support
  - `bank_transfer_country_coverage` - corridor support
  - `payment_rails` - SEPA/FPS/SWIFT/LOCAL
  - `card_transfer_coverage` - Visa/MC support
  - `tool_cache` - response caching
  - `audit_log` - admin operations

## 🗓️ Next Steps
- [ ] Initialize Next.js application
- [ ] Implement `/api/coverage-rails` endpoint
- [ ] Create frontend tool UI
- [ ] Set up n8n webhooks for data sync
