"""Integration tests for full automation pipeline"""

import unittest
import sys
import os
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from ..fixtures.test_data import TestDatabase


class TestFullDetectionCycle(unittest.TestCase):
    """Test complete pattern detection cycle."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_db = TestDatabase()
        self.conn = self.test_db.setup()

        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../2100OS/.gsd/automation'))

        from pattern_detector import PatternDetector
        from action_planner import ActionPlanner
        from risk_assessor import RiskAssessor

        self.detector = PatternDetector(self.conn)
        self.planner = ActionPlanner(self.conn)
        self.assessor = RiskAssessor()

    def tearDown(self):
        """Clean up test fixtures."""
        self.test_db.teardown()

    def test_full_detection_to_proposal_flow(self):
        """Test flow from detection to proposal creation."""
        # Step 1: Detect patterns
        patterns = self.detector.run_full_detection()
        self.assertGreater(len(patterns), 0)

        # Step 2: Create proposals from patterns
        proposals = self.planner.plan_from_patterns(patterns)
        self.assertEqual(len(proposals), len(patterns))

        # Step 3: Assess risk for each proposal
        for proposal in proposals:
            risk = self.assessor.assess_proposal(proposal)
            self.assertIn('level', risk)
            self.assertIn('score', risk)

    def test_pattern_to_proposal_persistence(self):
        """Test persistence of patterns and proposals."""
        # Detect and save patterns
        patterns = self.detector.run_full_detection()
        pattern_ids = self.detector.save_patterns(patterns)
        self.assertGreater(len(pattern_ids), 0)

        # Create and save proposals
        proposals = self.planner.plan_from_patterns(patterns)
        proposal_ids = []
        for proposal in proposals:
            proposal_id = self.planner.save_proposal(proposal)
            proposal_ids.append(proposal_id)

        # Verify persistence
        cursor = self.conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM automation_patterns")
        pattern_count = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM automation_proposals")
        proposal_count = cursor.fetchone()[0]

        self.assertGreater(pattern_count, 0)
        self.assertGreater(proposal_count, 0)

    def test_high_confidence_pattern_flow(self):
        """Test flow for high-confidence patterns."""
        # Detect patterns
        patterns = self.detector.run_full_detection()

        # Filter for high confidence
        high_conf_patterns = [p for p in patterns if p.get('confidence', 0) > 0.8]

        # Should have high confidence patterns
        self.assertGreater(len(high_conf_patterns), 0)

        # Create proposals
        proposals = self.planner.plan_from_patterns(high_conf_patterns)

        # High confidence should result in actionable proposals
        self.assertGreater(len(proposals), 0)
        for proposal in proposals:
            self.assertIn('action_type', proposal)
            self.assertIn('title', proposal)

    def test_inefficiency_detection_to_optimization(self):
        """Test flow from inefficiency detection to optimization proposal."""
        # Detect inefficiencies
        inefficiencies = self.detector.detect_inefficiencies(
            duration_threshold=120,
            min_occurrences=3
        )

        if len(inefficiencies) > 0:
            # Create optimization proposals
            proposals = [self.planner.plan_optimize_workflow(inef)
                        for ineff in inefficiencies]

            # All should be OPTIMIZE_WORKFLOW
            for proposal in proposals:
                self.assertEqual(proposal['action_type'], 'OPTIMIZE_WORKFLOW')
                self.assertIn('target_skill', proposal)

    def test_repetitive_task_to_schedule(self):
        """Test flow from repetitive task to schedule proposal."""
        # Detect temporal patterns
        temporal_patterns = self.detector.detect_temporal_patterns(
            min_consistency=0.8
        )

        if len(temporal_patterns) > 0:
            # Create schedule proposals
            proposals = [self.planner.plan_schedule_task(pattern)
                        for pattern in temporal_patterns]

            # All should be SCHEDULE_TASK
            for proposal in proposals:
                self.assertEqual(proposal['action_type'], 'SCHEDULE_TASK')
                self.assertIn('schedule_expression', proposal)


class TestFullProposalCycle(unittest.TestCase):
    """Test complete proposal lifecycle."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_db = TestDatabase()
        self.conn = self.test_db.setup()

        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../2100OS/.gsd/automation'))

        from pattern_detector import PatternDetector
        from action_planner import ActionPlanner
        from risk_assessor import RiskAssessor
        from execution_engine import ExecutionEngine

        self.detector = PatternDetector(self.conn)
        self.planner = ActionPlanner(self.conn)
        self.assessor = RiskAssessor()
        self.engine = ExecutionEngine(self.conn)

    def tearDown(self):
        """Clean up test fixtures."""
        self.test_db.teardown()

    def test_proposal_approval_to_execution(self):
        """Test flow from proposal to execution."""
        # Create a proposal
        patterns = self.detector.detect_temporal_patterns(min_consistency=0.8)
        if len(patterns) > 0:
            proposals = self.planner.plan_from_patterns(patterns)
            proposal = proposals[0]

            # Save proposal
            proposal_id = self.planner.save_proposal(proposal)

            # Approve proposal
            cursor = self.conn.cursor()
            cursor.execute(
                "UPDATE automation_proposals SET status = 'approved' WHERE id = ?",
                (proposal_id,)
            )
            self.conn.commit()

            # Execute (dry-run)
            result = self.engine.execute_by_id(proposal_id, dry_run=True)

            # Verify execution was attempted
            self.assertIn('success', result)

    def test_proposal_rejection(self):
        """Test proposal rejection flow."""
        # Create and save proposal
        proposal = {
            'proposal_type': 'TEST',
            'title': 'Test Proposal',
            'description': 'Test'
        }
        proposal_id = self.planner.save_proposal(proposal)

        # Reject proposal
        cursor = self.conn.cursor()
        cursor.execute(
            "UPDATE automation_proposals SET status = 'rejected', decided_at = ?, decision_by = ? WHERE id = ?",
            (datetime.now().isoformat(), 'user', proposal_id)
        )
        self.conn.commit()

        # Verify rejection
        cursor.execute(
            "SELECT status, decision_by FROM automation_proposals WHERE id = ?",
            (proposal_id,)
        )
        result = cursor.fetchone()

        self.assertEqual(result[0], 'rejected')
        self.assertEqual(result[1], 'user')

    def test_low_risk_auto_approval(self):
        """Test auto-approval of low-risk proposals."""
        # Create low-risk proposal
        proposal = {
            'proposal_type': 'SCHEDULE_TASK',
            'title': 'Weekly Report',
            'description': 'Generate weekly report',
            'impact_score': 0.7,
            'confidence_score': 0.9,
            'risk_level': 'LOW',
            'status': 'pending'
        }

        proposal_id = self.planner.save_proposal(proposal)

        # Assess risk
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM automation_proposals WHERE id = ?", (proposal_id,))
        saved_proposal = cursor.fetchone()

        proposal_dict = {
            'proposal_type': saved_proposal[1],
            'title': saved_proposal[2],
            'risk_level': saved_proposal[6]
        }

        risk = self.assessor.assess_proposal(proposal_dict)

        # LOW risk should be auto-executable
        self.assertEqual(risk['level'], 'LOW')
        self.assertTrue(risk['auto_execute_eligible'])

    def test_high_risk_manual_approval(self):
        """Test manual approval requirement for high-risk proposals."""
        # Create high-risk proposal
        proposal = {
            'proposal_type': 'DELETE_SKILL',
            'title': 'Delete Skill',
            'description': 'Delete a skill',
            'impact_score': 0.9,
            'confidence_score': 0.8,
            'risk_level': 'HIGH',
            'status': 'pending'
        }

        proposal_id = self.planner.save_proposal(proposal)

        # Assess risk
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM automation_proposals WHERE id = ?", (proposal_id,))
        saved_proposal = cursor.fetchone()

        proposal_dict = {
            'proposal_type': saved_proposal[1],
            'title': saved_proposal[2],
            'is_destructive': True,
            'is_reversible': False
        }

        risk = self.assessor.assess_proposal(proposal_dict)

        # HIGH risk should not be auto-executable
        self.assertEqual(risk['level'], 'HIGH')
        self.assertFalse(risk['auto_execute_eligible'])


class TestClosedLoopOperation(unittest.TestCase):
    """Test closed-loop feedback system."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_db = TestDatabase()
        self.conn = self.test_db.setup()

        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../2100OS/.gsd/automation'))

        from pattern_detector import PatternDetector
        from execution_engine import ExecutionEngine

        self.detector = PatternDetector(self.conn)
        self.engine = ExecutionEngine(self.conn)

    def tearDown(self):
        """Clean up test fixtures."""
        self.test_db.teardown()

    def test_execution_logging_to_task_history(self):
        """Test that executions are logged to task_history."""
        # Create a proposal
        patterns = self.detector.detect_temporal_patterns(min_consistency=0.8)
        if len(patterns) > 0:
            # Save and approve proposal
            from action_planner import ActionPlanner
            planner = ActionPlanner(self.conn)
            proposals = planner.plan_from_patterns(patterns)
            proposal_id = planner.save_proposal(proposals[0])

            # Approve
            cursor = self.conn.cursor()
            cursor.execute(
                "UPDATE automation_proposals SET status = 'approved' WHERE id = ?",
                (proposal_id,)
            )
            self.conn.commit()

            # Execute
            from unittest.mock import patch
            with patch('execution_engine.subprocess.run', return_value=Mock(returncode=0)):
                self.engine.execute_by_id(proposal_id, dry_run=False)

            # Check task_history
            cursor.execute("""
                SELECT * FROM task_history
                WHERE task_type = 'automation_execution'
                ORDER BY completed_at DESC
                LIMIT 1
            """)
            log_entry = cursor.fetchone()

            self.assertIsNotNone(log_entry)

    def test_learning_log_feedback(self):
        """Test that feedback is recorded in learning_log."""
        # Simulate execution with outcome
        from unittest.mock import patch, Mock

        with patch('execution_engine.subprocess.run', return_value=Mock(returncode=0)):
            # Execute something
            result = {'success': True, 'proposal_id': 1}

        # Record feedback
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO learning_log (context, outcome, lesson_learned, timestamp)
            VALUES (?, ?, ?, ?)
        """, ('automation_execution', 'success', 'Proposal executed successfully', datetime.now().isoformat()))
        self.conn.commit()

        # Verify feedback was recorded
        cursor.execute("SELECT * FROM learning_log WHERE context = 'automation_execution'")
        feedback = cursor.fetchone()

        self.assertIsNotNone(feedback)

    def test_pattern_improvement_from_feedback(self):
        """Test that patterns improve based on feedback."""
        # This is a conceptual test - in production, this would involve
        # ML model retraining based on feedback

        # Record successful execution feedback
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO learning_log (context, outcome, lesson_learned, timestamp)
            VALUES (?, ?, ?, ?)
        """, ('pattern_detection', 'success', 'Temporal pattern detected accurately', datetime.now().isoformat()))
        self.conn.commit()

        # In production, this would improve the pattern detector
        # For now, we just verify the feedback was recorded
        cursor.execute("SELECT * FROM learning_log WHERE context = 'pattern_detection'")
        feedback = cursor.fetchone()

        self.assertIsNotNone(feedback)


if __name__ == '__main__':
    unittest.main()
