---
name: File Organizer
description: Organize and manage files with intelligent categorization, batch operations, and safety controls
version: 1.1.0
triggers:
  - organize folder
  - organize files
  - sort files
  - categorize files
  - batch rename
  - clean up folder
  - find duplicates
  - organize downloads
examples:
  - "Organize my Downloads folder by type"
  - "Find duplicate files in Documents"
  - "Batch rename photos with date prefix"
  - "Clean up old files in this folder"
context_hints:
  - user mentions organizing or sorting files
  - user wants to clean up folders
  - user mentions duplicates or renaming
  - user references Downloads or messy folders
priority: 6
conflicts_with: []
dependencies:
  - pathlib (built-in)
capabilities:
  - file_organization
  - batch_operations
  - duplicate_detection
  - smart_categorization
  - file_renaming
auto_load: true
---

# File Organizer Skill

## Purpose

Intelligently organize and manage files with automated categorization, batch operations, duplicate detection, and safety controls. This skill is the foundation for Cowork autonomous file management.

## Capabilities

### Core Features
- **Smart Categorization**: Organize files by type, date, size, or custom rules
- **Batch Rename**: Rename multiple files with patterns and sequences
- **Duplicate Detection**: Find and handle duplicate files
- **Folder Organization**: Create organized folder structures automatically
- **Archive Old Files**: Move or compress files based on age
- **Safety Controls**: Dry-run mode, backups, undo capabilities
- **File Metadata**: Extract and use file properties for organization

## Instructions

When the user requests file organization tasks, follow these steps:

### 1. Request Folder Access

**Always request permission first** using the folder permission system:

```python
# Example folder access request
from folder_permissions import FolderPermissionManager

pm = FolderPermissionManager()
pm.request_access(
    path="C:/Users/Username/Downloads",
    reason="Organize files by type and date"
)
```

**User Communication**:
```
"I need access to your Downloads folder to organize the files. 
This will allow me to:
- Scan file types and metadata
- Create category folders
- Move files to organized locations
- Generate an organization report

Permission will be recorded in .agent/config/folder_permissions.json
Proceed with read/write access?"
```

### 2. Analyze Folder Contents

Scan and categorize files:

```powershell
python .agent/skills/file_organizer/scripts/file_scanner.py `
  --path "C:/Users/Username/Downloads" `
  --analyze
```

**Output**: File inventory with types, sizes, dates, duplicates

### 3. Create Organization Plan

Based on analysis, create a plan:

**By File Type**:
```
Documents/ → .pdf, .docx, .txt, .xlsx
Images/ → .jpg, .png, .gif, .svg
Videos/ → .mp4, .avi, .mkv
Archives/ → .zip, .rar, .7z
Code/ → .py, .js, .html, .css
Other/ → everything else
```

**By Date**:
```
2026-01/ → files from January 2026
2025-12/ → files from December 2025
Older/ → files older than 6 months
```

**Custom Rules**:
- Move files >50MB to "Large Files"
- Archive files >1 year old
- Group files by project (based on naming patterns)

### 4. Execute with Dry-Run First

**Always preview changes before applying**:

```powershell
python .agent/skills/file_organizer/scripts/organizer.py `
  --path "C:/Users/Username/Downloads" `
  --mode by-type `
  --dry-run
```

**Show preview to user**:
```
📋 Organization Preview:

Would move 45 files:
  Documents/ (12 files)
    - report.pdf
    - budget.xlsx
    - notes.txt
    ...
  Images/ (18 files)
    - photo1.jpg
    - screenshot.png
    ...
  Videos/ (8 files)
    - recording.mp4
    ...
  Archives/ (7 files)
    - backup.zip
    ...

Proceed with organization? (yes/no)
```

### 5. Execute Real Organization

**After user confirmation**:

```powershell
python .agent/skills/file_organizer/scripts/organizer.py `
  --path "C:/Users/Username/Downloads" `
  --mode by-type `
  --execute
```

**Create backup before major changes**:
- Save file list with original locations
- Create undo script
- Log all operations

### 6. Report Results

Provide summary:
```
✅ Organization Complete!

Organized 45 files into 4 categories:
  📄 Documents: 12 files
  🖼️ Images: 18 files
  🎥 Videos: 8 files
  📦 Archives: 7 files

Created folders:
  - C:/Users/Username/Downloads/Documents
  - C:/Users/Username/Downloads/Images
  - C:/Users/Username/Downloads/Videos
  - C:/Users/Username/Downloads/Archives

Backup created: .agent/backups/downloads_org_2026-01-15.json
Undo available: python undo_downloads_org.py
```

## Organization Modes

### 1. By File Type

**Trigger**: "organize by type", "sort by file type"

**Categories**:
- Documents: pdf, doc, docx, txt, rtf, odt
- Spreadsheets: xls, xlsx, csv
- Presentations: ppt, pptx
- Images: jpg, jpeg, png, gif, svg, bmp, webp
- Videos: mp4, avi, mkv, mov, wmv, flv
- Audio: mp3, wav, flac, aac, ogg
- Archives: zip, rar, 7z, tar, gz
- Code: py, js, html, css, java, cpp, etc.
- Executables: exe, msi, dmg, app

### 2. By Date

**Trigger**: "organize by date", "sort by time"

**Grouping**:
- YYYY-MM/ (monthly folders)
- YYYY/MM/ (yearly with monthly subfolders)
- Recent/ vs. Old/ (threshold: 6 months)

### 3. By Size

**Trigger**: "organize by size", "find large files"

**Categories**:
- Small: < 1 MB
- Medium: 1-10 MB
- Large: 10-100 MB
- Huge: > 100 MB

### 4. Find Duplicates

**Trigger**: "find duplicates", "remove duplicate files"

**Detection**:
- Compare file hashes (MD5/SHA256)
- Group identical files
- Option to keep newest/oldest/largest
- Move duplicates to review folder

**Safety**: Never auto-delete duplicates, always review first

### 5. Batch Rename

**Trigger**: "rename files", "batch rename"

**Patterns**:
- Sequential: file_001.jpg, file_002.jpg
- Date prefix: 2026-01-15_photo.jpg
- Replace text: old_name → new_name
- Lowercase/uppercase conversion
- Remove special characters

## Usage Examples

### Example 1: Organize Downloads

**Request**: "Organize my Downloads folder"

**Action**:
1. Request access to Downloads
2. Scan files
3. Categorize by type (Documents, Images, etc.)
4. Show dry-run preview
5. Get confirmation
6. Execute organization
7. Create backup and undo script
8. Report results

### Example 2: Find Duplicates

**Request**: "Find duplicate files in my Documents"

**Action**:
1. Request access
2. Calculate file hashes
3. Group duplicates
4. Show duplicate groups with sizes
5. Suggest which to keep/remove
6. Move duplicates to "Duplicates_Review" folder
7. Report space saved

### Example 3: Batch Rename Photos

**Request**: "Rename all photos in this folder with date prefix"

**Action**:
1. Request access
2. Scan for image files
3. Extract date from EXIF or file modified date
4. Generate new names: 2026-01-15_001.jpg
5. Show preview
6. Get confirmation
7. Execute rename
8. Report renamed files

### Example 4: Archive Old Files

**Request**: "Archive files older than 1 year"

**Action**:
1. Request access
2. Find files with modified date > 1 year ago
3. Create "Archive_2025" folder
4. Show list of files to archive
5. Get confirmation
6. Move or compress to archive
7. Report archived files and space freed

## Integration with Cowork

This skill is designed to work with the Cowork file agent:

**Autonomous Workflow**:
```
User: "Organize my Downloads"
→ Cowork agent activates
→ Loads File Organizer skill
→ Requests folder access
→ Scans and analyzes
→ Creates plan
→ Shows preview
→ Executes with user approval
→ Reports completion
```

## Safety Features

### Dry-Run Mode
- **Always enabled by default**
- Preview all changes before execution
- No files modified until user confirms

### Backups
- Create JSON manifest of original file locations
- Generate undo script
- Store in .agent/backups/

### Undo Capability
```powershell
python .agent/skills/file_organizer/scripts/undo.py --backup backups/org_2026-01-15.json
```

### Permissions
- Check folder permissions before any operation
- Log all file operations
- Respect global restrictions (system folders, etc.)

### Validation
- Verify destination paths exist
- Check disk space before moving
- Handle file conflicts (rename, skip, overwrite)

## Error Handling

**Permission Denied**: Request access or notify user
**File in Use**: Skip and report
**Disk Space**: Warn and abort
**File Conflicts**: Offer rename options
**Invalid Paths**: Validate and correct

## Notes

- Operations are logged to audit trail
- Works with folder_permissions.py for access control
- Compatible with Windows, macOS, Linux paths
- Handles special characters in filenames
- Preserves file metadata (timestamps, etc.)
- Can process large folders (1000s of files)
