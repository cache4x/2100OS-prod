"""Integration tests for autopilot system"""

import unittest
import sys
import os
from datetime import datetime
from unittest.mock import Mock, patch

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from ..fixtures.test_data import TestDatabase, SAMPLE_PROPOSALS


class TestAutopilotIntegration(unittest.TestCase):
    """Test autopilot integration with other components."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_db = TestDatabase()
        self.conn = self.test_db.setup()

        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../2100OS/.gsd/automation'))

        from autopilot import Autopilot
        from pattern_detector import PatternDetector
        from action_planner import ActionPlanner
        from execution_engine import ExecutionEngine

        self.autopilot = Autopilot(self.conn)
        self.detector = PatternDetector(self.conn)
        self.planner = ActionPlanner(self.conn)
        self.engine = ExecutionEngine(self.conn)

    def tearDown(self):
        """Clean up test fixtures."""
        if hasattr(self, 'autopilot'):
            self.autopilot.stop()
        self.test_db.teardown()

    def test_autopilot_with_ml_detector(self):
        """Test autopilot using ML-detected patterns."""
        # Detect patterns using ML
        from ml_pattern_detector import MLPatternDetector
        ml_detector = MLPatternDetector(self.conn)

        features = ml_detector.extract_features(skill_id='mmc-carrossel')
        self.assertIsNotNone(features)

        # Create proposals from detected patterns
        patterns = self.detector.run_full_detection()
        if len(patterns) > 0:
            proposals = self.planner.plan_from_patterns(patterns)

            # Evaluate with autopilot
            for proposal in proposals:
                decision = self.autopilot.evaluate_proposal(proposal)
                self.assertIn('auto_approve', decision)

    def test_autopilot_feedback_loop(self):
        """Test autopilot learning from feedback."""
        # Set mode to BALANCED
        self.autopilot.set_mode('BALANCED')

        # Simulate proposal evaluations
        for i in range(10):
            proposal = {
                'id': i,
                'proposal_type': 'SCHEDULE_TASK',
                'confidence_score': 0.8 + (i * 0.01),
                'risk_level': 'LOW'
            }

            decision = self.autopilot.evaluate_proposal(proposal)

            # Record feedback
            self.autopilot.record_feedback(
                proposal_id=i,
                was_correct=True,
                actual_outcome='success'
            )

        # Check learning occurred
        insights = self.autopilot.get_learning_insights()

        self.assertEqual(insights['total_decisions'], 10)
        self.assertGreater(insights['success_rate'], 0.7)

    def test_autopilot_execution_pipeline(self):
        """Test full autopilot execution pipeline."""
        # Create pending proposals
        cursor = self.conn.cursor()
        proposal_ids = []

        for i in range(3):
            cursor.execute("""
                INSERT INTO automation_proposals
                (proposal_type, title, description, impact_score, confidence_score, risk_level, status)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, ('SCHEDULE_TASK', f'Auto Task {i}', f'Description {i}', 0.8, 0.9, 'LOW', 'pending'))
            self.conn.commit()
            proposal_ids.append(cursor.lastrowid)

        # Run autopilot cycle (dry-run)
        with patch.object(self.autopilot, 'execute_proposal') as mock_exec:
            mock_exec.return_value = {'success': True}

            results = self.autopilot.run_cycle(dry_run=True, limit=5)

        # Should process proposals
        self.assertIn('processed', results)
        self.assertGreater(results['processed'], 0)

    def test_mode_switching_during_operation(self):
        """Test switching autopilot modes."""
        # Start in CONSERVATIVE
        self.autopilot.set_mode('CONSERVATIVE')
        self.assertEqual(self.autopilot.get_mode(), 'CONSERVATIVE')

        # Create proposal
        proposal = {
            'id': 1,
            'proposal_type': 'SCHEDULE_TASK',
            'confidence_score': 0.8,
            'risk_level': 'LOW'
        }

        conservative_decision = self.autopilot.evaluate_proposal(proposal)

        # Switch to AGGRESSIVE
        self.autopilot.set_mode('AGGRESSIVE')
        self.assertEqual(self.autopilot.get_mode(), 'AGGRESSIVE')

        aggressive_decision = self.autopilot.evaluate_proposal(proposal)

        # AGGRESSIVE should be more likely to approve
        self.assertLessEqual(
            conservative_decision['confidence'],
            aggressive_decision['confidence']
        )

    def test_autopilot_health_monitoring(self):
        """Test autopilot health monitoring."""
        # Perform some operations
        for i in range(5):
            proposal = {
                'id': i,
                'proposal_type': 'SCHEDULE_TASK',
                'confidence_score': 0.8,
                'risk_level': 'LOW'
            }

            self.autopilot.evaluate_proposal(proposal)
            self.autopilot.record_feedback(i, was_correct=True, actual_outcome='success')

        # Check health
        health = self.autopilot.get_health_status()

        self.assertIn('overall_health', health)
        self.assertIn('success_rate', health)

        # Should have good health after successful operations
        self.assertGreater(health['overall_health'], 0.7)

    def test_autopilot_configuration_persistence(self):
        """Test that autopilot configuration persists."""
        # Set configuration
        self.autopilot.set_config('test_key', 'test_value')
        self.autopilot.set_mode('BALANCED')

        # Create new instance (simulate restart)
        from autopilot import Autopilot
        new_autopilot = Autopilot(self.conn)

        # Should retrieve configuration
        mode = new_autopilot.get_mode()
        value = new_autopilot.get_config('test_key')

        self.assertIsNotNone(mode)
        self.assertEqual(value, 'test_value')

        new_autopilot.stop()

    def test_autopilot_error_recovery(self):
        """Test autopilot recovery from errors."""
        # Create proposal that will fail
        proposal = {
            'id': 1,
            'proposal_type': 'INVALID_TYPE',
            'confidence_score': 0.8
        }

        # Should handle error gracefully
        decision = self.autopilot.evaluate_proposal(proposal)

        self.assertIn('auto_approve', decision)
        # Should default to safe decision
        self.assertFalse(decision['auto_approve'])

    def test_batch_proposal_evaluation(self):
        """Test evaluation of multiple proposals."""
        proposals = SAMPLE_PROPOSALS

        evaluations = self.autopilot.evaluate_batch(proposals)

        # Should evaluate all proposals
        self.assertEqual(len(evaluations), len(proposals))

        # Check evaluation structure
        for eval in evaluations:
            self.assertIn('auto_approve', eval)
            self.assertIn('confidence', eval)

    def test_autopilot_with_scheduler(self):
        """Test autopilot integration with scheduler."""
        # Create schedule that triggers autopilot
        from scheduler import AutomationScheduler
        scheduler = AutomationScheduler(self.conn)

        schedule_id = scheduler.create_schedule({
            'task_name': 'autopilot_cycle',
            'task_type': 'skill',
            'schedule_expression': '0 * * * *',
            'parameters': {'action': 'run_autopilot_cycle'}
        })

        # Schedule should be created
        schedule = scheduler.get_schedule_by_id(schedule_id)
        self.assertIsNotNone(schedule)
        self.assertEqual(schedule['task_name'], 'autopilot_cycle')


class TestAutopilotScenarios(unittest.TestCase):
    """Test real-world autopilot scenarios."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_db = TestDatabase()
        self.conn = self.test_db.setup()

        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../2100OS/.gsd/automation'))

        from autopilot import Autopilot
        self.autopilot = Autopilot(self.conn)

    def tearDown(self):
        """Clean up test fixtures."""
        if hasattr(self, 'autopilot'):
            self.autopilot.stop()
        self.test_db.teardown()

    def test_weekly_report_scenario(self):
        """Test scenario: Auto-approve weekly report generation."""
        # Simulate weekly report proposal
        proposal = {
            'id': 1,
            'proposal_type': 'SCHEDULE_TASK',
            'title': 'Weekly Analytics Report',
            'description': 'Generate weekly analytics report every Monday at 9am',
            'confidence_score': 0.95,
            'risk_level': 'LOW',
            'impact_score': 0.7,
            'action_params': {
                'task_name': 'weekly_analytics_report',
                'schedule_expression': '0 9 * * 1',
                'task_type': 'report'
            }
        }

        # Should auto-approve
        self.autopilot.set_mode('BALANCED')
        decision = self.autopilot.evaluate_proposal(proposal)

        self.assertTrue(decision['auto_approve'])
        self.assertGreater(decision['confidence'], 0.8)

    def test_skill_creation_scenario(self):
        """Test scenario: Require approval for new skill creation."""
        proposal = {
            'id': 2,
            'proposal_type': 'CREATE_SKILL',
            'title': 'New Content Skill',
            'description': 'Create skill for content sequence',
            'confidence_score': 0.8,
            'risk_level': 'MEDIUM',
            'impact_score': 0.8
        }

        # Should require approval
        self.autopilot.set_mode('CONSERVATIVE')
        decision = self.autopilot.evaluate_proposal(proposal)

        # CONSERVATIVE mode should not auto-approve MEDIUM risk
        self.assertFalse(decision['auto_approve'])

    def test_high_risk_scenario(self):
        """Test scenario: Never auto-approve high-risk actions."""
        proposal = {
            'id': 3,
            'proposal_type': 'DELETE_SKILL',
            'title': 'Delete Unused Skill',
            'description': 'Delete skill that has not been used',
            'confidence_score': 0.9,
            'risk_level': 'HIGH',
            'impact_score': 0.6,
            'is_destructive': True,
            'is_reversible': False
        }

        # Should never auto-approve, regardless of mode
        for mode in ['CONSERVATIVE', 'BALANCED', 'AGGRESSIVE']:
            self.autopilot.set_mode(mode)
            decision = self.autopilot.evaluate_proposal(proposal)
            self.assertFalse(decision['auto_approve'],
                           f'HIGH risk should not be auto-approved in {mode} mode')

    def test_learning_from_mistakes_scenario(self):
        """Test scenario: Autopilot learns from incorrect decisions."""
        # Simulate incorrect auto-approval
        self.autopilot.record_decision(
            proposal_id=1,
            proposal_type='SCHEDULE_TASK',
            decision='approved',
            confidence=0.85
        )

        # Record that it was incorrect
        self.autopilot.record_feedback(
            proposal_id=1,
            was_correct=False,
            actual_outcome='error'
        )

        # Check that success rate decreased
        insights = self.autopilot.get_learning_insights()
        self.assertLess(insights['success_rate'], 1.0)

        # Next similar proposal should have lower confidence
        proposal = {
            'id': 2,
            'proposal_type': 'SCHEDULE_TASK',
            'confidence_score': 0.85,
            'risk_level': 'LOW'
        }

        decision = self.autopilot.evaluate_proposal(proposal)

        # Should be more cautious
        self.assertLess(decision['confidence'], 0.9)


if __name__ == '__main__':
    unittest.main()
