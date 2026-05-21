"""Unit tests for ml_pattern_detector.py"""

import unittest
import sys
import os
from datetime import datetime, timedelta

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from .fixtures.test_data import TestDatabase, SAMPLE_ML_FEATURES


class TestMLPatternDetector(unittest.TestCase):
    """Test cases for MLPatternDetector class."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_db = TestDatabase()
        self.conn = self.test_db.setup()

        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../.gsd/automation'))
        from ml_pattern_detector import MLPatternDetector
        self.detector = MLPatternDetector(self.conn)

    def tearDown(self):
        """Clean up test fixtures."""
        self.test_db.teardown()

    def test_feature_extraction(self):
        """Test extraction of numerical features from tasks."""
        features = self.detector.extract_features(skill_id='mmc-carrossel')

        # Should return feature dictionary
        self.assertIsInstance(features, dict)

        # Check for expected feature keys
        expected_keys = [
            'duration_normalized',
            'frequency_normalized',
            'success_rate',
            'time_since_last_use',
            'peak_usage_hour'
        ]

        for key in expected_keys:
            self.assertIn(key, features)

        # Features should be normalized (0-1) or reasonable values
        for key, value in features.items():
            if 'normalized' in key:
                self.assertGreaterEqual(value, 0.0)
                self.assertLessEqual(value, 1.0)

    def test_kmeans_clustering(self):
        """Test K-Means clustering of patterns."""
        # Create sample feature vectors
        features = [
            {'duration': 0.5, 'frequency': 0.8, 'success': 0.9},
            {'duration': 0.6, 'frequency': 0.7, 'success': 0.85},
            {'duration': 0.2, 'frequency': 0.3, 'success': 0.6},
            {'duration': 0.3, 'frequency': 0.4, 'success': 0.65},
        ]

        clusters = self.detector.cluster_patterns(features, n_clusters=2)

        # Should assign clusters to all patterns
        self.assertEqual(len(clusters), len(features))

        # Each cluster should be valid
        for cluster in clusters:
            self.assertIn('cluster_id', cluster)
            self.assertIn('pattern_id', cluster)

    def test_anomaly_detection(self):
        """Test detection of anomalous patterns."""
        # Create normal patterns
        normal_patterns = [
            {'duration': 100, 'frequency': 10},
            {'duration': 120, 'frequency': 12},
            {'duration': 110, 'frequency': 11},
        ]

        # Create anomalous pattern
        anomalous_pattern = {'duration': 500, 'frequency': 2}

        all_patterns = normal_patterns + [anomalous_pattern]

        anomalies = self.detector.detect_anomalies(all_patterns)

        # Should detect at least one anomaly
        self.assertGreater(len(anomalies), 0)

        # Anomaly should have high z-score
        for anomaly in anomalies:
            self.assertIn('z_score', anomaly)
            self.assertGreater(abs(anomaly['z_score']), 2.0)

    def test_predictive_analytics(self):
        """Test prediction of future needs."""
        predictions = self.detector.predict_future_needs(horizon_days=7)

        # Should return predictions
        self.assertIsInstance(predictions, dict)

        # Check for prediction types
        expected_keys = [
            'likely_tasks',
            'resource_demands',
            'peak_times'
        ]

        for key in expected_keys:
            self.assertIn(key, predictions)

    def test_seasonal_detection(self):
        """Test detection of seasonal patterns."""
        seasonal_patterns = self.detector.detect_seasonal_patterns()

        # Should return seasonal information
        self.assertIsInstance(seasonal_patterns, list)

        # Check pattern structure
        for pattern in seasonal_patterns:
            self.assertIn('pattern_type', pattern)
            self.assertIn('season', pattern)
            self.assertIn('confidence', pattern)

    def test_complex_sequence_detection(self):
        """Test detection of complex task sequences."""
        sequences = self.detector.detect_complex_sequences(min_length=3)

        # Should find complex sequences
        self.assertIsInstance(sequences, list)

        # Check sequence structure
        for sequence in sequences:
            self.assertIn('tasks', sequence)
            self.assertIn('frequency', sequence)
            self.assertGreater(len(sequence['tasks']), 2)

    def test_optimization_opportunities(self):
        """Test identification of optimization opportunities."""
        opportunities = self.detector.find_optimization_opportunities()

        # Should find opportunities
        self.assertIsInstance(opportunities, list)

        # Check opportunity structure
        for opp in opportunities:
            self.assertIn('type', opp)
            self.assertIn('potential_saving', opp)
            self.assertIn('confidence', opp)

    def test_feature_normalization(self):
        """Test normalization of feature vectors."""
        raw_features = {
            'duration': [100, 200, 150, 180],
            'frequency': [5, 10, 7, 8]
        }

        normalized = self.detector.normalize_features(raw_features)

        # Should normalize values to 0-1 range
        for key, values in normalized.items():
            for value in values:
                self.assertGreaterEqual(value, 0.0)
                self.assertLessEqual(value, 1.0)

    def test_confidence_score_calculation(self):
        """Test calculation of confidence scores."""
        pattern = {
            'frequency': 10,
            'consistency': 0.9,
            'data_quality': 0.8
        }

        confidence = self.detector.calculate_confidence(pattern)

        # Should be between 0 and 1
        self.assertGreaterEqual(confidence, 0.0)
        self.assertLessEqual(confidence, 1.0)

        # High quality pattern should have high confidence
        self.assertGreater(confidence, 0.7)

    def test_save_ml_patterns(self):
        """Test saving ML-detected patterns."""
        patterns = [
            {
                'pattern_type': 'ml_cluster',
                'cluster_id': 1,
                'confidence': 0.85
            }
        ]

        saved_ids = self.detector.save_patterns(patterns)

        # Should save patterns
        self.assertGreater(len(saved_ids), 0)

    def test_get_pattern_insights(self):
        """Test retrieval of insights for patterns."""
        # Create a pattern
        patterns = [{
            'pattern_type': 'test',
            'features': {'duration': 100, 'frequency': 5}
        }]
        saved_ids = self.detector.save_patterns(patterns)

        # Get insights
        insights = self.detector.get_pattern_insights(saved_ids[0])

        # Should return insights
        self.assertIsNotNone(insights)
        self.assertIn('pattern', insights)
        self.assertIn('analysis', insights)


class TestMLDetectorEdgeCases(unittest.TestCase):
    """Test edge cases and error handling."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_db = TestDatabase()
        self.conn = self.test_db.setup()

        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../.gsd/automation'))
        from ml_pattern_detector import MLPatternDetector
        self.detector = MLPatternDetector(self.conn)

    def tearDown(self):
        """Clean up test fixtures."""
        self.test_db.teardown()

    def test_empty_feature_set(self):
        """Test handling of empty feature sets."""
        features = []
        clusters = self.detector.cluster_patterns(features, n_clusters=2)

        # Should handle gracefully
        self.assertEqual(len(clusters), 0)

    def test_single_cluster(self):
        """Test clustering with single cluster."""
        features = [
            {'duration': 0.5, 'frequency': 0.8},
            {'duration': 0.6, 'frequency': 0.7}
        ]

        clusters = self.detector.cluster_patterns(features, n_clusters=1)

        # All should be in same cluster
        self.assertTrue(all(c['cluster_id'] == 0 for c in clusters))

    def test_insufficient_data_for_clustering(self):
        """Test clustering with insufficient data."""
        features = [
            {'duration': 0.5, 'frequency': 0.8}
        ]

        # Should handle gracefully
        try:
            clusters = self.detector.cluster_patterns(features, n_clusters=2)
            # If successful, all in same cluster
            self.assertEqual(len(clusters), 1)
        except ValueError:
            # Expected for insufficient data
            pass

    def test_extreme_feature_values(self):
        """Test handling of extreme feature values."""
        extreme_features = {
            'duration': [0, 999999],
            'frequency': [0.001, 1000]
        }

        normalized = self.detector.normalize_features(extreme_features)

        # Should normalize without errors
        for values in normalized.values():
            self.assertTrue(all(0 <= v <= 1 for v in values))

    def test_missing_features(self):
        """Test handling of missing feature values."""
        incomplete_features = {
            'duration': 100,
            'frequency': None  # Missing
        }

        # Should handle gracefully
        try:
            normalized = self.detector.normalize_features(incomplete_features)
            self.assertIsNotNone(normalized)
        except (KeyError, TypeError):
            # Expected for missing values
            pass

    def test_invalid_cluster_count(self):
        """Test handling of invalid cluster count."""
        features = [{'duration': 0.5, 'frequency': 0.8}]

        # Invalid cluster counts
        invalid_counts = [-1, 0, 1000]

        for count in invalid_counts:
            try:
                clusters = self.detector.cluster_patterns(features, n_clusters=count)
                # If successful, should use safe default
                self.assertGreater(len(clusters), 0)
            except ValueError:
                # Expected for invalid count
                pass


if __name__ == '__main__':
    unittest.main()
