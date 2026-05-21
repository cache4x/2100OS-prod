"""Unit tests for action_planner.py"""

import unittest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from .fixtures.test_data import TestDatabase, SAMPLE_PATTERNS


class TestActionPlanner(unittest.TestCase):
    """Test cases for ActionPlanner class."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_db = TestDatabase()
        self.conn = self.test_db.setup()

        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../.gsd/automation'))
        from action_planner import ActionPlanner
        self.planner = ActionPlanner(self.conn)

    def tearDown(self):
        """Clean up test fixtures."""
        self.test_db.teardown()

    def test_plan_create_skill(self):
        """Test planning CREATE_SKILL action."""
        pattern = {
            'pattern_type': 'task_sequence',
            'skills': ['mmc-carrossel', 'mmc-seo'],
            'frequency': 5
        }

        proposal = self.planner.plan_create_skill(pattern)

        # Check proposal structure
        self.assertEqual(proposal['action_type'], 'CREATE_SKILL')
        self.assertIn('title', proposal)
        self.assertIn('description', proposal)
        self.assertIn('skill_name', proposal)
        self.assertIn('skill_actions', proposal)

    def test_plan_optimize_workflow(self):
        """Test planning OPTIMIZE_WORKFLOW action."""
        pattern = {
            'pattern_type': 'inefficiency',
            'skill_id': 'mmc-email-profissional',
            'avg_duration': 150.0,
            'threshold': 120.0
        }

        proposal = self.planner.plan_optimize_workflow(pattern)

        # Check proposal structure
        self.assertEqual(proposal['action_type'], 'OPTIMIZE_WORKFLOW')
        self.assertIn('title', proposal)
        self.assertIn('target_skill', proposal)
        self.assertIn('current_duration', proposal)
        self.assertIn('suggested_improvement', proposal)

    def test_plan_schedule_task(self):
        """Test planning SCHEDULE_TASK action."""
        pattern = {
            'pattern_type': 'temporal_pattern',
            'skill_id': 'mmc-relatorio-ads',
            'schedule': '0 9 * * 1',
            'consistency': 0.95
        }

        proposal = self.planner.plan_schedule_task(pattern)

        # Check proposal structure
        self.assertEqual(proposal['action_type'], 'SCHEDULE_TASK')
        self.assertIn('title', proposal)
        self.assertIn('task_name', proposal)
        self.assertIn('schedule_expression', proposal)
        self.assertIn('task_type', proposal)

    def test_plan_merge_skills(self):
        """Test planning MERGE_SKILLS action."""
        pattern = {
            'pattern_type': 'task_sequence',
            'skills': ['skill1', 'skill2', 'skill3'],
            'frequency': 8
        }

        proposal = self.planner.plan_merge_skills(pattern)

        # Check proposal structure
        self.assertEqual(proposal['action_type'], 'MERGE_SKILLS')
        self.assertIn('title', proposal)
        self.assertIn('skills_to_merge', proposal)
        self.assertIn('merged_skill_name', proposal)

    def test_plan_archive_skill(self):
        """Test planning ARCHIVE_SKILL action."""
        pattern = {
            'pattern_type': 'underutilized_skill',
            'skill_id': 'old-unused-skill',
            'usage_count': 2,
            'last_used': '2024-01-01'
        }

        proposal = self.planner.plan_archive_skill(pattern)

        # Check proposal structure
        self.assertEqual(proposal['action_type'], 'ARCHIVE_SKILL')
        self.assertIn('title', proposal)
        self.assertIn('skill_id', proposal)
        self.assertIn('reason', proposal)

    def test_plan_cleanup(self):
        """Test planning CLEANUP action."""
        proposal = self.planner.plan_cleanup(reason='test', scope='old_patterns')

        # Check proposal structure
        self.assertEqual(proposal['action_type'], 'CLEANUP')
        self.assertIn('title', proposal)
        self.assertIn('cleanup_scope', proposal)

    def test_proposal_title_generation(self):
        """Test generation of descriptive proposal titles."""
        pattern = {
            'pattern_type': 'task_sequence',
            'skills': ['mmc-carrossel', 'mmc-seo'],
            'frequency': 10
        }

        proposal = self.planner.plan_create_skill(pattern)

        # Title should be descriptive and not empty
        self.assertIsNotNone(proposal['title'])
        self.assertGreater(len(proposal['title']), 0)
        # Should mention key aspects
        self.assertTrue(any(word in proposal['title'].lower()
                          for word in ['carrossel', 'seo', 'skill', 'automation']))

    def test_proposal_description_generation(self):
        """Test generation of detailed proposal descriptions."""
        pattern = {
            'pattern_type': 'inefficiency',
            'skill_id': 'slow-task',
            'avg_duration': 200.0
        }

        proposal = self.planner.plan_optimize_workflow(pattern)

        # Description should be detailed
        self.assertIsNotNone(proposal['description'])
        self.assertGreater(len(proposal['description']), 50)

    def test_batch_plan_from_patterns(self):
        """Test creating proposals from multiple patterns."""
        patterns = SAMPLE_PATTERNS

        proposals = self.planner.plan_from_patterns(patterns)

        # Should create proposal for each pattern
        self.assertEqual(len(proposals), len(patterns))

        # Each proposal should have required fields
        for proposal in proposals:
            self.assertIn('action_type', proposal)
            self.assertIn('title', proposal)
            self.assertIn('description', proposal)

    def test_save_proposal(self):
        """Test saving proposal to database."""
        proposal = {
            'proposal_type': 'CREATE_SKILL',
            'title': 'Test Proposal',
            'description': 'Test description',
            'impact_score': 0.8,
            'confidence_score': 0.7
        }

        proposal_id = self.planner.save_proposal(proposal)

        # Should return valid ID
        self.assertIsNotNone(proposal_id)
        self.assertGreater(proposal_id, 0)

        # Verify in database
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM automation_proposals WHERE id = ?", (proposal_id,))
        result = cursor.fetchone()
        self.assertIsNotNone(result)

    def test_proposal_impact_scoring(self):
        """Test calculation of impact scores."""
        # High frequency pattern should have high impact
        high_freq_pattern = {'frequency': 20, 'consistency': 0.9}
        high_impact = self.planner.calculate_impact(high_freq_pattern)

        # Low frequency pattern should have low impact
        low_freq_pattern = {'frequency': 2, 'consistency': 0.5}
        low_impact = self.planner.calculate_impact(low_freq_pattern)

        self.assertGreater(high_impact, low_impact)

    def test_action_type_selection(self):
        """Test correct action type selection for patterns."""
        test_cases = [
            ('task_sequence', 'CREATE_SKILL'),
            ('inefficiency', 'OPTIMIZE_WORKFLOW'),
            ('temporal_pattern', 'SCHEDULE_TASK'),
            ('underutilized_skill', 'ARCHIVE_SKILL')
        ]

        for pattern_type, expected_action in test_cases:
            pattern = {'pattern_type': pattern_type}
            action = self.planner.determine_action_type(pattern)
            self.assertEqual(action, expected_action,
                           f"Pattern {pattern_type} should map to {expected_action}")


class TestActionPlannerEdgeCases(unittest.TestCase):
    """Test edge cases and error handling."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_db = TestDatabase()
        self.conn = self.test_db.setup()

        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../.gsd/automation'))
        from action_planner import ActionPlanner
        self.planner = ActionPlanner(self.conn)

    def tearDown(self):
        """Clean up test fixtures."""
        self.test_db.teardown()

    def test_unknown_pattern_type(self):
        """Test handling of unknown pattern types."""
        unknown_pattern = {'pattern_type': 'unknown_type'}

        # Should handle gracefully or raise appropriate error
        try:
            proposal = self.planner.plan_from_patterns([unknown_pattern])
            # If it doesn't crash, check for graceful handling
            if proposal:
                self.assertIn('action_type', proposal[0])
        except ValueError:
            # Expected for unknown pattern type
            pass

    def test_malformed_pattern_data(self):
        """Test handling of malformed pattern data."""
        malformed_patterns = [
            {},  # Empty pattern
            {'pattern_type': 'task_sequence'},  # Missing required fields
            {'pattern_type': 'inefficiency', 'avg_duration': 'invalid'}  # Invalid data type
        ]

        for pattern in malformed_patterns:
            try:
                proposals = self.planner.plan_from_patterns([pattern])
                # If it doesn't crash, verify output is safe
                if proposals:
                    self.assertTrue(isinstance(proposals, list))
            except (KeyError, ValueError, TypeError):
                # Expected for malformed data
                pass

    def test_empty_patterns_list(self):
        """Test planning from empty patterns list."""
        proposals = self.planner.plan_from_patterns([])

        # Should return empty list
        self.assertEqual(len(proposals), 0)

    def test_proposal_with_minimal_data(self):
        """Test saving proposal with minimal required data."""
        minimal_proposal = {
            'proposal_type': 'TEST',
            'title': 'Minimal'
        }

        # Should save without crashing
        try:
            proposal_id = self.planner.save_proposal(minimal_proposal)
            self.assertIsNotNone(proposal_id)
        except KeyError:
            # Missing required fields is acceptable
            pass


if __name__ == '__main__':
    unittest.main()
