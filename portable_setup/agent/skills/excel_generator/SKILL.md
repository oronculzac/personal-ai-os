---
name: Excel Generator
description: Create Excel spreadsheets with formulas, formatting, charts, and multi-sheet support
version: 1.0.0
triggers:
  - create spreadsheet
  - generate excel
  - make xlsx
  - create excel
  - data to excel
  - build spreadsheet
dependencies:
  - openpyxl>=3.0.0
  - pandas>=1.5.0
capabilities:
  - excel_creation
  - formula_generation
  - data_formatting
  - chart_creation
  - multi_sheet_support
auto_load: true
---

# Excel Generator Skill

## Purpose

Generate professional Excel spreadsheets with formulas, formatting, charts, and multiple sheets. This skill enables automated creation of complex Excel workbooks for data analysis, reporting, and documentation.

## Capabilities

### Core Features
- **Multi-sheet workbooks**: Create workbooks with multiple worksheets
- **Formula support**: SUM, AVERAGE, VLOOKUP, IF, COUNT, and more
- **Data formatting**: Colors, fonts, borders, number formats
- **Charts and graphs**: Bar, line, pie, scatter charts
- **Data import**: Load data from CSV, JSON, Python dictionaries, pandas DataFrames
- **Styling**: Cell styles, conditional formatting, merged cells
- **Export formats**: XLSX, CSV

## Instructions

When the user requests Excel-related tasks, follow these steps:

### 1. Identify the Request Type

**Simple data table**:
```
User: "Create a spreadsheet with sales data"
→ Generate basic table with headers and data
```

**Calculated spreadsheet**:
```
User: "Create expense report with totals"
→ Generate table with SUM formulas
```

**Data analysis**:
```
User: "Create spreadsheet from this CSV with charts"
→ Import data, add calculations, create visualizations
```

**Complex workbook**:
```
User: "Create quarterly report workbook with multiple sheets"
→ Multi-sheet workbook with linked formulas
```

### 2. Execute Using Scripts

Use the `excel_builder.py` script for generation:

```powershell
python .agent/skills/excel_generator/scripts/excel_builder.py `
  --output "report.xlsx" `
  --data "data.json" `
  --template "quarterly_report" `
  --charts
```

### 3. Generation Workflow

**Step 1: Prepare Data**
- Gather or structure the data to be included
- Identify columns, headers, data types
- Determine calculations needed

**Step 2: Create Workbook**
- Initialize Excel workbook
- Create necessary sheets
- Set up headers

**Step 3: Populate Data**
- Insert data into cells
- Apply number formatting
- Add formulas

**Step 4: Apply Styling**
- Format headers (bold, background colors)
- Apply borders and alignment
- Set column widths
- Add conditional formatting if needed

**Step 5: Add Charts (if requested)**
- Create chart objects
- Link to data ranges
- Position and style charts

**Step 6: Save and Report**
- Save to specified location
- Provide summary of what was created

### 4. Common Formulas

**Totals**:
```excel
=SUM(B2:B10)
```

**Averages**:
```excel
=AVERAGE(C2:C10)
```

**Conditional**:
```excel
=IF(D2>1000, "High", "Low")
```

**Lookups**:
```excel
=VLOOKUP(A2, Sheet2!A:B, 2, FALSE)
```

**Counts**:
```excel
=COUNTIF(E2:E10, ">100")
```

## Usage Examples

### Example 1: Simple Sales Report

**Request**: "Create a sales report spreadsheet"

**Action**:
1. Create workbook with "Sales Report" sheet
2. Add headers: Date, Product, Quantity, Price, Total
3. Add sample or provided data
4. Add formula for Total column: `=C2*D2`
5. Add SUM at bottom for totals
6. Apply formatting (header bold, currency format)
7. Save as `sales_report.xlsx`

### Example 2: Budget Tracker

**Request**: "Make a monthly budget Excel file"

**Action**:
1. Create sheets: "Income", "Expenses", "Summary"
2. Income sheet: Categories, amounts, formulas
3. Expenses sheet: Categories, budgeted, actual, difference
4. Summary sheet: Total income, total expenses, balance
5. Add formulas linking across sheets
6. Apply conditional formatting (red for over-budget)
7. Save as `budget_tracker.xlsx`

### Example 3: Data Analysis from CSV

**Request**: "Convert this CSV to Excel and add charts"

**Action**:
1. Read CSV using pandas
2. Create workbook with "Data" and "Analysis" sheets
3. Import CSV data to "Data" sheet
4. Add calculated columns (totals, averages, percentages)
5. Create "Analysis" sheet with pivot-style summaries
6. Generate charts (bar chart for categories, line chart for trends)
7. Save as `data_analysis.xlsx`

## Integration with Other Skills

**Combine with Data Analyzer**:
```
User: "Analyze this CSV and create Excel report"
1. data_analyzer: Process CSV, generate statistics
2. excel_generator: Create formatted spreadsheet with analysis
```

**Combine with File Organizer**:
```
User: "Create Excel inventory from files in this folder"
1. file_organizer: Scan folder, extract file metadata
2. excel_generator: Create inventory spreadsheet
```

## Templates

Pre-built templates available in `resources/templates/`:

- `basic_table.xlsx`: Simple data table
- `financial_report.xlsx`: Income statement format
- `project_tracker.xlsx`: Project management template
- `grade_book.xlsx`: Educational grade tracking

## Error Handling

**Missing data**: Create template with placeholder text
**Invalid formulas**: Fall back to static values with note
**File already exists**: Prompt for overwrite or new name
**Dependency issues**: Install openpyxl if missing

## Safety

- ✅ Non-destructive (creates new files)
- ✅ Validates file paths before writing
- ✅ Handles encoding issues gracefully
- ✅ Reports file location on completion

## Notes

- Excel files are saved in XLSX format (Excel 2007+)
- Formulas are preserved and recalculate when opened
- Charts are embedded in the workbook
- Compatible with Excel, LibreOffice, Google Sheets
- Large datasets (>100k rows) may take longer to process
