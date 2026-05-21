"""Test fixtures and mock data for automation tests."""

import sqlite3
import tempfile
import os
from typing import List, Dict, Any
from datetime import datetime, timedelta


class TestDatabase:
    """Create temporary test database with sample data."""

    def __init__(self):
        self.db_path = tempfile.mktemp(suffix='.db')
        self.conn = None

    def setup(self):
        """Create test database schema and insert sample data."""
        self.conn = sqlite3.connect(self.db_path)
        self._create_schema()
        self._insert_sample_data()
        return self.conn

    def _create_schema(self):
        """Create test database schema."""
        cursor = self.conn.cursor()

        # Core tables
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                skill_id TEXT,
                action_type TEXT,
                started_at TIMESTAMP,
                completed_at TIMESTAMP,
                duration_seconds REAL,
                success BOOLEAN,
                metadata TEXT
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS skills (
                id TEXT PRIMARY KEY,
                name TEXT,
                description TEXT,
                usage_count INTEGER DEFAULT 0,
                last_used_at TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS automation_patterns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pattern_type TEXT,
                pattern_data TEXT,
                confidence REAL,
                detected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                action_taken TEXT
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS automation_proposals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                proposal_type TEXT,
                title TEXT,
                description TEXT,
                impact_score REAL,
                confidence_score REAL,
                risk_level TEXT,
                status TEXT DEFAULT 'pending',
                proposed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                decided_at TIMESTAMP,
                decision_by TEXT
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS automation_schedule (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task_name TEXT,
                task_type TEXT,
                schedule_expression TEXT,
                parameters TEXT,
                enabled BOOLEAN DEFAULT 1,
                next_run_at TIMESTAMP,
                last_run_at TIMESTAMP,
                run_count INTEGER DEFAULT 0
            )
        """)

        # Analytics views
        cursor.execute("""
            CREATE VIEW IF NOT EXISTS v_task_sequences AS
            SELECT
                skill_id,
                started_at,
                completed_at,
                duration_seconds,
                LAG(skill_id) OVER (ORDER BY started_at) as prev_skill_id
            FROM tasks
            WHERE success = 1
        """)

        self.conn.commit()

    def _insert_sample_data(self):
        """Insert sample data for testing."""
        cursor = self.conn.cursor()
        now = datetime.now()

        # Sample skills
        skills = [
            ('mmc-carrossel', 'Carrossel Creator', 'Create Instagram carousels', 45, now - timedelta(days=1)),
            ('mmc-email-profissional', 'Email Writer', 'Write professional emails', 30, now - timedelta(days=2)),
            ('mmc-anuncio-google', 'Google Ads Creator', 'Create Google ads', 15, now - timedelta(days=5)),
            ('mmc-relatorio-ads', 'Ads Reporter', 'Generate ads reports', 8, now - timedelta(days=10)),
            ('mmc-seo', 'SEO Optimizer', 'Optimize content for SEO', 25, now - timedelta(hours=6)),
        ]

        for skill in skills:
            cursor.execute(
                "INSERT OR REPLACE INTO skills (id, name, description, usage_count, last_used_at) VALUES (?, ?, ?, ?, ?)",
                skill
            )

        # Sample tasks with patterns
        tasks = []

        # Pattern 1: Weekly analytics report (every Monday morning)
        for week in range(4):
            base_time = now - timedelta(weeks=week, days=now.weekday())
            tasks.append((
                'mmc-relatorio-ads', 'analytics', 'report',
                base_time.replace(hour=9, minute=0),
                base_time.replace(hour=9, minute=15),
                900.0, True
            ))

        # Pattern 2: Morning content creation sequence
        for day in range(5):
            base_time = now - timedelta(days=day)
            tasks.append((
                'mmc-carrossel', 'create', 'content',
                base_time.replace(hour=10, minute=0),
                base_time.replace(hour=10, minute=30),
                1800.0, True
            ))
            tasks.append((
                'mmc-seo', 'optimize', 'content',
                base_time.replace(hour=10, minute=35),
                base_time.replace(hour=10, minute=50),
                900.0, True
            ))

        # Pattern 3: Inefficient task (>120s, repeated 3+ times)
        for i in range(5):
            base_time = now - timedelta(hours=i*6)
            tasks.append((
                'mmc-email-profissional', 'create', 'email',
                base_time,
                base_time + timedelta(seconds=150),
                150.0, True
            ))

        # Pattern 4: Underutilized skill with high potential
        cursor.execute(
            "UPDATE skills SET usage_count = 3 WHERE id = 'mmc-anuncio-google'"
        )

        for task in tasks:
            cursor.execute(
                """INSERT INTO tasks (skill_id, action_type, started_at, completed_at, duration_seconds, success)
                   VALUES (?, ?, ?, ?, ?, ?)""",
                task
            )

        self.conn.commit()

    def teardown(self):
        """Clean up test database."""
        if self.conn:
            self.conn.close()
        if os.path.exists(self.db_path):
            os.remove(self.db_path)


# Sample test data
SAMPLE_PATTERNS = {
    'task_sequence': {
        'type': 'task_sequence',
        'skills': ['mmc-carrossel', 'mmc-seo'],
        'frequency': 5,
        'avg_duration': 2700.0,
        'last_seen': datetime.now().isoformat()
    },
    'temporal_pattern': {
        'type': 'temporal_pattern',
        'skill_id': 'mmc-relatorio-ads',
        'schedule': '0 9 * * 1',
        'frequency': 4,
        'consistency': 0.95
    },
    'inefficiency': {
        'type': 'inefficiency',
        'skill_id': 'mmc-email-profissional',
        'avg_duration': 150.0,
        'threshold': 120.0,
        'occurrences': 5
    },
    'underutilized_skill': {
        'type': 'underutilized_skill',
        'skill_id': 'mmc-anuncio-google',
        'usage_count': 3,
        'potential_score': 0.8
    }
}

SAMPLE_PROPOSALS = [
    {
        'id': 1,
        'type': 'CREATE_SKILL',
        'title': 'Automate Weekly Content Sequence',
        'description': 'Create skill that combines carrossel + SEO optimization',
        'impact_score': 0.8,
        'confidence_score': 0.9,
        'risk_level': 'LOW',
        'status': 'pending'
    },
    {
        'id': 2,
        'type': 'SCHEDULE_TASK',
        'title': 'Weekly Analytics Report',
        'description': 'Automate weekly ads report generation',
        'impact_score': 0.7,
        'confidence_score': 0.95,
        'risk_level': 'LOW',
        'status': 'pending'
    },
    {
        'id': 3,
        'type': 'OPTIMIZE_WORKFLOW',
        'title': 'Optimize Email Creation',
        'description': 'Email creation takes 150s, could be optimized',
        'impact_score': 0.6,
        'confidence_score': 0.7,
        'risk_level': 'MEDIUM',
        'status': 'pending'
    }
]

SAMPLE_ML_FEATURES = {
    'duration_normalized': 0.5,
    'frequency_normalized': 0.8,
    'success_rate': 0.95,
    'time_since_last_use': 0.3,
    'skill_usage_count': 45,
    'avg_completion_time': 1200.0,
    'peak_usage_hour': 10
}
