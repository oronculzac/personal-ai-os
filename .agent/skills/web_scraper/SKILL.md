---
name: Web Scraper
description: Extract data from websites using browser automation, with support for dynamic content and structured data collection
version: 1.1.0
triggers:
  - scrape website
  - extract data from
  - get content from
  - crawl website
  - fetch web data
  - collect information from
examples:
  - "Scrape product prices from this website"
  - "Extract article headlines from TechCrunch"
  - "Get all links from this page"
  - "Collect data from this table"
context_hints:
  - user mentions web scraping or data extraction
  - user wants to get data from a website
  - user mentions crawling or collecting web data
  - user has a URL they want data from
priority: 6
conflicts_with: []
dependencies:
  - browser automation (built-in)
capabilities:
  - web_scraping
  - data_extraction
  - browser_automation
  - structured_data_collection
  - dynamic_content_handling
auto_load: true
---

# Web Scraper Skill

## Purpose

Extract structured data from websites using Antigravity's powerful browser automation capabilities. Handles dynamic content, JavaScript-heavy sites, and provides clean data extraction with multiple output formats.

## Capabilities

### Core Features
- **Browser Automation**: Use Antigravity's browser_subagent for full browser control
- **Dynamic Content**: Handle JavaScript-rendered content naturally
- **Data Extraction**: Extract text, links, images, tables, and structured data
- **Multiple Formats**: Output as JSON, CSV, Excel, or Markdown
- **Pagination**: Navigate through multi-page results
- **Authentication**: Handle login-required sites
- **Rate Limiting**: Respectful scraping with delays
- **Error Handling**: Robust retry logic and fallbacks

## Instructions

When the user requests web scraping tasks, follow these steps:

### 1. Understand the Request

**Identify what to extract**:
- Text content (articles, descriptions, prices)
- Structured data (tables, lists)
- Links and URLs
- Images and media
- Metadata (titles, dates, authors)

**Example requests**:
```
User: "Scrape product prices from this website"
→ Extract: product names, prices, availability

User: "Get all article titles from this news site"
→ Extract: headlines, links, publication dates

User: "Extract contact information from these pages"
→ Extract: emails, phone numbers, addresses
```

### 2. Plan the Browser Task

Create a clear browser subagent task:

**Components**:
1. **Navigate** to target URL(s)
2. **Wait** for content to load (if dynamic)
3. **Extract** specific elements using selectors
4. **Navigate** to next page if needed (pagination)
5. **Return** structured data

**Browser Subagent Pattern**:
```
Use browser_subagent with clear task:
1. Navigate to [URL]
2. Wait for [selector] to appear
3. Extract all elements matching [selector]
4. For each element, get: [text/link/attribute]
5. Return as JSON array with keys: [field1, field2, ...]
```

### 3. Execute Browser Task

**Example browser task**:
```
Task: "Navigate to https://example.com/products. 
Wait for product cards to load (selector: '.product-card'). 
Extract from each card:
- Product name from '.product-title'
- Price from '.price'
- Link from 'a' href attribute
Return as JSON array with keys: name, price, url"
```

### 4. Format and Save Results

**Output Options**:
- **JSON**: Structured data for further processing
- **CSV**: Spreadsheet-compatible format
- **Excel**: Using Excel Generator skill
- **Markdown**: Readable report format

### 5. Handle Common Scenarios

**Dynamic Content**:
```
"Wait for selector '.content-loaded' before extracting"
"Scroll to bottom to trigger lazy loading"
"Click 'Load More' button to reveal additional content"
```

**Pagination**:
```
"Extract data from page 1, then click 'Next' button"
"Repeat extraction for pages 1-10"
"Stop when 'Next' button is disabled"
```

**Authentication**:
```
"Navigate to login page"
"Fill username field with [username]"
"Fill password field with [password]"
"Click login button"
"Wait for redirect to dashboard"
"Then proceed with scraping"
```

## Usage Examples

### Example 1: Scrape Product Listings

**Request**: "Scrape product names and prices from this e-commerce site"

**Action**:
1. Ask user for URL
2. Create browser subagent task:
   ```
   Navigate to [URL]
   Wait for product grid to load
   Extract all products with:
   - Name from h2.product-name
   - Price from span.price
   - Link from a.product-link href
   Return as JSON
   ```
3. Receive data from browser agent
4. Format as CSV or Excel
5. Save to file
6. Report: "Extracted 50 products to products.csv"

### Example 2: News Article Collection

**Request**: "Get all article headlines from TechCrunch homepage"

**Action**:
1. Create browser task:
   ```
   Navigate to https://techcrunch.com
   Wait for article feed to load
   Extract all articles:
   - Headline from h2.post-title
   - Summary from p.excerpt
   - URL from a href
   - Date from time.published
   Return as JSON array
   ```
2. Process returned data
3. Create markdown report or Excel file
4. Save: `techcrunch_articles_2026-01-15.md`

### Example 3: Multi-Page Scraping

**Request**: "Scrape the first 5 pages of search results"

**Action**:
1. Create browser task with pagination:
   ```
   Navigate to search URL
   For pages 1 to 5:
     - Extract all results on current page
     - Click 'Next' button
     - Wait for new results to load
   Return all collected data as JSON
   ```
2. Compile results
3. Save to Excel using Excel Generator skill
4. Report: "Extracted 250 results across 5 pages"

### Example 4: Table Extraction

**Request**: "Extract the data table from this page"

**Action**:
1. Create browser task:
   ```
   Navigate to [URL]
   Find table element
   Extract headers from thead
   Extract all rows from tbody
   Return as structured JSON with headers and rows
   ```
2. Convert to CSV or Excel
3. Maintain column structure
4. Save with proper headers

### Example 5: Image Collection

**Request**: "Download all product images from this page"

**Action**:
1. Browser task:
   ```
   Navigate to [URL]
   Find all img tags in product grid
   Extract src attributes
   Return array of image URLs
   ```
2. Create image download list
3. Optionally: Download images to folder
4. Generate manifest file

## Integration with Other Skills

### With Excel Generator

**Workflow**: "Scrape product data and create Excel report"
1. Web Scraper: Extract product information
2. Excel Generator: Create formatted spreadsheet with:
   - Data table
   - Summary statistics
   - Charts if numeric data available

### With File Organizer

**Workflow**: "Scrape images and organize by category"
1. Web Scraper: Collect image URLs and metadata
2. Download images to folder
3. File Organizer: Sort by category or date

### With Data Analyzer

**Workflow**: "Scrape pricing data and analyze trends"
1. Web Scraper: Collect price history
2. Data Analyzer: Calculate trends, averages
3. Excel Generator: Create report with visualizations

## Browser Automation Best Practices

### Respectful Scraping

**Rate Limiting**:
```
"Wait 2 seconds between page loads"
"Limit to 10 pages per session"
```

**User Agent**:
```
"Use standard browser user agent"
"Identify as legitimate browser"
```

**Robots.txt**:
```
"Check robots.txt before scraping"
"Respect crawl delays specified"
```

### Robust Extraction

**Wait for Content**:
```
"Wait for selector to appear before extracting"
"Maximum wait 10 seconds"
"Fall back to alternative selector if timeout"
```

**Error Handling**:
```
"If selector not found, try alternative: [alt-selector]"
"If page fails to load, retry up to 3 times"
"Return partial results if some pages fail"
```

**Data Cleaning**:
```
"Trim whitespace from extracted text"
"Remove special characters from prices"
"Normalize date formats"
```

## Output Formats

### JSON
```json
{
  "url": "https://example.com",
  "scraped_at": "2026-01-15T09:00:00Z",
  "data": [
    {
      "title": "Product 1",
      "price": "$29.99",
      "url": "https://example.com/product1"
    }
  ]
}
```

### CSV
```csv
title,price,url
"Product 1","$29.99","https://example.com/product1"
"Product 2","$39.99","https://example.com/product2"
```

### Markdown
```markdown
# Scraped Data from example.com
*Collected: 2026-01-15 09:00*

## Results (2 items)

### Product 1
- **Price**: $29.99
- **URL**: https://example.com/product1

### Product 2
- **Price**: $39.99
- **URL**: https://example.com/product2
```

## Safety & Ethics

### Ethical Guidelines

✅ **Do**:
- Respect robots.txt
- Use rate limiting
- Only scrape public data
- Provide attribution
- Check terms of service

❌ **Don't**:
- Scrape personal data without consent
- Bypass authentication illegally
- Overwhelm servers (DDoS)
- Violate copyright
- Ignore rate limits

### Privacy

- Don't scrape personal information (emails, phones) without permission
- Don't store sensitive data
- Respect privacy policies
- Get user consent for data collection

## Error Handling

**Common Issues**:

**Page Not Loading**:
```
"Retry with longer timeout"
"Check if URL is correct"
"Verify internet connection"
```

**Selector Not Found**:
```
"Try alternative selector"
"Check if page structure changed"
"Use more generic selector"
```

**Rate Limited**:
```
"Increase delay between requests"
"Reduce number of pages"
"Try again later"
```

**Dynamic Content Timeout**:
```
"Increase wait time"
"Scroll to trigger lazy loading"
"Check if JavaScript is blocked"
```

## Notes

- Uses Antigravity's built-in browser_subagent (no external dependencies)
- Works with JavaScript-heavy single-page applications
- Automatic video recording of scraping session
- Respects Antigravity's browser automation safety features
- Results are automatically saved to artifacts directory
