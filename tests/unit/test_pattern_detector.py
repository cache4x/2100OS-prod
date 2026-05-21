"""Unit tests for pattern_detector.py"""

import unittest
import sys
import os
from datetime import datetime, timedelta

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from .fixtures.test_data import TestDatabase, SAMPLE_PATTERNS


class TestPatternDetector(unittest.TestCase):
    """Test cases for PatternDetector class."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_db = TestDatabase()
        self.conn = self.test_db.setup()

        # Import here to use test database
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../.gsd/automation'))
        from pattern_detector import PatternDetector
        self.detector = PatternDetector(self.conn)

    def tearDown(self):
        """Clean up test fixtures."""
        self.test_db.teardown()

    def test_detect_task_sequences(self):
        """Test detection of recurring task sequences."""
        patterns = self.detector.detect_task_sequences(min_frequency=3)

        # Should detect the carrossel + SEO sequence
        self.assertGreater(len(patterns), 0)

        # Check pattern structure
        pattern = patterns[0]
        self.assertIn('pattern_type', pattern)
        self.assertEqual(pattern['pattern_type'], 'task_sequence')
        self.assertIn('skills', pattern)
        self.assertIn('frequency', pattern)
        self.assertGreaterEqual(pattern['frequency'], 3)

    def test_detect_temporal_patterns(self):
        """Test detection of time-based patterns."""
        patterns = self.detector.detect_temporal_patterns(min_consistency=0.8)

        # Should detect Monday morning reports
        self.assertGreater(len(patterns), 0)

        # Check pattern structure
        pattern = patterns[0]
        self.assertEqual(pattern['pattern_type'], 'temporal_pattern')
        self.assertIn('skill_id', pattern)
        self.assertIn('schedule', pattern)
        self.assertIn('consistency', pattern)
        self.assertGreaterEqual(pattern['consistency'], 0.8)

    def test_detect_inefficiencies(self):
        """Test detection of inefficient tasks."""
        patterns = self.detector.detect_inefficiencies(duration_threshold=120, min_occurrences=3)

        # Should detect slow email creation
        self.assertGreater(len(patterns), 0)

        # Check pattern structure
        pattern = patterns[0]
        self.assertEqual(pattern['pattern_type'], 'inefficiency')
        self.assertIn('skill_id', pattern)
        self.assertIn('avg_duration', pattern)
        self.assertGreater(pattern['avg_duration'], 120)

    def test_detect_underutilized_skills(self):
        """Test detection of underutilized skills with potential."""
        patterns = self.detector.detect_underutilized_skills(
            max_usage_count=10,
            min_potential_score=0.5
        )

        # Should detect underutilized Google Ads skill
        self.assertGreater(len(patterns), 0)

        # Check pattern structure
        pattern = patterns[0]
        self.assertEqual(pattern['pattern_type'], 'underutilized_skill')
        self.assertIn('skill_id', pattern)
        self.assertIn('usage_count', pattern)
        self.assertLessEqual(pattern['usage_count'], 10)

    def test_detect_repetitive_tasks(self):
        """Test detection of repetitive single tasks."""
        patterns = self.detector.detect_repetitive_tasks(min_occurrences=4)

        # Should detect repetitive tasks
        self.assertGreater(len(patterns), 0)

        # Check pattern structure
        pattern = patterns[0]
        self.assertEqual(pattern['pattern_type'], 'repetitive_task')
        self.assertIn('skill_id', pattern)
        self.assertIn('occurrences', pattern)
        self.assertGreaterEqual(pattern['occurrences'], 4)

    def test_pattern_confidence_calculation(self):
        """Test confidence score calculation for patterns."""
        pattern = {
            'frequency': 10,
            'consistency': 0.9,
            'recency': 1.0
        }

        confidence = self.detector.calculate_confidence(pattern)

        # Confidence should be between 0 and 1
        self.assertGreaterEqual(confidence, 0.0)
        self.assertLessEqual(confidence, 1.0)

        # High frequency and consistency should give high confidence
        self.assertGreater(confidence, 0.7)

    def test_save_patterns(self):
        """Test saving detected patterns to database."""
        patterns = [
            {
                'pattern_type': 'task_sequence',
                'skills': ['skill1', 'skill2'],
                'frequency': 5,
                'confidence': 0.8
            }
        ]

        saved_ids = self.detector.save_patterns(patterns)

        # Should save at least one pattern
        self.assertGreater(len(saved_ids), 0)

        # Verify pattern was saved
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM automation_patterns WHERE id = ?", (saved_ids[0],))
        result = cursor.fetchone()

        self.assertIsNotNone(result)

    def test_get_pattern_by_id(self):
        """Test retrieving a pattern by ID."""
        # First save a pattern
        patterns = [{
            'pattern_type': 'test_pattern',
            'test_data': 'value',
            'confidence': 0.75
        }]
        saved_ids = self.detector.save_patterns(patterns)

        # Retrieve the pattern
        pattern = self.detector.get_pattern_by_id(saved_ids[0])

        # Check retrieved data
        self.assertIsNotNone(pattern)
        self.assertEqual(pattern['pattern_type'], 'test_pattern')
        self.assertEqual(pattern['test_data'], 'value')
        self.assertEqual(pattern['confidence'], 0.75)

    def test_get_recent_patterns(self):
        """Test retrieving recent patterns."""
        # Save some patterns
        patterns = [
            {'pattern_type': 'pattern1', 'confidence': 0.8},
            {'pattern_type': 'pattern2', 'confidence': 0.7},
            {'pattern_type': 'pattern3', 'confidence': 0.9}
        ]
        self.detector.save_patterns(patterns)

        # Get recent patterns
        recent = self.detector.get_recent_patterns(limit=2)

        # Should get at most 2 patterns
        self.assertLessEqual(len(recent), 2)

    def test_full_detection_cycle(self):
        """Test complete detection cycle."""
        # Run all detectors
        all_patterns = self.detector.run_full_detection()

        # Should detect multiple pattern types
        self.assertGreater(len(all_patterns), 0)

        # Check variety of pattern types
        pattern_types = set(p['pattern_type'] for p in all_patterns)
        self.assertGreater(len(pattern_types), 1)


class TestPatternDetectorEdgeCases(unittest.TestCase):
    """Test edge cases and error handling."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_db = TestDatabase()
        self.conn = self.test_db.setup()

        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../.gsd/automation'))
        from pattern_detector import PatternDetector
        self.detector = PatternDetector(self.conn)

    def tearDown(self):
        """Clean up test fixtures."""
        self.test_db.teardown()

    def test_empty_database(self):
        """Test behavior with empty database."""
        # Clear tasks
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM tasks")
        self.conn.commit()

        # Should return empty list, not crash
        patterns = self.detector.detect_task_sequences()
        self.assertEqual(len(patterns), 0)

    def test_invalid_pattern_id(self):
        """Test retrieving non-existent pattern."""
        pattern = self.detector.get_pattern_by_id(99999)
        self.assertIsNone(pattern)

    def test_threshold_filters(self):
        """Test that threshold parameters work correctly."""
        # High threshold should return fewer patterns
        high_threshold = self.detector.detect_task_sequences(min_frequency=10)
        low_threshold = self.detector.detect_task_sequences(min_frequency=2)

        self.assertLessEqual(len(high_threshold), len(low_threshold))

    def test_malformed_pattern_data(self):
        """Test handling of malformed pattern data."""
        # Pattern with missing required fields
        bad_pattern = {'pattern_type': 'test'}  # Missing confidence

        # Should handle gracefully
        try:
            saved_ids = self.detector.save_patterns([bad_pattern])
            # If it saves, that's OK too
        except (KeyError, ValueError):
            # Expected error for malformed data
            pass


if __name__ == '__main__':
    unittest.main()
