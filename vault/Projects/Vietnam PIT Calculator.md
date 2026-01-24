---
type: project
status: active
priority: high
created: 2026-01-22
tags:
  - vietnam
  - tax
  - calculator
  - ai
  - nextjs
linear: https://linear.app/linear-home-workspace/project/vietnam-pit-calculator-24645c967ffb
github: https://github.com/oronculzac/vietnam-pit-calculator
---

# Vietnam PIT Calculator

A webapp helping expats in Vietnam estimate Personal Income Tax (PIT) with audit-friendly breakdowns, AI explanations, and versioned tax rules.

## Quick Links
- **GitHub**: [oronculzac/vietnam-pit-calculator](https://github.com/oronculzac/vietnam-pit-calculator)
- **Linear Project**: [Vietnam PIT Calculator](https://linear.app/linear-home-workspace/project/vietnam-pit-calculator-24645c967ffb)
- **Local Dev**: `cd projects/vietnam-pit-calculator/src/web && npm run dev`

## Status

| Phase | Status | Issues |
|-------|--------|--------|
| 1. Foundation | ✅ Complete | LIN-28 |
| 2. Rules Engine | ✅ Complete | LIN-29 |
| 3. Calculator Core | ✅ Complete | LIN-30 |
| 4. Web Application | ✅ Complete | LIN-31 |
| 5. AI Augmentation | ✅ Complete | LIN-32 |
| 6. Testing | ✅ 68/68 passing | LIN-33 |
| 7. Enhanced AI | 🔄 In Progress | LIN-34 to LIN-37 |
| 8. Feature Audit | ✅ Complete | - |

## Recent Additions (Jan 2026 Audit)

### ✅ Completed
- **Gross-to-Net Conversion** - Zone-based insurance calculation with expat support
- **Net-to-Gross Calculator** - Binary search algorithm for reverse calculation
- **USD/VND Currency Toggle** - Display in either currency (rate: ₫25,400/$1)
- **Employer Cost View** - Total employer cost breakdown in results
- **Brand Extractor Skill** - Firecrawl-based brand extraction for VN companies

### 🔄 Planned
- [ ] Net→Gross input field in Income step
- [ ] PDF export for calculations
- [ ] Share calculation via URL
- [ ] Live exchange rate from Vietcombank

## Tech Stack
- **Frontend**: Next.js 15, TypeScript, Tailwind CSS v4, shadcn/ui
- **AI**: Groq (Llama 3.3 70B), Perplexity (web search)
- **Validation**: Zod schemas for rules and inputs
- **Testing**: Node test runner, 68 regression tests

## 2026 Tax Rules Applied
- **Taxpayer Deduction**: 15,500,000 VND/month
- **Dependent Deduction**: 6,200,000 VND/month
- **Progressive Brackets**: 5%, 10%, 20%, 30%, 35%
- **Non-Resident Rate**: 20% flat
- **10% Withholding**: ≥2M VND, no/short contract

## Key Files
```
projects/vietnam-pit-calculator/
├── src/engine/calculator.ts     # Deterministic PIT + Gross-to-Net
├── src/rules/VN_PIT_2026.json   # 2026 tax constants
├── src/web/src/lib/ai/          # Groq + Perplexity integration
├── src/web/src/lib/currency.ts  # VND/USD conversion utilities
└── tests/scenarios/             # 68 regression tests
```

## Sources
- Resolution 110/2025/UBTVQH15 (family deductions)
- Circular 111/2013/TT-BTC (general PIT rules)
- Baker McKenzie 2026 Summary (brackets)

