"""
Session Wrapper Scripts Package

Provides automated "Learning-in-Public" workflow:
- collect_context: Aggregate Git, Linear, and Obsidian data
- publish_detector: Determine if session is GitHub-worthy
- linear_client: Direct Linear API access
- session_wrapper: Main orchestration script
- synthesizer: Generate narratives and social drafts
- weekly_summary: Aggregate weekly stats
"""

from .collect_context import get_config, get_git_info, get_linear_tickets, get_obsidian_focus
from .publish_detector import analyze_session, PublishDecision, ContentType, TargetRepo
from .linear_client import LinearClient, LinearIssue
from .synthesizer import synthesize_session, SynthesizedContent
from .weekly_summary import generate_weekly_summary, WeeklySummary

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
    'LinearIssue',
    'synthesize_session',
    'SynthesizedContent',
    'generate_weekly_summary',
    'WeeklySummary'
]
