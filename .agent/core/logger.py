"""
Structured Logging System for Personal AI OS

Provides consistent JSON logging across all skills and core modules.
Logs are written to .agent/logs/ with rotation.

Usage:
    from core.logger import get_logger, log_skill_run
    
    logger = get_logger(__name__)
    logger.info("Processing started", extra={"skill": "session_wrapper"})
    
    # Or for skill execution tracking
    log_skill_run("session_wrapper", success=True, duration_ms=1234)
"""

import os
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any
from functools import wraps
import time


class JSONFormatter(logging.Formatter):
    """Format log records as JSON for structured logging."""
    
    def format(self, record: logging.LogRecord) -> str:
        log_data = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        
        # Add extra fields
        if hasattr(record, 'skill'):
            log_data['skill'] = record.skill
        if hasattr(record, 'duration_ms'):
            log_data['duration_ms'] = record.duration_ms
        if hasattr(record, 'success'):
            log_data['success'] = record.success
        if hasattr(record, 'error'):
            log_data['error'] = record.error
        
        # Add any other extra fields
        for key, value in record.__dict__.items():
            if key not in ['name', 'msg', 'args', 'created', 'filename', 
                          'funcName', 'levelname', 'levelno', 'lineno',
                          'module', 'msecs', 'pathname', 'process',
                          'processName', 'relativeCreated', 'stack_info',
                          'thread', 'threadName', 'exc_info', 'exc_text',
                          'message', 'skill', 'duration_ms', 'success', 'error']:
                if not key.startswith('_'):
                    log_data[key] = value
        
        # Add exception info if present
        if record.exc_info:
            log_data['exception'] = self.formatException(record.exc_info)
        
        return json.dumps(log_data)


def get_logs_dir() -> Path:
    """Get the logs directory path."""
    # Find workspace root by looking for .agent folder
    current = Path.cwd()
    while current != current.parent:
        if (current / ".agent").exists():
            logs_dir = current / ".agent" / "logs"
            logs_dir.mkdir(parents=True, exist_ok=True)
            return logs_dir
        current = current.parent
    
    # Fallback to current directory
    logs_dir = Path.cwd() / ".agent" / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)
    return logs_dir


def get_logger(name: str, level: int = logging.INFO) -> logging.Logger:
    """
    Get a configured logger instance.
    
    Args:
        name: Logger name (typically __name__)
        level: Logging level
    
    Returns:
        Configured logger with JSON file handler
    """
    logger = logging.getLogger(name)
    
    if not logger.handlers:  # Avoid duplicate handlers
        logger.setLevel(level)
        
        # File handler with JSON format
        logs_dir = get_logs_dir()
        log_file = logs_dir / "system.log"
        
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setFormatter(JSONFormatter())
        file_handler.setLevel(level)
        logger.addHandler(file_handler)
        
        # Console handler for errors only
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.ERROR)
        console_handler.setFormatter(logging.Formatter(
            '%(levelname)s: %(message)s'
        ))
        logger.addHandler(console_handler)
    
    return logger


def log_skill_run(
    skill_name: str,
    success: bool,
    duration_ms: Optional[int] = None,
    error: Optional[str] = None,
    metadata: Optional[Dict[str, Any]] = None
) -> None:
    """
    Log a skill execution to the runs.jsonl file.
    
    Args:
        skill_name: Name of the skill that was executed
        success: Whether the execution was successful
        duration_ms: Execution duration in milliseconds
        error: Error message if failed
        metadata: Additional metadata to log
    """
    logs_dir = get_logs_dir()
    runs_file = logs_dir / "runs.jsonl"
    
    run_data = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "skill": skill_name,
        "success": success,
    }
    
    if duration_ms is not None:
        run_data["duration_ms"] = duration_ms
    if error:
        run_data["error"] = error
    if metadata:
        run_data.update(metadata)
    
    with open(runs_file, 'a', encoding='utf-8') as f:
        f.write(json.dumps(run_data) + '\n')


def log_sync_run(
    direction: str,
    created: int = 0,
    updated: int = 0,
    skipped: int = 0,
    errors: int = 0,
    duration_ms: Optional[int] = None
) -> None:
    """
    Log an Obsidian↔Linear sync execution.
    
    Args:
        direction: 'obsidian_to_linear' or 'linear_to_obsidian'
        created: Number of items created
        updated: Number of items updated
        skipped: Number of items skipped
        errors: Number of errors
        duration_ms: Execution duration
    """
    logs_dir = get_logs_dir()
    sync_file = logs_dir / "sync.jsonl"
    
    sync_data = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "direction": direction,
        "created": created,
        "updated": updated,
        "skipped": skipped,
        "errors": errors,
        "success": errors == 0,
    }
    
    if duration_ms is not None:
        sync_data["duration_ms"] = duration_ms
    
    with open(sync_file, 'a', encoding='utf-8') as f:
        f.write(json.dumps(sync_data) + '\n')


def track_execution(skill_name: str):
    """
    Decorator to track skill execution time and success.
    
    Usage:
        @track_execution("my_skill")
        def my_function():
            ...
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            try:
                result = func(*args, **kwargs)
                duration_ms = int((time.time() - start_time) * 1000)
                log_skill_run(skill_name, success=True, duration_ms=duration_ms)
                return result
            except Exception as e:
                duration_ms = int((time.time() - start_time) * 1000)
                log_skill_run(skill_name, success=False, duration_ms=duration_ms, error=str(e))
                raise
        return wrapper
    return decorator


def get_run_stats(skill_name: Optional[str] = None, days: int = 7) -> Dict[str, Any]:
    """
    Get execution statistics for skills.
    
    Args:
        skill_name: Filter to specific skill, or None for all
        days: Number of days to look back
    
    Returns:
        Dict with total runs, success rate, avg duration
    """
    logs_dir = get_logs_dir()
    runs_file = logs_dir / "runs.jsonl"
    
    if not runs_file.exists():
        return {"total": 0, "success_rate": 0.0, "avg_duration_ms": 0}
    
    cutoff = datetime.utcnow().timestamp() - (days * 86400)
    runs = []
    
    with open(runs_file, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                run = json.loads(line.strip())
                run_time = datetime.fromisoformat(run['timestamp'].replace('Z', '+00:00')).timestamp()
                if run_time >= cutoff:
                    if skill_name is None or run.get('skill') == skill_name:
                        runs.append(run)
            except (json.JSONDecodeError, KeyError):
                continue
    
    if not runs:
        return {"total": 0, "success_rate": 0.0, "avg_duration_ms": 0}
    
    successes = sum(1 for r in runs if r.get('success', False))
    durations = [r.get('duration_ms', 0) for r in runs if 'duration_ms' in r]
    
    return {
        "total": len(runs),
        "success_rate": round(successes / len(runs) * 100, 1),
        "avg_duration_ms": int(sum(durations) / len(durations)) if durations else 0,
    }


if __name__ == "__main__":
    # Test logging
    logger = get_logger("test")
    logger.info("Test log message", extra={"skill": "test_skill"})
    
    # Test skill run logging
    log_skill_run("test_skill", success=True, duration_ms=123)
    
    # Test sync logging
    log_sync_run("obsidian_to_linear", created=5, skipped=2)
    
    print("✅ Logging system initialized")
    print(f"📁 Logs directory: {get_logs_dir()}")
    print(f"📊 Stats: {get_run_stats()}")
