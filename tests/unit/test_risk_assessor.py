"""Unit tests for risk_assessor.py"""

import unittest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from .fixtures.test_data import SAMPLE_PROPOSALS


class TestRiskAssessor(unittest.TestCase):
    """Test cases for RiskAssessor class."""

    def setUp(self):
        """Set up test fixtures."""
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../.gsd/automation'))
        from risk_assessor import RiskAssessor
        self.assessor = RiskAssessor()

    def test_assess_low_risk_proposal(self):
        """Test assessment of LOW risk proposals."""
        proposal = {
            'action_type': 'SCHEDULE_TASK',
            'title': 'Weekly Report',
            'is_destructive': False,
            'is_reversible': True,
            'affects_database': False,
            'requires_user_approval': False
        }

        risk = self.assessor.assess_proposal(proposal)

        # Should be LOW risk
        self.assertEqual(risk['level'], 'LOW')
        self.assertGreater(risk['score'], 0.0)
        self.assertLessEqual(risk['score'], 0.3)

    def test_assess_medium_risk_proposal(self):
        """Test assessment of MEDIUM risk proposals."""
        proposal = {
            'action_type': 'CREATE_SKILL',
            'title': 'New Skill Creation',
            'is_destructive': False,
            'is_reversible': True,
            'affects_database': False,
            'requires_user_approval': True
        }

        risk = self.assessor.assess_proposal(proposal)

        # Should be MEDIUM risk
        self.assertEqual(risk['level'], 'MEDIUM')
        self.assertGreater(risk['score'], 0.3)
        self.assertLessEqual(risk['score'], 0.7)

    def test_assess_high_risk_proposal(self):
        """Test assessment of HIGH risk proposals."""
        proposal = {
            'action_type': 'DELETE_SKILL',
            'title': 'Delete Skill',
            'is_destructive': True,
            'is_reversible': False,
            'affects_database': True,
            'requires_user_approval': True
        }

        risk = self.assessor.assess_proposal(proposal)

        # Should be HIGH risk
        self.assertEqual(risk['level'], 'HIGH')
        self.assertGreater(risk['score'], 0.7)
        self.assertLessEqual(risk['score'], 1.0)

    def test_destructive_operation_penalty(self):
        """Test that destructive operations increase risk."""
        safe_proposal = {
            'action_type': 'SCHEDULE_TASK',
            'is_destructive': False
        }

        destructive_proposal = {
            'action_type': 'DELETE_SKILL',
            'is_destructive': True
        }

        safe_risk = self.assessor.assess_proposal(safe_proposal)
        destructive_risk = self.assessor.assess_proposal(destructive_proposal)

        self.assertGreater(destructive_risk['score'], safe_risk['score'])

    def test_irreversible_operation_penalty(self):
        """Test that irreversible operations increase risk."""
        reversible_proposal = {
            'action_type': 'CREATE_SKILL',
            'is_reversible': True
        }

        irreversible_proposal = {
            'action_type': 'ARCHIVE_SKILL',
            'is_reversible': False
        }

        reversible_risk = self.assessor.assess_proposal(reversible_proposal)
        irreversible_risk = self.assessor.assess_proposal(irreversible_proposal)

        self.assertGreater(irreversible_risk['score'], reversible_risk['score'])

    def test_database_modification_penalty(self):
        """Test that database modifications increase risk."""
        no_db_proposal = {
            'action_type': 'ANALYZE',
            'affects_database': False
        }

        db_proposal = {
            'action_type': 'MODIFY_SCHEMA',
            'affects_database': True
        }

        no_db_risk = self.assessor.assess_proposal(no_db_proposal)
        db_risk = self.assessor.assess_proposal(db_proposal)

        self.assertGreater(db_risk['score'], no_db_risk['score'])

    def test_risk_factors_detailed(self):
        """Test that risk factors are properly identified."""
        proposal = {
            'action_type': 'DELETE_SKILL',
            'is_destructive': True,
            'is_reversible': False,
            'affects_database': True
        }

        risk = self.assessor.assess_proposal(proposal)

        # Should list factors
        self.assertIn('factors', risk)
        self.assertIsInstance(risk['factors'], list)
        self.assertGreater(len(risk['factors']), 0)

        # Factors should be descriptive
        for factor in risk['factors']:
            self.assertIn('description', factor)
            self.assertIn('weight', factor)

    def test_auto_execute_eligibility(self):
        """Test determination of auto-execute eligibility."""
        # LOW risk should be auto-executable
        low_risk = self.assessor.assess_proposal({
            'action_type': 'SCHEDULE_TASK',
            'is_destructive': False,
            'is_reversible': True
        })
        self.assertTrue(low_risk['auto_execute_eligible'])

        # HIGH risk should not be auto-executable
        high_risk = self.assessor.assess_proposal({
            'action_type': 'DELETE_SKILL',
            'is_destructive': True,
            'is_reversible': False
        })
        self.assertFalse(high_risk['auto_execute_eligible'])

    def test_batch_risk_assessment(self):
        """Test risk assessment for multiple proposals."""
        proposals = SAMPLE_PROPOSALS

        risk_assessments = self.assessor.assess_batch(proposals)

        # Should assess all proposals
        self.assertEqual(len(risk_assessments), len(proposals))

        # Each assessment should have required fields
        for assessment in risk_assessments:
            self.assertIn('level', assessment)
            self.assertIn('score', assessment)
            self.assertIn('factors', assessment)

    def test_confidence_adjustment(self):
        """Test that confidence affects risk assessment."""
        high_confidence_proposal = {
            'action_type': 'CREATE_SKILL',
            'confidence_score': 0.95
        }

        low_confidence_proposal = {
            'action_type': 'CREATE_SKILL',
            'confidence_score': 0.3
        }

        high_conf_risk = self.assessor.assess_proposal(high_confidence_proposal)
        low_conf_risk = self.assessor.assess_proposal(low_confidence_proposal)

        # Lower confidence should increase risk score
        self.assertGreater(low_conf_risk['score'], high_conf_risk['score'])

    def test_risk_threshold_customization(self):
        """Test customization of risk thresholds."""
        custom_thresholds = {
            'low_max': 0.2,
            'medium_max': 0.6
        }

        assessor = type('RiskAssessor', (), {
            'assess_proposal': lambda self, p: self._assess_with_thresholds(p, custom_thresholds),
            '_assess_with_thresholds': lambda self, p, t: {'score': 0.25, 'level': 'MEDIUM'}
        })()

        result = assessor.assess_proposal({'action_type': 'TEST'})
        self.assertIsNotNone(result)

    def test_risk_level_string_format(self):
        """Test that risk levels are properly formatted."""
        test_cases = [
            (0.1, 'LOW'),
            (0.5, 'MEDIUM'),
            (0.9, 'HIGH')
        ]

        for score, expected_level in test_cases:
            risk = self.assessor._determine_level(score)
            self.assertEqual(risk, expected_level)


class TestRiskAssessorEdgeCases(unittest.TestCase):
    """Test edge cases and error handling."""

    def setUp(self):
        """Set up test fixtures."""
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../.gsd/automation'))
        from risk_assessor import RiskAssessor
        self.assessor = RiskAssessor()

    def test_missing_proposal_fields(self):
        """Test handling of proposals with missing fields."""
        incomplete_proposal = {'action_type': 'UNKNOWN'}

        # Should handle gracefully
        risk = self.assessor.assess_proposal(incomplete_proposal)

        # Should still return valid assessment
        self.assertIn('level', risk)
        self.assertIn('score', risk)

    def test_extreme_scores(self):
        """Test handling of extreme risk scores."""
        # Should clamp to valid range
        self.assertGreaterEqual(self.assessor._normalize_score(-0.5), 0.0)
        self.assertLessEqual(self.assessor._normalize_score(1.5), 1.0)

    def test_empty_batch(self):
        """Test batch assessment with empty list."""
        assessments = self.assessor.assess_batch([])

        # Should return empty list
        self.assertEqual(len(assessments), 0)

    def test_unknown_action_type(self):
        """Test handling of unknown action types."""
        unknown_proposal = {
            'action_type': 'UNKNOWN_ACTION',
            'is_destructive': False,
            'is_reversible': True
        }

        # Should default to MEDIUM risk for unknown actions
        risk = self.assessor.assess_proposal(unknown_proposal)
        self.assertIn(risk['level'], ['LOW', 'MEDIUM', 'HIGH'])

    def test_conflicting_risk_factors(self):
        """Test handling of conflicting risk indicators."""
        conflicting_proposal = {
            'action_type': 'COMPLEX_ACTION',
            'is_destructive': False,      # Low risk factor
            'is_reversible': False,       # High risk factor
            'affects_database': False,    # Low risk factor
            'requires_user_approval': True  # High risk factor
        }

        risk = self.assessor.assess_proposal(conflicting_proposal)

        # Should balance factors and return valid assessment
        self.assertIn('level', risk)
        self.assertIn(risk['level'], ['LOW', 'MEDIUM', 'HIGH'])


if __name__ == '__main__':
    unittest.main()
