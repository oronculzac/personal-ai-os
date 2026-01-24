#!/usr/bin/env python3
"""
Brand Extractor - Extract branding from a URL using Firecrawl MCP

This script provides a helper for extracting brand identity from websites.
Note: This is meant to be called by Claude using the Firecrawl MCP tool,
not run directly. The script documents the expected data structures.

Usage via Claude:
    firecrawl_scrape(url="https://example.com", formats=["branding"])
"""

import json
from dataclasses import dataclass
from typing import Optional


@dataclass
class Colors:
    """Brand color palette"""
    primary: Optional[str] = None
    secondary: Optional[str] = None
    accent: Optional[str] = None
    background: Optional[str] = None
    text_primary: Optional[str] = None
    text_secondary: Optional[str] = None


@dataclass
class Typography:
    """Brand typography system"""
    font_families: dict = None  # primary, heading, code
    font_sizes: dict = None     # h1, h2, body, small
    font_weights: dict = None   # regular, medium, bold


@dataclass
class Spacing:
    """Brand spacing guidelines"""
    base_unit: Optional[int] = None    # e.g., 8
    border_radius: Optional[str] = None # e.g., "8px"


@dataclass
class BrandingProfile:
    """Complete brand identity profile"""
    url: str
    color_scheme: str  # "light" or "dark"
    colors: Colors
    typography: Typography
    spacing: Spacing
    logo_url: Optional[str] = None
    favicon_url: Optional[str] = None


def format_brand_markdown(branding: dict, url: str) -> str:
    """Format branding data as Markdown report"""
    
    lines = [
        f"# Brand Analysis: {url}",
        "",
        "## Color Scheme",
        f"- Mode: {branding.get('colorScheme', 'unknown')}",
        "",
        "## Colors"
    ]
    
    colors = branding.get('colors', {})
    for key, value in colors.items():
        if value:
            lines.append(f"- {key}: `{value}`")
    
    lines.extend([
        "",
        "## Typography"
    ])
    
    typography = branding.get('typography', {})
    font_families = typography.get('fontFamilies', {})
    for key, value in font_families.items():
        if value:
            lines.append(f"- {key}: {value}")
    
    lines.extend([
        "",
        "## Spacing"
    ])
    
    spacing = branding.get('spacing', {})
    if spacing.get('baseUnit'):
        lines.append(f"- Base Unit: {spacing['baseUnit']}px")
    if spacing.get('borderRadius'):
        lines.append(f"- Border Radius: {spacing['borderRadius']}")
    
    images = branding.get('images', {})
    if images:
        lines.extend([
            "",
            "## Images"
        ])
        if images.get('logo'):
            lines.append(f"- Logo: {images['logo']}")
        if images.get('favicon'):
            lines.append(f"- Favicon: {images['favicon']}")
    
    return "\n".join(lines)


def format_brand_json(branding: dict, url: str) -> str:
    """Format branding data as JSON"""
    from datetime import datetime
    
    output = {
        "url": url,
        "extracted_at": datetime.now().isoformat(),
        "branding": branding
    }
    
    return json.dumps(output, indent=2)


if __name__ == "__main__":
    print("Brand Extractor Helper")
    print("=" * 40)
    print()
    print("This script documents the branding data structures.")
    print("To extract branding, use the Firecrawl MCP tool:")
    print()
    print('  firecrawl_scrape:')
    print('    url: "https://example.com"')
    print('    formats: ["branding"]')
