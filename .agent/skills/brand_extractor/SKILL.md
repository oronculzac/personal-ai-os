---
name: Brand Extractor
description: Extract brand identity from websites using Firecrawl MCP branding format. Use when the user wants to analyze brand colors, typography, logos, and design systems from a website URL. Triggers include "extract brand from", "get branding", "analyze brand identity", "brand style guide", or "design system from website".
---

# Brand Extractor Skill

## Purpose

Extract comprehensive brand identity (colors, typography, spacing, logos) from any website using Firecrawl's branding format. Can generate brand style guides and analyze Vietnamese company branding.

## Capabilities

1. **Single URL Extraction** - Extract brand identity from one website
2. **Batch Extraction** - Extract from multiple URLs
3. **Vietnamese Brand Database** - Lookup known VN brand URLs
4. **Brand Style Guide** - Generate PDF reports (integrates with PDF skill)

## Instructions

### 1. Extract Brand from Single URL

Use Firecrawl MCP `scrape` with branding format:

```
firecrawl_scrape:
  url: "https://example.com"
  formats: ["branding"]
```

Returns a BrandingProfile with:
- `colorScheme`: "dark" or "light"
- `colors`: primary, secondary, accent, background, text colors
- `typography`: fontFamilies, fontSizes, fontWeights
- `spacing`: baseUnit, borderRadius
- `images`: logo, favicon, ogImage

### 2. Batch Brand Extraction

For multiple URLs, call scrape sequentially and compile results:

```python
brands = []
for url in urls:
    result = firecrawl_scrape(url, formats=["branding"])
    brands.append({
        "url": url,
        "branding": result["branding"]
    })
```

### 3. Vietnamese Brand Database

Common Vietnamese brands with official URLs:

| Brand | Category | URL |
|-------|----------|-----|
| Viettel | Telecom | https://viettel.com.vn |
| Vinamilk | Dairy | https://www.vinamilk.com.vn |
| VinMart | Retail | https://winmart.vn |
| Masan | FMCG | https://www.masangroup.com |
| FPT | Tech | https://fpt.com.vn |
| Vietcombank | Banking | https://vietcombank.com.vn |
| BIDV | Banking | https://www.bidv.com.vn |
| VPBank | Banking | https://vpbank.com.vn |
| Vinhomes | Real Estate | https://vinhomes.vn |
| TH True Milk | Dairy | https://www.thmilk.vn |
| Sabeco | Beverage | https://www.sabeco.com.vn |
| VNPT | Telecom | https://vnpt.com.vn |
| MobiFone | Telecom | https://mobifone.vn |

### 4. Generate Brand Style Guide

After extracting branding, generate a PDF style guide:

1. Extract branding using Firecrawl
2. Use PDF skill (reportlab) to create style guide with:
   - Color palette swatches
   - Typography specimens
   - Logo/favicon display
   - Spacing guidelines

Example workflow:
```
1. Extract: firecrawl_scrape(url, formats=["branding"])
2. Parse colors, typography, spacing from response
3. Generate PDF using reportlab (see PDF skill)
```

## Output Formats

### JSON (default)
```json
{
  "url": "https://example.com",
  "extracted_at": "2026-01-23T06:30:00Z",
  "branding": {
    "colorScheme": "dark",
    "colors": {
      "primary": "#FF6B35",
      "secondary": "#004E89"
    },
    "typography": {
      "fontFamilies": {
        "primary": "Inter",
        "heading": "Inter"
      }
    }
  }
}
```

### Markdown Report
```markdown
# Brand Analysis: Example.com

## Colors
- Primary: #FF6B35
- Secondary: #004E89

## Typography
- Primary Font: Inter
- Heading Font: Inter

## Theme: Dark Mode
```

## Integration

### With PDF Skill
Generate PDF brand style guides using reportlab.

### With Web Scraper
Combine branding with full page content extraction.

## Notes

- Firecrawl MCP must be available
- Some sites may block scraping
- Logo extraction works best with PNG/JPG formats
- SVG logos may not display in PDF output
