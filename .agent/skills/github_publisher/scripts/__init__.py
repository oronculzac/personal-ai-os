"""
GitHub Publisher Scripts Package

Provides automated publishing to GitHub repositories:
- publisher: Core publishing logic with repo routing
"""

from .publisher import (
    publish_to_github,
    generate_commit_message,
    load_config,
    PublishConfig,
    PublishResult,
    TargetRepo
)

__all__ = [
    'publish_to_github',
    'generate_commit_message',
    'load_config',
    'PublishConfig',
    'PublishResult',
    'TargetRepo'
]
