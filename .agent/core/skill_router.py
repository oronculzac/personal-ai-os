#!/usr/bin/env python3
"""
Skill Router - Deterministic skill matching helper

Provides weighted scoring to help select the most appropriate skill
based on user input, context, and priority.

Usage:
    from skill_router import SkillRouter
    router = SkillRouter()
    matches = router.match("sync my tasks to Linear")
    # Returns: [('obsidian_linear_sync', 0.85), ('linear_manager', 0.60), ...]
"""

import json
import re
import sys
from pathlib import Path
from typing import List, Tuple, Dict, Optional
from dataclasses import dataclass


@dataclass
class SkillMatch:
    """Represents a skill match result"""
    name: str
    path: str
    score: float
    match_reasons: List[str]


class SkillRouter:
    """Routes user requests to the most appropriate skill(s)"""
    
    def __init__(self, registry_path: Optional[Path] = None):
        """Initialize router with skill registry"""
        if registry_path is None:
            # Find skill registry
            workspace_root = Path(__file__).parent.parent
            registry_path = workspace_root / "config" / "skill_registry.json"
        
        self.registry_path = registry_path
        self.skills = self._load_registry()
    
    def _load_registry(self) -> Dict:
        """Load skill registry (converts list to dict by id)"""
        try:
            with open(self.registry_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                skills_list = data.get('skills', [])
                # Convert list to dict keyed by id
                return {skill.get('id', skill.get('name', '')): skill 
                        for skill in skills_list}
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Warning: Could not load skill registry: {e}")
            return {}
    
    def _normalize(self, text: str) -> str:
        """Normalize text for matching"""
        return text.lower().strip()
    
    def _score_trigger_match(self, query: str, triggers: List[str]) -> Tuple[float, List[str]]:
        """Score based on trigger matches (0-1)"""
        query_norm = self._normalize(query)
        score = 0.0
        reasons = []
        
        for trigger in triggers:
            trigger_norm = self._normalize(trigger)
            
            # Exact match
            if trigger_norm in query_norm:
                score = max(score, 0.9)
                reasons.append(f"trigger match: '{trigger}'")
            # Partial word match
            elif any(word in query_norm for word in trigger_norm.split()):
                score = max(score, 0.5)
                reasons.append(f"partial trigger: '{trigger}'")
        
        return score, reasons
    
    def _score_example_match(self, query: str, examples: List[str]) -> Tuple[float, List[str]]:
        """Score based on example similarity (0-1)"""
        query_words = set(self._normalize(query).split())
        max_score = 0.0
        reasons = []
        
        for example in examples:
            example_words = set(self._normalize(example).split())
            
            # Calculate word overlap
            common = query_words & example_words
            if common:
                overlap = len(common) / max(len(query_words), len(example_words))
                if overlap > max_score:
                    max_score = overlap
                    reasons = [f"example similarity: '{example[:40]}...'"]
        
        return min(max_score, 0.8), reasons  # Cap at 0.8
    
    def _score_context_match(self, query: str, context_hints: List[str]) -> Tuple[float, List[str]]:
        """Score based on context hint matches (0-1)"""
        query_norm = self._normalize(query)
        score = 0.0
        reasons = []
        
        for hint in context_hints:
            hint_norm = self._normalize(hint)
            # Check if hint keywords are in query
            hint_words = hint_norm.split()
            matches = sum(1 for word in hint_words if word in query_norm and len(word) > 3)
            if matches >= 2:
                score = max(score, 0.6)
                reasons.append(f"context: '{hint[:30]}...'")
        
        return score, reasons
    
    def match(self, query: str, top_n: int = 5) -> List[SkillMatch]:
        """
        Match query to skills, returning ranked matches.
        
        Args:
            query: User's natural language request
            top_n: Number of top matches to return
        
        Returns:
            List of SkillMatch objects, sorted by score descending
        """
        matches = []
        
        for skill_name, skill_data in self.skills.items():
            total_score = 0.0
            all_reasons = []
            
            # Get metadata
            triggers = skill_data.get('triggers', [])
            examples = skill_data.get('examples', [])
            context_hints = skill_data.get('context_hints', [])
            priority = skill_data.get('priority', 5) / 10.0  # Normalize to 0-1
            
            # Score triggers (weight: 0.4)
            trigger_score, trigger_reasons = self._score_trigger_match(query, triggers)
            total_score += trigger_score * 0.4
            all_reasons.extend(trigger_reasons)
            
            # Score examples (weight: 0.3)
            example_score, example_reasons = self._score_example_match(query, examples)
            total_score += example_score * 0.3
            all_reasons.extend(example_reasons)
            
            # Score context hints (weight: 0.2)
            context_score, context_reasons = self._score_context_match(query, context_hints)
            total_score += context_score * 0.2
            all_reasons.extend(context_reasons)
            
            # Apply priority boost (weight: 0.1)
            total_score += priority * 0.1
            
            if total_score > 0:
                matches.append(SkillMatch(
                    name=skill_name,
                    path=skill_data.get('path', ''),
                    score=round(total_score, 3),
                    match_reasons=all_reasons
                ))
        
        # Sort by score descending
        matches.sort(key=lambda x: x.score, reverse=True)
        return matches[:top_n]
    
    def best_match(self, query: str) -> Optional[SkillMatch]:
        """Get the single best matching skill"""
        matches = self.match(query, top_n=1)
        return matches[0] if matches else None
    
    def suggest_skills(self, query: str, threshold: float = 0.3) -> List[str]:
        """Get list of skill names that match above threshold"""
        matches = self.match(query, top_n=10)
        return [m.name for m in matches if m.score >= threshold]


def main():
    """CLI for testing skill routing"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Route queries to skills')
    parser.add_argument('query', nargs='?', help='Query to match')
    parser.add_argument('--top', type=int, default=5, help='Number of matches')
    parser.add_argument('--threshold', type=float, default=0.2, help='Min score')
    args = parser.parse_args()
    
    router = SkillRouter()
    
    if args.query:
        queries = [args.query]
    else:
        # Demo queries
        queries = [
            "wrap up this session",
            "sync my tasks to Linear",
            "create a new project",
            "scrape this website",
            "generate a Spark ETL script",
        ]
    
    for query in queries:
        print(f"\n📝 Query: \"{query}\"")
        print("-" * 50)
        matches = router.match(query, top_n=args.top)
        
        for i, m in enumerate(matches, 1):
            if m.score >= args.threshold:
                print(f"  {i}. {m.name} (score: {m.score:.2f})")
                for reason in m.match_reasons[:2]:
                    print(f"     → {reason}")


if __name__ == "__main__":
    main()
