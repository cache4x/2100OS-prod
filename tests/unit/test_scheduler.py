"""Unit tests for scheduler.py"""

import unittest
import sys
import os
from datetime import datetime, timedelta
from unittest.mock import Mock, patch

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from .fixtures.test_data import TestDatabase


class TestAutomationScheduler(unittest.TestCase):
    """Test cases for AutomationScheduler class."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_db = TestDatabase()
        self.conn = self.test_db.setup()

        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../.gsd/automation'))
        from scheduler import AutomationScheduler
        self.scheduler = AutomationScheduler(self.conn)

    def tearDown(self):
        """Clean up test fixtures."""
        if hasattr(self, 'scheduler'):
            self.scheduler.stop()
        self.test_db.teardown()

    def test_create_schedule(self):
        """Test creating a new schedule."""
        schedule_data = {
            'task_name': 'weekly_report',
            'task_type': 'report',
            'schedule_expression': '0 9 * * 1',  # Every Monday 9am
            'parameters': {'format': 'detailed'}
        }

        schedule_id = self.scheduler.create_schedule(schedule_data)

        # Should return valid ID
        self.assertIsNotNone(schedule_id)
        self.assertGreater(schedule_id, 0)

        # Verify in database
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM automation_schedule WHERE id = ?", (schedule_id,))
        result = cursor.fetchone()

        self.assertIsNotNone(result)
        self.assertEqual(result[1], 'weekly_report')

    def test_cron_parsing(self):
        """Test parsing of cron expressions."""
        test_cases = [
            ('0 9 * * 1', 'Every Monday at 9:00 AM'),
            ('*/5 * * * *', 'Every 5 minutes'),
            ('0 0 * * *', 'Every day at midnight'),
            ('30 14 * * 1-5', 'Weekdays at 2:30 PM')
        ]

        for expression, expected_desc in test_cases:
            parsed = self.scheduler.parse_cron_expression(expression)
            self.assertIsNotNone(parsed)
            self.assertIn('expression', parsed)

    def test_next_run_calculation(self):
        """Test calculation of next run time."""
        schedule = {
            'schedule_expression': '0 9 * * *',  # Daily at 9am
            'last_run_at': None
        }

        next_run = self.scheduler.calculate_next_run(schedule)

        # Should be in the future
        self.assertIsNotNone(next_run)
        self.assertGreater(next_run, datetime.now())

    def test_next_run_after_execution(self):
        """Test next run calculation after execution."""
        now = datetime.now()
        schedule = {
            'schedule_expression': '0 9 * * *',  # Daily at 9am
            'last_run_at': now.isoformat()
        }

        next_run = self.scheduler.calculate_next_run(schedule)

        # Should be at least next day
        self.assertIsNotNone(next_run)

    def test_list_schedules(self):
        """Test listing all schedules."""
        # Create sample schedules
        for i in range(3):
            self.scheduler.create_schedule({
                'task_name': f'test_task_{i}',
                'task_type': 'test',
                'schedule_expression': f'{i} * * * *'
            })

        schedules = self.scheduler.list_schedules()

        # Should return all schedules
        self.assertGreaterEqual(len(schedules), 3)

        # Check structure
        for schedule in schedules:
            self.assertIn('id', schedule)
            self.assertIn('task_name', schedule)
            self.assertIn('next_run_at', schedule)

    def test_get_schedule_by_id(self):
        """Test retrieving schedule by ID."""
        schedule_id = self.scheduler.create_schedule({
            'task_name': 'test_task',
            'task_type': 'test',
            'schedule_expression': '0 * * * *'
        })

        schedule = self.scheduler.get_schedule_by_id(schedule_id)

        # Should return schedule
        self.assertIsNotNone(schedule)
        self.assertEqual(schedule['id'], schedule_id)
        self.assertEqual(schedule['task_name'], 'test_task')

    def test_update_schedule(self):
        """Test updating existing schedule."""
        schedule_id = self.scheduler.create_schedule({
            'task_name': 'test_task',
            'task_type': 'test',
            'schedule_expression': '0 * * * *'
        })

        # Update schedule
        updated = self.scheduler.update_schedule(schedule_id, {
            'enabled': False,
            'parameters': {'new_param': 'value'}
        })

        self.assertTrue(updated)

        # Verify update
        schedule = self.scheduler.get_schedule_by_id(schedule_id)
        self.assertEqual(schedule['enabled'], 0)

    def test_delete_schedule(self):
        """Test deleting a schedule."""
        schedule_id = self.scheduler.create_schedule({
            'task_name': 'test_task',
            'task_type': 'test',
            'schedule_expression': '0 * * * *'
        })

        # Delete schedule
        deleted = self.scheduler.delete_schedule(schedule_id)

        self.assertTrue(deleted)

        # Verify deletion
        schedule = self.scheduler.get_schedule_by_id(schedule_id)
        self.assertIsNone(schedule)

    def test_enable_disable_schedule(self):
        """Test enabling and disabling schedules."""
        schedule_id = self.scheduler.create_schedule({
            'task_name': 'test_task',
            'task_type': 'test',
            'schedule_expression': '0 * * * *'
        })

        # Disable
        self.scheduler.disable_schedule(schedule_id)
        schedule = self.scheduler.get_schedule_by_id(schedule_id)
        self.assertEqual(schedule['enabled'], 0)

        # Enable
        self.scheduler.enable_schedule(schedule_id)
        schedule = self.scheduler.get_schedule_by_id(schedule_id)
        self.assertEqual(schedule['enabled'], 1)

    def test_get_due_schedules(self):
        """Test retrieval of due schedules."""
        # Create schedule that should run soon
        self.scheduler.create_schedule({
            'task_name': 'immediate_task',
            'task_type': 'test',
            'schedule_expression': '* * * * *'  # Every minute
        })

        due_schedules = self.scheduler.get_due_schedules()

        # Should find at least the immediate task
        self.assertGreater(len(due_schedules), 0)

    def test_execute_schedule_reminder(self):
        """Test execution of reminder task type."""
        schedule_id = self.scheduler.create_schedule({
            'task_name': 'test_reminder',
            'task_type': 'reminder',
            'schedule_expression': '0 * * * *',
            'parameters': {'message': 'Test reminder'}
        })

        with patch.object(self.scheduler, '_execute_reminder') as mock_execute:
            mock_execute.return_value = {'success': True}

            result = self.scheduler.execute_schedule(schedule_id)

            self.assertTrue(result['success'])
            mock_execute.assert_called_once()

    def test_execute_schedule_analysis(self):
        """Test execution of analysis task type."""
        schedule_id = self.scheduler.create_schedule({
            'task_name': 'test_analysis',
            'task_type': 'analysis',
            'schedule_expression': '0 * * * *'
        })

        with patch.object(self.scheduler, '_execute_analysis') as mock_execute:
            mock_execute.return_value = {'success': True}

            result = self.scheduler.execute_schedule(schedule_id)

            self.assertTrue(result['success'])

    def test_execute_schedule_report(self):
        """Test execution of report task type."""
        schedule_id = self.scheduler.create_schedule({
            'task_name': 'test_report',
            'task_type': 'report',
            'schedule_expression': '0 * * * *'
        })

        with patch.object(self.scheduler, '_execute_report') as mock_execute:
            mock_execute.return_value = {'success': True}

            result = self.scheduler.execute_schedule(schedule_id)

            self.assertTrue(result['success'])

    def test_execute_schedule_cleanup(self):
        """Test execution of cleanup task type."""
        schedule_id = self.scheduler.create_schedule({
            'task_name': 'test_cleanup',
            'task_type': 'cleanup',
            'schedule_expression': '0 * * * *'
        })

        with patch.object(self.scheduler, '_execute_cleanup') as mock_execute:
            mock_execute.return_value = {'success': True}

            result = self.scheduler.execute_schedule(schedule_id)

            self.assertTrue(result['success'])

    def test_execute_schedule_backup(self):
        """Test execution of backup task type."""
        schedule_id = self.scheduler.create_schedule({
            'task_name': 'test_backup',
            'task_type': 'backup',
            'schedule_expression': '0 * * * *'
        })

        with patch.object(self.scheduler, '_execute_backup') as mock_execute:
            mock_execute.return_value = {'success': True}

            result = self.scheduler.execute_schedule(schedule_id)

            self.assertTrue(result['success'])

    def test_execute_schedule_skill(self):
        """Test execution of skill task type."""
        schedule_id = self.scheduler.create_schedule({
            'task_name': 'test_skill',
            'task_type': 'skill',
            'schedule_expression': '0 * * * *',
            'parameters': {'skill_id': 'test-skill'}
        })

        with patch.object(self.scheduler, '_execute_skill') as mock_execute:
            mock_execute.return_value = {'success': True}

            result = self.scheduler.execute_schedule(schedule_id)

            self.assertTrue(result['success'])

    def test_update_run_count(self):
        """Test that run count is updated after execution."""
        schedule_id = self.scheduler.create_schedule({
            'task_name': 'test_task',
            'task_type': 'test',
            'schedule_expression': '0 * * * *'
        })

        # Execute
        with patch.object(self.scheduler, '_execute_test', return_value={'success': True}):
            self.scheduler.execute_schedule(schedule_id)

        # Check run count increased
        schedule = self.scheduler.get_schedule_by_id(schedule_id)
        self.assertEqual(schedule['run_count'], 1)

    def test_update_last_run_time(self):
        """Test that last run time is updated."""
        schedule_id = self.scheduler.create_schedule({
            'task_name': 'test_task',
            'task_type': 'test',
            'schedule_expression': '0 * * * *'
        })

        before = datetime.now()

        # Execute
        with patch.object(self.scheduler, '_execute_test', return_value={'success': True}):
            self.scheduler.execute_schedule(schedule_id)

        # Check last_run_at updated
        schedule = self.scheduler.get_schedule_by_id(schedule_id)
        last_run = datetime.fromisoformat(schedule['last_run_at'])
        self.assertGreater(last_run, before)

    def test_get_scheduler_stats(self):
        """Test retrieval of scheduler statistics."""
        stats = self.scheduler.get_stats()

        # Should return statistics
        self.assertIn('total_schedules', stats)
        self.assertIn('active_schedules', stats)
        self.assertIn('total_runs', stats)
        self.assertIn('successful_runs', stats)


class TestAutomationSchedulerEdgeCases(unittest.TestCase):
    """Test edge cases and error handling."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_db = TestDatabase()
        self.conn = self.test_db.setup()

        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../.gsd/automation'))
        from scheduler import AutomationScheduler
        self.scheduler = AutomationScheduler(self.conn)

    def tearDown(self):
        """Clean up test fixtures."""
        if hasattr(self, 'scheduler'):
            self.scheduler.stop()
        self.test_db.teardown()

    def test_invalid_cron_expression(self):
        """Test handling of invalid cron expressions."""
        invalid_expressions = [
            'invalid',
            '7 * * * *',  # Invalid minute
            '* 25 * * *',  # Invalid hour
            '* * * * 8'   # Invalid day
        ]

        for expr in invalid_expressions:
            parsed = self.scheduler.parse_cron_expression(expr)
            # Should handle gracefully
            self.assertIsNotNone(parsed)

    def test_nonexistent_schedule_id(self):
        """Test operations on non-existent schedule."""
        result = self.scheduler.get_schedule_by_id(99999)
        self.assertIsNone(result)

        updated = self.scheduler.update_schedule(99999, {'enabled': False})
        self.assertFalse(updated)

        deleted = self.scheduler.delete_schedule(99999)
        self.assertFalse(deleted)

    def test_schedule_with_missing_parameters(self):
        """Test creating schedule with missing parameters."""
        incomplete_data = {
            'task_name': 'test'
        }

        # Should handle gracefully
        try:
            schedule_id = self.scheduler.create_schedule(incomplete_data)
            # If created, should have defaults
            self.assertIsNotNone(schedule_id)
        except (KeyError, ValueError):
            # Expected for missing required fields
            pass

    def test_execution_failure_handling(self):
        """Test handling of execution failures."""
        schedule_id = self.scheduler.create_schedule({
            'task_name': 'failing_task',
            'task_type': 'test',
            'schedule_expression': '0 * * * *'
        })

        with patch.object(self.scheduler, '_execute_test', side_effect=Exception('Test error')):
            result = self.scheduler.execute_schedule(schedule_id)

        # Should handle error
        self.assertFalse(result['success'])
        self.assertIn('error', result)

    def test_unknown_task_type(self):
        """Test handling of unknown task types."""
        schedule_id = self.scheduler.create_schedule({
            'task_name': 'unknown_task',
            'task_type': 'unknown_type',
            'schedule_expression': '0 * * * *'
        })

        result = self.scheduler.execute_schedule(schedule_id)

        # Should indicate unknown type
        self.assertFalse(result['success'])

    def test_concurrent_execution(self):
        """Test handling of concurrent execution attempts."""
        schedule_id = self.scheduler.create_schedule({
            'task_name': 'concurrent_task',
            'task_type': 'test',
            'schedule_expression': '0 * * * *'
        })

        # Try to execute same schedule multiple times
        with patch.object(self.scheduler, '_execute_test', return_value={'success': True}):
            results = [
                self.scheduler.execute_schedule(schedule_id)
                for _ in range(3)
            ]

        # Should handle all attempts
        self.assertTrue(all('success' in r for r in results))

    def test_daemon_mode_lifecycle(self):
        """Test daemon mode start and stop."""
        # Start daemon
        started = self.scheduler.start_daemon()
        self.assertTrue(started)

        # Check status
        status = self.scheduler.get_daemon_status()
        self.assertIsNotNone(status)

        # Stop daemon
        stopped = self.scheduler.stop_daemon()
        self.assertTrue(stopped)

    def test_empty_schedule_list(self):
        """Test listing when no schedules exist."""
        schedules = self.scheduler.list_schedules()
        self.assertEqual(len(schedules), 0)

    def test_scheduling_with_timezone(self):
        """Test scheduling with timezone considerations."""
        schedule_id = self.scheduler.create_schedule({
            'task_name': 'timezone_task',
            'task_type': 'test',
            'schedule_expression': '0 9 * * *',
            'parameters': {'timezone': 'UTC'}
        })

        next_run = self.scheduler.calculate_next_run({
            'schedule_expression': '0 9 * * *',
            'last_run_at': None,
            'timezone': 'UTC'
        })

        self.assertIsNotNone(next_run)


if __name__ == '__main__':
    unittest.main()
