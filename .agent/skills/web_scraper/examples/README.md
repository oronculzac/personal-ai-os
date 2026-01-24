# Web Scraper Skill Examples

This skill leverages Antigravity's browser automation to extract data from websites.

## Example 1: Product Scraping

**Task**: Extract product listings from an e-commerce site

**Browser Subagent Task**:
```
Navigate to https://example-shop.com/products
Wait for product grid to load (selector: '.product-grid')
Extract all products:
- Name from '.product-title' text
- Price from '.product-price' text  
- Image URL from 'img.product-image' src attribute
- Product link from 'a.product-link' href attribute
Return as JSON array with keys: name, price, image_url, product_url
```

**Expected Output**:
```json
[
  {
    "name": "Wireless Mouse",
    "price": "$29.99",
    "image_url": "https://example-shop.com/images/mouse.jpg",
    "product_url": "https://example-shop.com/products/wireless-mouse"
  }
]
```

## Example 2: News Article Headlines

**Task**: Collect latest news headlines

**Browser Subagent Task**:
```
Navigate to https://news-site.com
Wait for article feed to appear
Extract all article cards:
- Headline from 'h2.article-title'
- Summary from 'p.article-excerpt'  
- Author from 'span.author-name'
- Published date from 'time.publish-date' datetime attribute
- Article URL from parent 'a' href
Return as JSON with keys: headline, summary, author, published_date, url
```

## Example 3: Table Data Extraction

**Task**: Extract tabular data from a page

**Browser Subagent Task**:
```
Navigate to https://data-site.com/statistics
Find table with id 'data-table'
Extract table headers from 'thead th' elements
Extract all table rows from 'tbody tr'
For each row, get all cell values from 'td' elements
Return structured data with headers as keys and rows as array of objects
```

## Usage with Other Skills

### Create Excel Report from Scraped Data

```
1. Use Web Scraper to extract product data
2. Save results to JSON
3. Use Excel Generator to create formatted spreadsheet:
   - Import JSON data  
   - Add headers and formatting
   - Create summary statistics
   - Save as products_report.xlsx
```

### Multi-Skill Workflow

```
User: "Scrape this product comparison site and create an Excel report"

Workflow:
1. Web Scraper: Extract product comparison table
2. Excel Generator: Create formatted spreadsheet
3. File Organizer: Save to appropriate folder
```

## Best Practices

- Always respect robots.txt
- Use reasonable delays between requests (2-3 seconds)
- Limit concurrent requests
- Handle errors gracefully  
- Clean and validate exported data
- Provide clear attribution

## Notes

- Scraping sessions are automatically recorded as videos
- Results are saved to artifacts directory
- Dynamic content is fully supported via browser automation
- No need for complex selector logic - browser sees rendered page
