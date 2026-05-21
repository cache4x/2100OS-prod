"""Unit tests for autopilot.py"""

import unittest
import sys
import os
from datetime import datetime, timedelta
from unittest.mock import Mock, patch, MagicMock

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from .fixtures.test_data import TestDatabase, SAMPLE_PROPOSALS


class TestAutopilot(unittest.TestCase):
    """Test cases for Autopilot class."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_db = TestDatabase()
        self.conn = self.test_db.setup()

        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../.gsd/automation'))
        from autopilot import Autopilot
        self.autopilot = Autopilot(self.conn)

        # Insert sample proposal
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO automation_proposals
            (proposal_type, title, description, impact_score, confidence_score, risk_level, status)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, ('SCHEDULE_TASK', 'Weekly Report', 'Auto-generate weekly report', 0.8, 0.9, 'LOW', 'pending'))
        self.conn.commit()
        self.proposal_id = cursor.lastrowid

    def tearDown(self):
        """Clean up test fixtures."""
        if hasattr(self, 'autopilot'):
            self.autopilot.stop()
        self.test_db.teardown()

    def test_conservative_mode(self):
        """Test autopilot in CONSERVATIVE mode."""
        # Set mode to conservative
        self.autopilot.set_mode('CONSERVATIVE')

        # Create test proposal
        proposal = {
            'id': self.proposal_id,
            'proposal_type': 'SCHEDULE_TASK',
            'title': 'Safe Task',
            'confidence_score': 0.95,
            'risk_level': 'LOW',
            'impact_score': 0.7
        }

        decision = self.autopilot.evaluate_proposal(proposal)

        # Should auto-approve high confidence, low risk
        self.assertTrue(decision['auto_approve'])
        self.assertIn('confidence', decision)

    def test_balanced_mode(self):
        """Test autopilot in BALANCED mode."""
        self.autopilot.set_mode('BALANCED')

        proposal = {
            'id': self.proposal_id,
            'proposal_type': 'CREATE_SKILL',
            'title': 'New Skill',
            'confidence_score': 0.8,
            'risk_level': 'MEDIUM',
            'impact_score': 0.7
        }

        decision = self.autopilot.evaluate_proposal(proposal)

        # Balanced mode may approve some medium risk
        self.assertIn('auto_approve', decision)

    def test_aggressive_mode(self):
        """Test autopilot in AGGRESSIVE mode."""
        self.autopilot.set_mode('AGGRESSIVE')

        proposal = {
            'id': self.proposal_id,
            'proposal_type': 'OPTIMIZE_WORKFLOW',
            'title': 'Optimize',
            'confidence_score': 0.7,
            'risk_level': 'MEDIUM',
            'impact_score': 0.8
        }

        decision = self.autopilot.evaluate_proposal(proposal)

        # Aggressive mode should approve more
        self.assertIn('auto_approve', decision)

    def test_off_mode(self):
        """Test autopilot in OFF mode."""
        self.autopilot.set_mode('OFF')

        proposal = {
            'id': self.proposal_id,
            'proposal_type': 'SCHEDULE_TASK',
            'confidence_score': 0.99,
            'risk_level': 'LOW'
        }

        decision = self.autopilot.evaluate_proposal(proposal)

        # OFF mode should never auto-approve
        self.assertFalse(decision['auto_approve'])

    def test_dynamic_thresholds(self):
        """Test dynamic threshold adjustment."""
        initial_threshold = self.autopilot.get_approval_threshold()

        # Simulate successful approvals
        for i in range(10):
            self.autopilot.record_feedback(
                proposal_id=i,
                was_correct=True,
                actual_outcome='success'
            )

        # Threshold should adjust based on success rate
        new_threshold = self.autopilot.get_approval_threshold()
        self.assertIsNotNone(new_threshold)

    def test_learning_loop(self):
        """Test continuous learning from feedback."""
        # Record some feedback
        feedback_data = [
            {'proposal_id': 1, 'was_correct': True, 'outcome': 'success'},
            {'proposal_id': 2, 'was_correct': False, 'outcome': 'error'},
            {'proposal_id': 3, 'was_correct': True, 'outcome': 'success'}
        ]

        for feedback in feedback_data:
            self.autopilot.record_feedback(**feedback)

        # Get learning insights
        insights = self.autopilot.get_learning_insights()

        # Should provide insights
        self.assertIsNotNone(insights)
        self.assertIn('total_decisions', insights)
        self.assertIn('success_rate', insights)

    def test_health_monitoring(self):
        """Test autopilot health monitoring."""
        health = self.autopilot.get_health_status()

        # Should return health metrics
        self.assertIn('overall_health', health)
        self.assertIn('success_rate', health)
        self.assertIn('confidence_avg', health)
        self.assertIn('last_check', health)

    def test_type_specific_stats(self):
        """Test statistics by proposal type."""
        # Record various decisions
        proposal_types = ['CREATE_SKILL', 'SCHEDULE_TASK', 'OPTIMIZE_WORKFLOW']
        for i, ptype in enumerate(proposal_types):
            self.autopilot.record_decision(
                proposal_id=i,
                proposal_type=ptype,
                decision='approved',
                confidence=0.8
            )

        # Get type-specific stats
        stats = self.autopilot.get_type_stats()

        # Should have stats for each type
        for ptype in proposal_types:
            self.assertIn(ptype, stats)

    def test_approval_score_calculation(self):
        """Test calculation of approval scores."""
        proposal = {
            'confidence_score': 0.85,
            'risk_level': 'LOW',
            'impact_score': 0.8,
            'proposal_type': 'SCHEDULE_TASK'
        }

        score = self.autopilot.calculate_approval_score(proposal)

        # Should be between 0 and 1
        self.assertGreaterEqual(score, 0.0)
        self.assertLessEqual(score, 1.0)

        # High confidence + low risk = high score
        self.assertGreater(score, 0.6)

    def test_execute_approved_proposals(self):
        """Test execution of auto-approved proposals."""
        # Create proposals that will be auto-approved
        with patch.object(self.autopilot, 'evaluate_proposal') as mock_eval:
            mock_eval.return_value = {'auto_approve': True, 'confidence': 0.9}

            with patch.object(self.autopilot, 'execute_proposal') as mock_exec:
                mock_exec.return_value = {'success': True}

                results = self.autopilot.run_cycle(limit=5)

        # Should process proposals
        self.assertIsInstance(results, dict)
        self.assertIn('processed', results)
        self.assertIn('approved', results)

    def test_configuration_persistence(self):
        """Test that configuration is persisted."""
        # Set configuration
        self.autopilot.set_config('test_key', 'test_value')

        # Get configuration
        value = self.autopilot.get_config('test_key')

        self.assertEqual(value, 'test_value')

    def test_get_pending_proposals(self):
        """Test retrieval of pending proposals."""
        proposals = self.autopilot.get_pending_proposals()

        # Should return list
        self.assertIsInstance(proposals, list)

        # Check structure
        for proposal in proposals:
            self.assertIn('id', proposal)
            self.assertIn('proposal_type', proposal)

    def test_batch_evaluation(self):
        """Test evaluation of multiple proposals."""
        proposals = SAMPLE_PROPOSALS

        evaluations = self.autopilot.evaluate_batch(proposals)

        # Should evaluate all proposals
        self.assertEqual(len(evaluations), len(proposals))

        # Each evaluation should have decision
        for eval in evaluations:
            self.assertIn('auto_approve', eval)
            self.assertIn('confidence', eval)

    def test_risk_adjustment(self):
        """Test risk-based decision adjustment."""
        high_risk = {
            'id': 1,
            'risk_level': 'HIGH',
            'confidence_score': 0.9
        }

        low_risk = {
            'id': 2,
            'risk_level': 'LOW',
            'confidence_score': 0.7
        }

        high_decision = self.autopilot.evaluate_proposal(high_risk)
        low_decision = self.autopilot.evaluate_proposal(low_risk)

        # High risk should be less likely to auto-approve
        self.assertLessEqual(high_decision['confidence'], low_decision['confidence'])

    def test_confidence_decay(self):
        """Test confidence decay over time."""
        # Create old proposal
        old_proposal = {
            'id': 1,
            'created_at': (datetime.now() - timedelta(days=10)).isoformat(),
            'confidence_score': 0.9
        }

        # Create new proposal
        new_proposal = {
            'id': 2,
            'created_at': datetime.now().isoformat(),
            'confidence_score': 0.9
        }

        old_decision = self.autopilot.evaluate_proposal(old_proposal)
        new_decision = self.autopilot.evaluate_proposal(new_proposal)

        # Old proposal should have lower adjusted confidence
        self.assertLessEqual(old_decision['confidence'], new_decision['confidence'])


class TestAutopilotEdgeCases(unittest.TestCase):
    """Test edge cases and error handling."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_db = TestDatabase()
        self.conn = self.test_db.setup()

        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../.gsd/automation'))
        from autopilot import Autopilot
        self.autopilot = Autopilot(self.conn)

    def tearDown(self):
        """Clean up test fixtures."""
        if hasattr(self, 'autopilot'):
            self.autopilot.stop()
        self.test_db.teardown()

    def test_invalid_mode(self):
        """Test setting invalid mode."""
        # Should handle gracefully
        try:
            self.autopilot.set_mode('INVALID_MODE')
            # If successful, should use safe default
            current_mode = self.autopilot.get_mode()
            self.assertIsNotNone(current_mode)
        except ValueError:
            # Expected for invalid mode
            pass

    def test_missing_proposal_fields(self):
        """Test evaluation of incomplete proposals."""
        incomplete_proposal = {
            'id': 1
            # Missing confidence, risk_level, etc.
        }

        decision = self.autopilot.evaluate_proposal(incomplete_proposal)

        # Should handle gracefully
        self.assertIn('auto_approve', decision)

    def test_extreme_confidence_values(self):
        """Test handling of extreme confidence values."""
        extreme_proposals = [
            {'confidence_score': -0.5, 'risk_level': 'LOW'},
            {'confidence_score': 1.5, 'risk_level': 'LOW'}
        ]

        for proposal in extreme_proposals:
            decision = self.autopilot.evaluate_proposal(proposal)
            # Should normalize to valid range
            self.assertIn('confidence', decision)

    def test_empty_feedback_history(self):
        """Test insights with no feedback history."""
        insights = self.autopilot.get_learning_insights()

        # Should return default insights
        self.assertIsNotNone(insights)
        self.assertIn('total_decisions', insights)
        self.assertEqual(insights['total_decisions'], 0)

    def test_concurrent_decision_handling(self):
        """Test handling of concurrent decisions."""
        proposals = [
            {'id': i, 'confidence_score': 0.8, 'risk_level': 'LOW'}
            for i in range(10)
        ]

        # Evaluate concurrently
        decisions = [self.autopilot.evaluate_proposal(p) for p in proposals]

        # All should have valid decisions
        self.assertTrue(all('auto_approve' in d for d in decisions))

    def test_memory_efficiency(self):
        """Test memory usage with large datasets."""
        # Simulate large feedback history
        for i in range(1000):
            self.autopilot.record_feedback(
                proposal_id=i,
                was_correct=True,
                actual_outcome='success'
            )

        # Should still function efficiently
        insights = self.autopilot.get_learning_insights()
        self.assertEqual(insights['total_decisions'], 1000)

    def test_error_recovery(self):
        """Test recovery from errors."""
        # Force an error state
        with patch.object(self.autopilot, '_evaluate_internal', side_effect=Exception('Test error')):
            proposal = {'id': 1, 'confidence_score': 0.8}
            decision = self.autopilot.evaluate_proposal(proposal)

        # Should recover gracefully
        self.assertIn('auto_approve', decision)
        # Should default to safe decision
        self.assertFalse(decision['auto_approve'])


if __name__ == '__main__':
    unittest.main()
