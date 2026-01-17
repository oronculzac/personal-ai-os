"""
Linear Client - Consolidated Linear API Access

This is the SINGLE SOURCE OF TRUTH for Linear API operations.
All skills should import from here.

Usage:
    from .agent.core.linear_client import LinearClient
    # or
    import sys; sys.path.insert(0, '.agent/core')
    from linear_client import LinearClient
"""

# Re-export everything from the implementation
from .linear_client import (
    LinearClient,
    LinearIssue,
    format_issues_for_display
)

__all__ = ['LinearClient', 'LinearIssue', 'format_issues_for_display']
