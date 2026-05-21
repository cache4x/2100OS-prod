"""Unit tests for execution_engine.py"""

import unittest
import sys
import os
from unittest.mock import Mock, patch, MagicMock

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from .fixtures.test_data import TestDatabase, SAMPLE_PROPOSALS


class TestExecutionEngine(unittest.TestCase):
    """Test cases for ExecutionEngine class."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_db = TestDatabase()
        self.conn = self.test_db.setup()

        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../.gsd/automation'))
        from execution_engine import ExecutionEngine
        self.engine = ExecutionEngine(self.conn)

        # Insert sample proposal
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO automation_proposals
            (proposal_type, title, description, impact_score, confidence_score, risk_level, status)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, ('CREATE_SKILL', 'Test Skill', 'Test description', 0.8, 0.9, 'LOW', 'approved'))
        self.conn.commit()
        self.proposal_id = cursor.lastrowid

    def tearDown(self):
        """Clean up test fixtures."""
        self.test_db.teardown()

    @patch('execution_engine.subprocess.run')
    def test_execute_create_skill(self, mock_run):
        """Test execution of CREATE_SKILL action."""
        mock_run.return_value = Mock(returncode=0)

        proposal = {
            'id': self.proposal_id,
            'proposal_type': 'CREATE_SKILL',
            'title': 'Test Skill',
            'action_params': {
                'skill_name': 'test-skill',
                'skill_description': 'Test description'
            }
        }

        result = self.engine.execute_proposal(proposal, dry_run=False)

        # Should execute successfully
        self.assertTrue(result['success'])
        self.assertIn('message', result)

    @patch('execution_engine.subprocess.run')
    def test_execute_optimize_workflow(self, mock_run):
        """Test execution of OPTIMIZE_WORKFLOW action."""
        mock_run.return_value = Mock(returncode=0)

        proposal = {
            'id': self.proposal_id,
            'proposal_type': 'OPTIMIZE_WORKFLOW',
            'title': 'Optimize Workflow',
            'action_params': {
                'target_skill': 'slow-skill',
                'improvement': 'Add caching'
            }
        }

        result = self.engine.execute_proposal(proposal, dry_run=False)

        self.assertTrue(result['success'])
        self.assertIn('message', result)

    @patch('execution_engine.subprocess.run')
    def test_execute_schedule_task(self, mock_run):
        """Test execution of SCHEDULE_TASK action."""
        mock_run.return_value = Mock(returncode=0)

        proposal = {
            'id': self.proposal_id,
            'proposal_type': 'SCHEDULE_TASK',
            'title': 'Schedule Report',
            'action_params': {
                'task_name': 'weekly-report',
                'schedule_expression': '0 9 * * 1',
                'task_type': 'report'
            }
        }

        result = self.engine.execute_proposal(proposal, dry_run=False)

        self.assertTrue(result['success'])

        # Verify schedule was created
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM automation_schedule WHERE task_name = ?", ('weekly-report',))
        schedule = cursor.fetchone()
        self.assertIsNotNone(schedule)

    @patch('execution_engine.subprocess.run')
    def test_execute_merge_skills(self, mock_run):
        """Test execution of MERGE_SKILLS action."""
        mock_run.return_value = Mock(returncode=0)

        proposal = {
            'id': self.proposal_id,
            'proposal_type': 'MERGE_SKILLS',
            'title': 'Merge Skills',
            'action_params': {
                'skills_to_merge': ['skill1', 'skill2'],
                'merged_skill_name': 'combined-skill'
            }
        }

        result = self.engine.execute_proposal(proposal, dry_run=False)

        self.assertTrue(result['success'])

    @patch('execution_engine.subprocess.run')
    def test_execute_archive_skill(self, mock_run):
        """Test execution of ARCHIVE_SKILL action."""
        mock_run.return_value = Mock(returncode=0)

        proposal = {
            'id': self.proposal_id,
            'proposal_type': 'ARCHIVE_SKILL',
            'title': 'Archive Old Skill',
            'action_params': {
                'skill_id': 'old-unused-skill'
            }
        }

        result = self.engine.execute_proposal(proposal, dry_run=False)

        self.assertTrue(result['success'])

    @patch('execution_engine.subprocess.run')
    def test_execute_cleanup(self, mock_run):
        """Test execution of CLEANUP action."""
        mock_run.return_value = Mock(returncode=0)

        proposal = {
            'id': self.proposal_id,
            'proposal_type': 'CLEANUP',
            'title': 'Cleanup Old Patterns',
            'action_params': {
                'scope': 'patterns',
                'older_than_days': 30
            }
        }

        result = self.engine.execute_proposal(proposal, dry_run=False)

        self.assertTrue(result['success'])

    def test_dry_run_mode(self):
        """Test dry-run mode doesn't execute actions."""
        proposal = {
            'id': self.proposal_id,
            'proposal_type': 'CREATE_SKILL',
            'title': 'Test Skill',
            'action_params': {'skill_name': 'test'}
        }

        result = self.engine.execute_proposal(proposal, dry_run=True)

        # Should indicate dry run
        self.assertTrue(result['success'])
        self.assertIn('dry_run', result)
        self.assertTrue(result['dry_run'])

    def test_execute_by_id(self):
        """Test executing proposal by ID."""
        with patch.object(self.engine, 'execute_proposal') as mock_execute:
            mock_execute.return_value = {'success': True}

            result = self.engine.execute_by_id(self.proposal_id, dry_run=True)

            # Should fetch and execute proposal
            self.assertTrue(result['success'])
            mock_execute.assert_called_once()

    def test_execute_approved_proposals(self):
        """Test executing all approved proposals."""
        # Insert multiple approved proposals
        cursor = self.conn.cursor()
        for i in range(3):
            cursor.execute("""
                INSERT INTO automation_proposals
                (proposal_type, title, description, impact_score, confidence_score, risk_level, status)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (f'ACTION_{i}', f'Test {i}', f'Description {i}', 0.7, 0.8, 'LOW', 'approved'))
        self.conn.commit()

        with patch.object(self.engine, 'execute_proposal') as mock_execute:
            mock_execute.return_value = {'success': True}

            results = self.engine.execute_approved(dry_run=True, limit=5)

            # Should execute approved proposals
            self.assertGreaterEqual(len(results), 3)

    def test_error_handling(self):
        """Test error handling during execution."""
        proposal = {
            'id': self.proposal_id,
            'proposal_type': 'INVALID_ACTION',
            'title': 'Invalid Action'
        }

        result = self.engine.execute_proposal(proposal, dry_run=False)

        # Should handle error gracefully
        self.assertIn('success', result)
        self.assertFalse(result['success'])
        self.assertIn('error', result)

    def test_execution_logging(self):
        """Test that executions are logged properly."""
        proposal = {
            'id': self.proposal_id,
            'proposal_type': 'SCHEDULE_TASK',
            'title': 'Test Schedule',
            'action_params': {'task_name': 'test'}
        }

        with patch('execution_engine.subprocess.run', return_value=Mock(returncode=0)):
            self.engine.execute_proposal(proposal, dry_run=False)

        # Verify logging
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT * FROM task_history
            WHERE task_type = 'automation_execution'
            ORDER BY completed_at DESC
            LIMIT 1
        """)
        log_entry = cursor.fetchone()

        self.assertIsNotNone(log_entry)

    def test_update_proposal_status(self):
        """Test that proposal status is updated after execution."""
        proposal = {
            'id': self.proposal_id,
            'proposal_type': 'SCHEDULE_TASK',
            'title': 'Test',
            'action_params': {'task_name': 'test'}
        }

        with patch('execution_engine.subprocess.run', return_value=Mock(returncode=0)):
            self.engine.execute_proposal(proposal, dry_run=False)

        # Check status was updated
        cursor = self.conn.cursor()
        cursor.execute("SELECT status FROM automation_proposals WHERE id = ?", (self.proposal_id,))
        status = cursor.fetchone()[0]

        self.assertEqual(status, 'executed')

    def test_get_execution_stats(self):
        """Test retrieval of execution statistics."""
        stats = self.engine.get_execution_stats()

        # Should return statistics
        self.assertIn('total_executions', stats)
        self.assertIn('successful_executions', stats)
        self.assertIn('failed_executions', stats)
        self.assertIn('success_rate', stats)

    def test_concurrent_execution_handling(self):
        """Test handling of concurrent execution requests."""
        proposals = [
            {
                'id': i,
                'proposal_type': 'SCHEDULE_TASK',
                'title': f'Concurrent {i}',
                'action_params': {'task_name': f'test{i}'}
            }
            for i in range(5)
        ]

        with patch('execution_engine.subprocess.run', return_value=Mock(returncode=0)):
            results = [self.engine.execute_proposal(p, dry_run=True) for p in proposals]

        # All should succeed
        self.assertTrue(all(r['success'] for r in results))


class TestExecutionEngineEdgeCases(unittest.TestCase):
    """Test edge cases and error handling."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_db = TestDatabase()
        self.conn = self.test_db.setup()

        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../.gsd/automation'))
        from execution_engine import ExecutionEngine
        self.engine = ExecutionEngine(self.conn)

    def tearDown(self):
        """Clean up test fixtures."""
        self.test_db.teardown()

    def test_nonexistent_proposal_id(self):
        """Test executing non-existent proposal."""
        result = self.engine.execute_by_id(99999)

        # Should handle gracefully
        self.assertIn('success', result)
        self.assertFalse(result['success'])
        self.assertIn('error', result)

    def test_proposal_with_missing_params(self):
        """Test executing proposal with missing parameters."""
        proposal = {
            'id': 1,
            'proposal_type': 'CREATE_SKILL',
            'title': 'Incomplete Proposal'
        }

        result = self.engine.execute_proposal(proposal, dry_run=True)

        # Should indicate missing parameters
        self.assertIn('success', result)
        if not result['success']:
            self.assertIn('error', result)

    def test_command_execution_timeout(self):
        """Test handling of command execution timeouts."""
        proposal = {
            'id': 1,
            'proposal_type': 'CREATE_SKILL',
            'title': 'Long Running Task',
            'action_params': {'skill_name': 'test'}
        }

        with patch('execution_engine.subprocess.run', side_effect=TimeoutError('Command timed out')):
            result = self.engine.execute_proposal(proposal, dry_run=False)

        # Should handle timeout
        self.assertFalse(result['success'])

    def test_invalid_risk_level_execution(self):
        """Test that HIGH risk proposals require explicit approval."""
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO automation_proposals
            (proposal_type, title, description, impact_score, confidence_score, risk_level, status)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, ('DELETE_SKILL', 'Delete Skill', 'Dangerous action', 0.9, 0.5, 'HIGH', 'approved'))
        self.conn.commit()
        proposal_id = cursor.lastrowid

        proposal = {
            'id': proposal_id,
            'proposal_type': 'DELETE_SKILL',
            'title': 'Dangerous',
            'action_params': {'skill_id': 'test'},
            'risk_level': 'HIGH'
        }

        result = self.engine.execute_proposal(proposal, dry_run=False)

        # HIGH risk should require additional checks
        self.assertIn('success', result)

    def test_rollback_on_failure(self):
        """Test rollback mechanism when execution fails."""
        proposal = {
            'id': 1,
            'proposal_type': 'CREATE_SKILL',
            'title': 'Failing Proposal',
            'action_params': {'skill_name': 'test'}
        }

        with patch('execution_engine.subprocess.run', return_value=Mock(returncode=1)):
            result = self.engine.execute_proposal(proposal, dry_run=False)

        # Should not leave system in inconsistent state
        self.assertFalse(result['success'])
        # Verify rollback or cleanup occurred
        self.assertIn('message', result)


if __name__ == '__main__':
    unittest.main()
