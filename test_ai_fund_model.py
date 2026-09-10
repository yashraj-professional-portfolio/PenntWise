"""
Unit and integration tests for PennyWise AI Fund Tracking, Explaining Model, and Suggestion Engine.
"""

import unittest
import numpy as np
import pandas as pd
from ai_fund_model import (
    FinancialProfile,
    FundTrackingModel,
    ExplainableEngine,
    SuggestionEngine,
    generate_synthetic_training_data,
    get_default_pennywise_profile
)


class TestAIFundModel(unittest.TestCase):

    def setUp(self):
        self.profile = get_default_pennywise_profile()
        self.tracker = FundTrackingModel().fit()
        self.explainer = ExplainableEngine(self.tracker)
        self.suggester = SuggestionEngine(self.tracker, self.explainer)

    def test_profile_metrics_calculation(self):
        """Test fundamental accounting calculations in FinancialProfile."""
        self.assertEqual(self.profile.monthly_income, 3450.0)
        expected_expenses = 950 + 420 + 380 + 180.50 + 110 + 80 + 65 + 50 + 0
        self.assertAlmostEqual(self.profile.total_expenses, expected_expenses, places=2)
        self.assertAlmostEqual(self.profile.net_cashflow, 3450.0 - expected_expenses, places=2)
        self.assertTrue(0.0 < self.profile.savings_rate < 1.0)
        self.assertGreater(self.profile.emergency_runway_months, 3.0)

    def test_synthetic_data_generation(self):
        """Verify synthetic data adheres to schema and sensible ranges."""
        df = generate_synthetic_training_data(n_samples=50, random_seed=123)
        self.assertEqual(len(df), 50)
        self.assertIn("target_health_score", df.columns)
        self.assertIn("target_savings_6m", df.columns)
        self.assertTrue((df["target_health_score"] >= 0).all() and (df["target_health_score"] <= 100).all())

    def test_fund_tracking_predictions(self):
        """Verify health score prediction and 6-month savings projection."""
        score = self.tracker.predict_health_score(self.profile)
        self.assertIsInstance(score, float)
        self.assertGreaterEqual(score, 0.0)
        self.assertLessEqual(score, 100.0)

        trajectory = self.tracker.predict_savings_trajectory(self.profile, months=6)
        self.assertEqual(len(trajectory), 6)
        self.assertGreater(trajectory[-1]["projected_balance"], self.profile.current_savings)
        self.assertTrue(0 <= trajectory[-1]["savings_goal_progress_pct"] <= 100)

    def test_anomaly_detection(self):
        """Verify anomaly detection on high-spike profiles."""
        spike_profile = FinancialProfile(
            user_name="Spike User",
            monthly_income=2000.0,
            housing_expense=700.0,
            groceries_expense=700.0,  # 35% of income -> high grocery anomaly
            dining_expense=500.0,     # 25% of income -> high dining anomaly
            transport_expense=100.0,
            entertainment_expense=50.0,
            utilities_expense=50.0,
            subscriptions_expense=90.0,  # High subscriptions
            misc_expense=20.0,
            current_savings=500.0,
            savings_goal_target=5000.0,
            monthly_savings_target=200.0,
            unusual_charges=150.0
        )
        anomalies = self.tracker.detect_anomalies(spike_profile)
        categories = [a["category"] for a in anomalies]
        self.assertIn("Dining Out", categories)
        self.assertIn("Groceries", categories)
        self.assertIn("Subscriptions", categories)
        self.assertIn("Unusual Charges", categories)

    def test_explainable_ai_shap_attributions(self):
        """Verify SHAP calculations, feature impact directions, and narrative."""
        attr = self.explainer.get_feature_attributions(self.profile)
        self.assertIn("base_health_score", attr)
        self.assertIn("predicted_health_score", attr)
        self.assertTrue(len(attr["top_positive_drivers"]) > 0)
        self.assertTrue(len(attr["top_negative_drags"]) > 0)

        narrative = self.explainer.generate_narrative_explanation(self.profile)
        self.assertIn("summary_narrative", narrative)
        self.assertIn(narrative["status"], ["Strong & Resilient", "Moderate with Optimization Room", "High Vulnerability"])
        self.assertTrue(len(narrative["key_insights"]) > 0)

    def test_suggestion_engine_generation(self):
        """Verify actionable recommendations are produced with quantified impacts."""
        suggestions = self.suggester.generate_suggestions(self.profile)
        self.assertGreater(len(suggestions), 0)
        for s in suggestions:
            self.assertIn("id", s)
            self.assertIn("title", s)
            self.assertIn("priority", s)
            self.assertIn("monthly_savings", s)
            self.assertGreater(s["monthly_savings"], 0)
            self.assertIn("health_score_impact", s)
            self.assertIn("rationale", s)


if __name__ == "__main__":
    unittest.main()
