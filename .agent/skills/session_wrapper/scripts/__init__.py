"""
Session Wrapper Scripts Package

Provides automated "Learning-in-Public" workflow:
- collect_context: Aggregate Git, Linear, and Obsidian data
- publish_detector: Determine if session is GitHub-worthy
- linear_client: Direct Linear API access
- session_wrapper: Main orchestration script
"""

from .collect_context import get_config, get_git_info, get_linear_tickets, get_obsidian_focus
from .publish_detector import analyze_session, PublishDecision, ContentType, TargetRepo
from .linear_client import LinearClient, LinearIssue

__all__ = [
    'get_config',
    'get_git_info', 
    'get_linear_tickets',
    'get_obsidian_focus',
    'analyze_session',
    'PublishDecision',
    'ContentType',
    'TargetRepo',
    'LinearClient',
    'LinearIssue'
]
