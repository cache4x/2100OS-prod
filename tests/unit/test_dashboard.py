"""Unit tests for dashboard.py"""

import unittest
import sys
import os
from datetime import datetime, timedelta
from unittest.mock import Mock, patch
import io

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from .fixtures.test_data import TestDatabase


class TestAutomationDashboard(unittest.TestCase):
    """Test cases for AutomationDashboard class."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_db = TestDatabase()
        self.conn = self.test_db.setup()

        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../.gsd/automation'))
        from dashboard import AutomationDashboard
        self.dashboard = AutomationDashboard(self.conn)

    def tearDown(self):
        """Clean up test fixtures."""
        self.test_db.teardown()

    def test_core_metrics(self):
        """Test retrieval of core metrics."""
        metrics = self.dashboard.get_core_metrics()

        # Should return metrics dictionary
        self.assertIsInstance(metrics, dict)

        # Check for expected metric keys
        expected_keys = [
            'total_proposals',
            'pending_proposals',
            'approved_proposals',
            'executed_proposals',
            'success_rate'
        ]

        for key in expected_keys:
            self.assertIn(key, metrics)

    def test_time_series_data(self):
        """Test retrieval of time series data."""
        # Insert sample data
        cursor = self.conn.cursor()
        now = datetime.now()
        for i in range(10):
            cursor.execute("""
                INSERT INTO automation_proposals
                (proposal_type, title, description, impact_score, confidence_score, risk_level, status, proposed_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, ('TEST', f'Test {i}', f'Desc {i}', 0.7, 0.8, 'LOW', 'approved',
                  (now - timedelta(days=i)).isoformat()))
        self.conn.commit()

        time_series = self.dashboard.get_time_series(days=7)

        # Should return time series data
        self.assertIsInstance(time_series, list)

        # Check structure
        for point in time_series:
            self.assertIn('date', point)
            self.assertIn('count', point)

    def test_performance_analytics(self):
        """Test retrieval of performance analytics."""
        analytics = self.dashboard.get_performance_analytics()

        # Should return analytics
        self.assertIsInstance(analytics, dict)

        # Check for expected analytics
        expected_keys = [
            'approval_rate',
            'execution_success_rate',
            'avg_proposal_duration',
            'top_performing_types'
        ]

        for key in expected_keys:
            self.assertIn(key, analytics)

    def test_pattern_analytics(self):
        """Test retrieval of pattern analytics."""
        analytics = self.dashboard.get_pattern_analytics()

        # Should return pattern analytics
        self.assertIsInstance(analytics, dict)

        # Check for expected keys
        expected_keys = [
            'total_patterns',
            'active_patterns',
            'pattern_types',
            'recent_patterns'
        ]

        for key in expected_keys:
            self.assertIn(key, analytics)

    def test_autopilot_metrics(self):
        """Test retrieval of autopilot metrics."""
        metrics = self.dashboard.get_autopilot_metrics()

        # Should return autopilot metrics
        self.assertIsInstance(metrics, dict)

        # Check for expected keys
        expected_keys = [
            'mode',
            'health_score',
            'total_decisions',
            'auto_approval_rate',
            'success_rate'
        ]

        for key in expected_keys:
            self.assertIn(key, metrics)

    def test_schedule_overview(self):
        """Test retrieval of schedule overview."""
        # Insert sample schedules
        cursor = self.conn.cursor()
        for i in range(3):
            cursor.execute("""
                INSERT INTO automation_schedule
                (task_name, task_type, schedule_expression, enabled, next_run_at)
                VALUES (?, ?, ?, ?, ?)
            """, (f'task_{i}', 'test', f'{i} * * * *', 1,
                  (datetime.now() + timedelta(hours=i)).isoformat()))
        self.conn.commit()

        overview = self.dashboard.get_schedule_overview()

        # Should return overview
        self.assertIsInstance(overview, dict)

        # Check for expected keys
        expected_keys = [
            'total_schedules',
            'active_schedules',
            'upcoming_runs',
            'recent_executions'
        ]

        for key in expected_keys:
            self.assertIn(key, overview)

    def test_pending_breakdown(self):
        """Test breakdown of pending proposals."""
        # Insert sample proposals
        cursor = self.conn.cursor()
        for i in range(5):
            cursor.execute("""
                INSERT INTO automation_proposals
                (proposal_type, title, description, impact_score, confidence_score, risk_level, status)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, ('TEST', f'Test {i}', f'Desc {i}', 0.7, 0.8, 'LOW', 'pending'))
        self.conn.commit()

        breakdown = self.dashboard.get_pending_breakdown()

        # Should return breakdown
        self.assertIsInstance(breakdown, dict)

        # Check for expected breakdowns
        expected_keys = [
            'by_type',
            'by_risk_level',
            'by_confidence',
            'high_priority'
        ]

        for key in expected_keys:
            self.assertIn(key, breakdown)

    def test_dashboard_render(self):
        """Test dashboard rendering."""
        # Capture output
        captured_output = io.StringIO()

        with patch('sys.stdout', captured_output):
            self.dashboard.render_dashboard()

        # Should produce output
        output = captured_output.getvalue()
        self.assertGreater(len(output), 0)

        # Should contain expected sections
        expected_sections = [
            'CORE METRICS',
            'PENDING PROPOSALS',
            'PERFORMANCE'
        ]

        for section in expected_sections:
            self.assertIn(section, output)

    def test_trend_calculation(self):
        """Test calculation of trends."""
        # Create sample time series data
        data = [
            {'date': '2024-01-01', 'value': 10},
            {'date': '2024-01-02', 'value': 15},
            {'date': '2024-01-03', 'value': 12}
        ]

        trend = self.dashboard.calculate_trend(data)

        # Should return trend info
        self.assertIn('direction', trend)
        self.assertIn('change_percent', trend)

        # Direction should be valid
        self.assertIn(trend['direction'], ['up', 'down', 'stable'])

    def test_health_score_calculation(self):
        """Test calculation of health scores."""
        metrics = {
            'success_rate': 0.9,
            'approval_rate': 0.8,
            'execution_rate': 0.85
        }

        health = self.dashboard.calculate_health_score(metrics)

        # Should be between 0 and 1
        self.assertGreaterEqual(health, 0.0)
        self.assertLessEqual(health, 1.0)

        # Good metrics should give good health
        self.assertGreater(health, 0.7)

    def test_filtering_by_date_range(self):
        """Test filtering data by date range."""
        # Insert sample data across different dates
        cursor = self.conn.cursor()
        now = datetime.now()
        for i in range(10):
            cursor.execute("""
                INSERT INTO automation_proposals
                (proposal_type, title, description, impact_score, confidence_score, risk_level, status, proposed_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, ('TEST', f'Test {i}', f'Desc {i}', 0.7, 0.8, 'LOW', 'approved',
                  (now - timedelta(days=i)).isoformat()))
        self.conn.commit()

        # Get last 3 days
        recent = self.dashboard.get_proposals_in_range(days=3)

        # Should filter correctly
        self.assertLessEqual(len(recent), 4)  # 0, 1, 2, 3 days ago

    def test_export_metrics(self):
        """Test exporting metrics to various formats."""
        # Test JSON export
        json_export = self.dashboard.export_metrics(format='json')
        self.assertIsInstance(json_export, str)

        # Test dict export
        dict_export = self.dashboard.export_metrics(format='dict')
        self.assertIsInstance(dict_export, dict)


class TestDashboardEdgeCases(unittest.TestCase):
    """Test edge cases and error handling."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_db = TestDatabase()
        self.conn = self.test_db.setup()

        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../.gsd/automation'))
        from dashboard import AutomationDashboard
        self.dashboard = AutomationDashboard(self.conn)

    def tearDown(self):
        """Clean up test fixtures."""
        self.test_db.teardown()

    def test_empty_database(self):
        """Test dashboard with empty database."""
        metrics = self.dashboard.get_core_metrics()

        # Should return zeros, not crash
        self.assertEqual(metrics['total_proposals'], 0)
        self.assertEqual(metrics['pending_proposals'], 0)

    def test_invalid_date_range(self):
        """Test handling of invalid date ranges."""
        # Negative days
        result = self.dashboard.get_proposals_in_range(days=-1)
        self.assertIsInstance(result, list)

        # Very large days
        result = self.dashboard.get_proposals_in_range(days=10000)
        self.assertIsInstance(result, list)

    def test_export_invalid_format(self):
        """Test export with invalid format."""
        # Should handle gracefully
        try:
            result = self.dashboard.export_metrics(format='invalid')
            # If successful, should return dict as default
            self.assertIsInstance(result, (dict, str))
        except ValueError:
            # Expected for invalid format
            pass

    def test_missing_metrics(self):
        """Trend calculation with missing data."""
        empty_data = []
        trend = self.dashboard.calculate_trend(empty_data)

        # Should handle gracefully
        self.assertIn('direction', trend)
        self.assertEqual(trend['direction'], 'stable')

    def test_dashboard_refresh(self):
        """Test dashboard refresh functionality."""
        # Get initial metrics
        initial = self.dashboard.get_core_metrics()

        # Insert new data
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO automation_proposals
            (proposal_type, title, description, impact_score, confidence_score, risk_level, status)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, ('TEST', 'New', 'Desc', 0.7, 0.8, 'LOW', 'pending'))
        self.conn.commit()

        # Refresh and get new metrics
        refreshed = self.dashboard.get_core_metrics()

        # Should reflect changes
        self.assertEqual(refreshed['total_proposals'], initial['total_proposals'] + 1)

    def test_concurrent_dashboard_access(self):
        """Test handling of concurrent dashboard access."""
        # Simulate concurrent access
        import threading

        results = []

        def get_metrics():
            results.append(self.dashboard.get_core_metrics())

        threads = [threading.Thread(target=get_metrics) for _ in range(5)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        # All should complete successfully
        self.assertEqual(len(results), 5)
        self.assertTrue(all(isinstance(r, dict) for r in results))

    def test_very_large_dataset(self):
        """Test dashboard with large dataset."""
        # Insert many records
        cursor = self.conn.cursor()
        for i in range(1000):
            cursor.execute("""
                INSERT INTO automation_proposals
                (proposal_type, title, description, impact_score, confidence_score, risk_level, status)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, ('TEST', f'Test {i}', f'Desc {i}', 0.7, 0.8, 'LOW', 'approved'))
        self.conn.commit()

        # Should still function
        metrics = self.dashboard.get_core_metrics()
        self.assertEqual(metrics['total_proposals'], 1000)

    def test_unicode_handling(self):
        """Test handling of unicode characters."""
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO automation_proposals
            (proposal_type, title, description, impact_score, confidence_score, risk_level, status)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, ('TEST', 'Tëst Ñamé', 'Descriçión with émojis 🚀', 0.7, 0.8, 'LOW', 'pending'))
        self.conn.commit()

        # Should handle unicode
        proposals = self.dashboard.get_pending_breakdown()
        self.assertIsNotNone(proposals)


if __name__ == '__main__':
    unittest.main()
