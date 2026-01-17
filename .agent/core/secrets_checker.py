"""
Secrets Safety Checker - Prevent accidental exposure of sensitive data

This module scans content before publishing to ensure no secrets,
API keys, passwords, or sensitive information is exposed.
"""

import re
import json
from pathlib import Path
from typing import List, Tuple, Dict
from dataclasses import dataclass


@dataclass
class SecretMatch:
    """Represents a detected secret."""
    pattern_name: str
    match: str
    line_number: int
    redacted: str


# Patterns that indicate potential secrets
SECRET_PATTERNS = {
    # API Keys
    "github_token": r'ghp_[A-Za-z0-9]{36}',
    "github_oauth": r'gho_[A-Za-z0-9]{36}',
    "github_pat": r'github_pat_[A-Za-z0-9_]{22,}',
    "linear_api_key": r'lin_api_[A-Za-z0-9]{32,}',
    "openai_key": r'sk-[A-Za-z0-9]{32,}',
    "anthropic_key": r'sk-ant-[A-Za-z0-9-]{32,}',
    "aws_access_key": r'AKIA[A-Z0-9]{16}',
    "aws_secret_key": r'[A-Za-z0-9/+=]{40}',
    "devto_api_key": r'[A-Za-z0-9]{20,30}',  # Generic pattern for dev.to
    
    # Generic patterns
    "api_key_generic": r'(?i)(api[_-]?key|apikey)\s*[:=]\s*["\']?([A-Za-z0-9_-]{20,})["\']?',
    "password": r'(?i)(password|passwd|pwd)\s*[:=]\s*["\']?([^\s"\']{8,})["\']?',
    "secret": r'(?i)(secret|token)\s*[:=]\s*["\']?([A-Za-z0-9_-]{16,})["\']?',
    "private_key": r'-----BEGIN (?:RSA |EC |DSA )?PRIVATE KEY-----',
    "bearer_token": r'Bearer\s+[A-Za-z0-9._-]+',
    
    # Email/personal info
    "email": r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
    
    # Connection strings
    "connection_string": r'(?i)(mongodb|mysql|postgresql|redis)://[^\s]+',
    "db_password": r'(?i)password=[^\s&;]+',
}

# Files that should never be published
BLOCKED_FILES = [
    '.env',
    '.env.local',
    '.env.production',
    'secrets.json',
    'credentials.json',
    '*.pem',
    '*.key',
    '*_secret*',
    'mcp_config.json',  # Contains API keys!
]

# Patterns that are safe to ignore (false positives)
SAFE_PATTERNS = [
    r'example\.com',
    r'placeholder',
    r'YOUR_.*_HERE',
    r'xxxx+',
    r'\*\*\*+',
]


def is_safe_match(match: str) -> bool:
    """Check if a match is actually a safe placeholder."""
    for pattern in SAFE_PATTERNS:
        if re.search(pattern, match, re.IGNORECASE):
            return True
    return False


def scan_content(content: str) -> List[SecretMatch]:
    """
    Scan content for potential secrets.
    
    Returns list of detected secrets with line numbers.
    """
    matches = []
    lines = content.split('\n')
    
    for line_num, line in enumerate(lines, 1):
        for pattern_name, pattern in SECRET_PATTERNS.items():
            for match in re.finditer(pattern, line):
                matched_text = match.group(0)
                
                # Skip safe patterns
                if is_safe_match(matched_text):
                    continue
                
                # Redact the match for safe display
                if len(matched_text) > 10:
                    redacted = matched_text[:4] + '***' + matched_text[-4:]
                else:
                    redacted = '***REDACTED***'
                
                matches.append(SecretMatch(
                    pattern_name=pattern_name,
                    match=matched_text,
                    line_number=line_num,
                    redacted=redacted
                ))
    
    return matches


def scan_file(file_path: Path) -> Tuple[bool, List[SecretMatch]]:
    """
    Scan a file for secrets.
    
    Returns: (is_safe, list of matches)
    """
    # Check against blocked file patterns
    file_name = file_path.name.lower()
    for blocked in BLOCKED_FILES:
        if blocked.startswith('*'):
            if file_name.endswith(blocked[1:]):
                return False, [SecretMatch(
                    pattern_name="blocked_file",
                    match=str(file_path),
                    line_number=0,
                    redacted=f"File type blocked: {blocked}"
                )]
        elif blocked in file_name:
            return False, [SecretMatch(
                pattern_name="blocked_file",
                match=str(file_path),
                line_number=0,
                redacted=f"File blocked: {blocked}"
            )]
    
    # Read and scan content
    try:
        content = file_path.read_text(encoding='utf-8')
        matches = scan_content(content)
        return len(matches) == 0, matches
    except Exception as e:
        return True, []  # If can't read, assume safe (might be binary)


def redact_secrets(content: str) -> str:
    """
    Replace detected secrets with redacted versions.
    """
    result = content
    matches = scan_content(content)
    
    for match in matches:
        result = result.replace(match.match, match.redacted)
    
    return result


def check_publish_safety(files: List[Path]) -> Tuple[bool, str]:
    """
    Check if files are safe to publish.
    
    Returns: (is_safe, report)
    """
    all_matches = []
    blocked_files = []
    
    for file_path in files:
        is_safe, matches = scan_file(file_path)
        if not is_safe:
            if matches and matches[0].pattern_name == "blocked_file":
                blocked_files.append(str(file_path))
            else:
                all_matches.extend([(file_path, m) for m in matches])
    
    if not blocked_files and not all_matches:
        return True, "✅ All files appear safe to publish."
    
    # Build report
    lines = ["⚠️ PUBLISHING SAFETY CHECK FAILED", "=" * 40, ""]
    
    if blocked_files:
        lines.append("🚫 BLOCKED FILES (should never be published):")
        for f in blocked_files:
            lines.append(f"   • {f}")
        lines.append("")
    
    if all_matches:
        lines.append("🔒 POTENTIAL SECRETS DETECTED:")
        for file_path, match in all_matches:
            lines.append(f"   • {file_path}:{match.line_number}")
            lines.append(f"     Type: {match.pattern_name}")
            lines.append(f"     Found: {match.redacted}")
        lines.append("")
    
    lines.append("Action: Remove or redact these items before publishing.")
    
    return False, "\n".join(lines)


# CLI
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "--test":
            # Test with sample content
            test_content = """
# Config file
api_key = "ghp_XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX1234"
password = "mysecretpassword123"
email = test@example.com

# Safe placeholder
API_KEY = "YOUR_API_KEY_HERE"
"""
            matches = scan_content(test_content)
            print("Detected secrets:")
            for m in matches:
                print(f"  - {m.pattern_name}: {m.redacted} (line {m.line_number})")
        else:
            # Check specific files
            files = [Path(f) for f in sys.argv[1:]]
            is_safe, report = check_publish_safety(files)
            print(report)
    else:
        print("Usage:")
        print("  python secrets_checker.py --test")
        print("  python secrets_checker.py <file1> <file2> ...")
