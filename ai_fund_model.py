"""
PennyWise AI Fund Tracking, Explainable AI (XAI), and Smart Recommendation Model.

This module implements:
1. FundTrackingModel: Tracks income, expenses, category burn rates, anomalies, and predicts cashflow trajectories.
2. ExplainableEngine: Computes SHAP feature attribution and generates human-readable explanations of financial health.
3. SuggestionEngine: Synthesizes predictive insights into prioritized, actionable recommendations.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Tuple, Optional
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import Ridge
from sklearn.preprocessing import StandardScaler
import shap


@dataclass
class FinancialProfile:
    user_name: str
    monthly_income: float
    housing_expense: float
    groceries_expense: float
    dining_expense: float
    transport_expense: float
    entertainment_expense: float
    utilities_expense: float
    subscriptions_expense: float
    misc_expense: float
    current_savings: float
    savings_goal_target: float
    monthly_savings_target: float
    unusual_charges: float = 0.0

    @property
    def total_expenses(self) -> float:
        return (
            self.housing_expense
            + self.groceries_expense
            + self.dining_expense
            + self.transport_expense
            + self.entertainment_expense
            + self.utilities_expense
            + self.subscriptions_expense
            + self.misc_expense
            + self.unusual_charges
        )

    @property
    def net_cashflow(self) -> float:
        return self.monthly_income - self.total_expenses

    @property
    def savings_rate(self) -> float:
        if self.monthly_income <= 0:
            return 0.0
        return max(0.0, (self.net_cashflow / self.monthly_income))

    @property
    def emergency_runway_months(self) -> float:
        if self.total_expenses <= 0:
            return 99.0
        return self.current_savings / self.total_expenses

    @property
    def discretionary_spend(self) -> float:
        return self.dining_expense + self.entertainment_expense + self.misc_expense

    @property
    def fixed_spend(self) -> float:
        return self.housing_expense + self.utilities_expense + self.subscriptions_expense

    def to_feature_dict(self) -> Dict[str, float]:
        total_exp = max(1.0, self.total_expenses)
        inc = max(1.0, self.monthly_income)
        return {
            "monthly_income": self.monthly_income,
            "total_expenses": total_exp,
            "net_cashflow": self.net_cashflow,
            "savings_rate": self.savings_rate,
            "emergency_runway_months": self.emergency_runway_months,
            "housing_ratio": self.housing_expense / inc,
            "groceries_ratio": self.groceries_expense / inc,
            "dining_ratio": self.dining_expense / inc,
            "transport_ratio": self.transport_expense / inc,
            "entertainment_ratio": self.entertainment_expense / inc,
            "subscriptions_ratio": self.subscriptions_expense / inc,
            "utilities_ratio": self.utilities_expense / inc,
            "discretionary_spend": self.dining_expense + self.entertainment_expense + self.misc_expense,
            "fixed_spend": self.housing_expense + self.utilities_expense + self.subscriptions_expense,
            "current_savings": self.current_savings,
            "unusual_charges": self.unusual_charges
        }


def generate_synthetic_training_data(n_samples: int = 1200, random_seed: int = 42) -> pd.DataFrame:
    """Generates realistic student & young professional financial records for training."""
    np.random.seed(random_seed)

    incomes = np.random.uniform(1500, 6500, n_samples)
    records = []

    for inc in incomes:
        # Realistic student/young adult budget splits
        housing = inc * np.random.uniform(0.22, 0.45)
        groceries = inc * np.random.uniform(0.10, 0.22)
        dining = inc * np.random.uniform(0.05, 0.20)
        transport = inc * np.random.uniform(0.04, 0.12)
        entertainment = inc * np.random.uniform(0.03, 0.15)
        utilities = inc * np.random.uniform(0.03, 0.08)
        subscriptions = np.random.uniform(15, 95)
        misc = inc * np.random.uniform(0.02, 0.10)
        unusual = np.random.choice([0.0, 0.0, 0.0, 45.0, 120.0, 250.0], p=[0.70, 0.15, 0.05, 0.05, 0.03, 0.02])
        savings = np.random.uniform(500, 20000)
        goal_target = np.random.uniform(3000, 15000)
        monthly_target = inc * np.random.uniform(0.10, 0.25)

        profile = FinancialProfile(
            user_name="Synthetic User",
            monthly_income=inc,
            housing_expense=housing,
            groceries_expense=groceries,
            dining_expense=dining,
            transport_expense=transport,
            entertainment_expense=entertainment,
            utilities_expense=utilities,
            subscriptions_expense=subscriptions,
            misc_expense=misc,
            current_savings=savings,
            savings_goal_target=goal_target,
            monthly_savings_target=monthly_target,
            unusual_charges=unusual
        )

        feats = profile.to_feature_dict()

        # Calculate synthetic Target Health Score (0 - 100) based on economic fundamentals
        # 1. Savings Rate component (max 30 pts)
        c_sav = min(30.0, profile.savings_rate * 100.0)
        # 2. Budget Discipline (low discretionary ratio) (max 25 pts)
        disc_ratio = feats["discretionary_spend"] / max(1.0, inc)
        c_disc = max(0.0, 25.0 - (disc_ratio * 40.0))
        # 3. Emergency Runway (max 20 pts, full score at >= 6 months)
        c_runway = min(20.0, (profile.emergency_runway_months / 6.0) * 20.0)
        # 4. Housing Burdensome Penalty (max 15 pts)
        c_house = max(0.0, 15.0 - max(0.0, (feats["housing_ratio"] - 0.30) * 50.0))
        # 5. Anomaly Penalty (max 10 pts)
        c_anom = max(0.0, 10.0 - (unusual / 25.0))

        noise = np.random.normal(0, 2.0)
        health_score = np.clip(c_sav + c_disc + c_runway + c_house + c_anom + noise, 10.0, 99.0)

        # Projected 6-month savings accumulation target
        projected_savings_6m = savings + (profile.net_cashflow * 6.0) + np.random.normal(0, 100)

        feats["target_health_score"] = round(health_score, 1)
        feats["target_savings_6m"] = round(projected_savings_6m, 2)
        records.append(feats)

    return pd.DataFrame(records)


class FundTrackingModel:
    """Core predictive model that tracks fund health, forecasts balances, and detects anomalies."""

    def __init__(self):
        self.feature_columns = [
            "monthly_income",
            "total_expenses",
            "net_cashflow",
            "savings_rate",
            "emergency_runway_months",
            "housing_ratio",
            "groceries_ratio",
            "dining_ratio",
            "transport_ratio",
            "entertainment_ratio",
            "subscriptions_ratio",
            "utilities_ratio",
            "discretionary_spend",
            "fixed_spend",
            "current_savings",
            "unusual_charges"
        ]
        self.health_model = RandomForestRegressor(n_estimators=100, max_depth=6, random_state=42)
        self.forecast_model = Ridge(alpha=1.0)
        self.scaler = StandardScaler()
        self.is_fitted = False

    def fit(self, df: Optional[pd.DataFrame] = None) -> "FundTrackingModel":
        if df is None:
            df = generate_synthetic_training_data()

        X = df[self.feature_columns]
        y_health = df["target_health_score"]
        y_forecast = df["target_savings_6m"]

        self.health_model.fit(X, y_health)

        X_scaled = self.scaler.fit_transform(X)
        self.forecast_model.fit(X_scaled, y_forecast)

        self.is_fitted = True
        return self

    def predict_health_score(self, profile: FinancialProfile) -> float:
        if not self.is_fitted:
            self.fit()
        feats = pd.DataFrame([profile.to_feature_dict()])[self.feature_columns]
        score = self.health_model.predict(feats)[0]
        return float(np.clip(score, 0.0, 100.0))

    def predict_savings_trajectory(self, profile: FinancialProfile, months: int = 6) -> List[Dict[str, Any]]:
        """Projects month-by-month fund balance trajectory with confidence intervals."""
        trajectory = []
        running_savings = profile.current_savings
        monthly_net = profile.net_cashflow

        for m in range(1, months + 1):
            running_savings += monthly_net
            # Variance expands with time horizon
            uncertainty = np.sqrt(m) * (abs(profile.discretionary_spend) * 0.15)
            trajectory.append({
                "month_index": m,
                "projected_balance": round(running_savings, 2),
                "lower_bound": round(max(0.0, running_savings - uncertainty), 2),
                "upper_bound": round(running_savings + uncertainty, 2),
                "savings_goal_progress_pct": round(min(100.0, (running_savings / max(1.0, profile.savings_goal_target)) * 100), 1)
            })
        return trajectory

    def detect_anomalies(self, profile: FinancialProfile) -> List[Dict[str, Any]]:
        """Identifies out-of-band spending categories and micro-leakages."""
        anomalies = []
        inc = profile.monthly_income

        if profile.dining_expense > (inc * 0.18):
            anomalies.append({
                "category": "Dining Out",
                "severity": "HIGH",
                "message": f"Dining out is consuming {(profile.dining_expense/inc)*100:.1f}% of income, exceeding safe student threshold (15%).",
                "excess_amount": round(profile.dining_expense - (inc * 0.12), 2)
            })

        if profile.groceries_expense > (inc * 0.25):
            anomalies.append({
                "category": "Groceries",
                "severity": "MEDIUM",
                "message": f"Grocery expenses are {(profile.groceries_expense/inc)*100:.1f}% of income, 35% above peer average.",
                "excess_amount": round(profile.groceries_expense - (inc * 0.18), 2)
            })

        if profile.subscriptions_expense > 65.0:
            anomalies.append({
                "category": "Subscriptions",
                "severity": "MEDIUM",
                "message": f"Total monthly subscriptions of ${profile.subscriptions_expense:.2f} suggest recurring unused memberships.",
                "excess_amount": round(profile.subscriptions_expense - 30.0, 2)
            })

        if profile.unusual_charges > 50.0:
            anomalies.append({
                "category": "Unusual Charges",
                "severity": "HIGH",
                "message": f"Detected ${profile.unusual_charges:.2f} in non-routine single-charge anomalies.",
                "excess_amount": profile.unusual_charges
            })

        return anomalies


class ExplainableEngine:
    """Explainable AI (XAI) engine using SHAP for interpreting model decisions and fund trajectories."""

    def __init__(self, tracking_model: FundTrackingModel):
        self.tracking_model = tracking_model
        if not self.tracking_model.is_fitted:
            self.tracking_model.fit()
        self.explainer = shap.TreeExplainer(self.tracking_model.health_model)
        self.feature_columns = self.tracking_model.feature_columns

    def get_feature_attributions(self, profile: FinancialProfile) -> Dict[str, Any]:
        """Calculates exact SHAP values for individual financial factors."""
        feats = pd.DataFrame([profile.to_feature_dict()])[self.feature_columns]
        shap_vals = self.explainer.shap_values(feats)[0]
        base_value = float(self.explainer.expected_value[0] if isinstance(self.explainer.expected_value, np.ndarray) else self.explainer.expected_value)

        attributions = []
        friendly_names = {
            "monthly_income": "Monthly Inflows",
            "total_expenses": "Total Outflow Burn",
            "net_cashflow": "Net Monthly Surplus",
            "savings_rate": "Savings Velocity Rate",
            "emergency_runway_months": "Emergency Runway Depth",
            "housing_ratio": "Housing Overhead",
            "groceries_ratio": "Grocery Basket Cost",
            "dining_ratio": "Dining & Takeout",
            "transport_ratio": "Transit & Gas",
            "entertainment_ratio": "Entertainment & Events",
            "subscriptions_ratio": "Recurring Subscriptions",
            "utilities_ratio": "Utilities & Bills",
            "discretionary_spend": "Discretionary Spending",
            "fixed_spend": "Fixed Commitments",
            "current_savings": "Liquid Cash Reserves",
            "unusual_charges": "Unscheduled Spike Charges"
        }

        for feat, val in zip(self.feature_columns, shap_vals):
            attributions.append({
                "feature": feat,
                "display_name": friendly_names.get(feat, feat),
                "shap_impact": round(float(val), 2),
                "direction": "POSITIVE" if val >= 0 else "NEGATIVE",
                "magnitude": round(abs(float(val)), 2),
                "raw_value": round(float(feats[feat].iloc[0]), 2)
            })

        # Sort by impact magnitude
        attributions.sort(key=lambda x: x["magnitude"], reverse=True)

        return {
            "base_health_score": round(base_value, 1),
            "predicted_health_score": round(base_value + float(np.sum(shap_vals)), 1),
            "top_positive_drivers": [a for a in attributions if a["shap_impact"] > 0][:4],
            "top_negative_drags": [a for a in attributions if a["shap_impact"] < 0][:4],
            "full_attributions": attributions
        }

    def generate_narrative_explanation(self, profile: FinancialProfile) -> Dict[str, Any]:
        """Translates mathematical SHAP values into an intuitive plain-English narrative."""
        attr = self.get_feature_attributions(profile)
        predicted_score = attr["predicted_health_score"]
        positives = attr["top_positive_drivers"]
        negatives = attr["top_negative_drags"]

        # Health tier definition
        if predicted_score >= 80:
            status = "Strong & Resilient"
        elif predicted_score >= 60:
            status = "Moderate with Optimization Room"
        else:
            status = "High Vulnerability"

        key_positive_text = ", ".join([f"{p['display_name']} (+{p['shap_impact']:.1f} pts)" for p in positives[:2]])
        key_negative_text = ", ".join([f"{n['display_name']} ({n['shap_impact']:.1f} pts)" for n in negatives[:2]])

        narrative = (
            f"Your financial health score is currently evaluated at {predicted_score}/100 ({status}). "
            f"The primary positive drivers elevating your score are {key_positive_text}. "
            f"Conversely, the primary drags pulling down your score are {key_negative_text}."
        )

        insights = []
        if profile.savings_rate >= 0.20:
            insights.append({
                "type": "STRENGTH",
                "title": "Superior Savings Rate",
                "body": f"You are saving {profile.savings_rate*100:.1f}% of income, outperforming the student benchmark of 15%."
            })
        elif profile.savings_rate < 0.10:
            insights.append({
                "type": "RISK",
                "title": "Thin Cash Cushion",
                "body": f"A savings rate of {profile.savings_rate*100:.1f}% leaves you vulnerable to sudden unexpected bills."
            })

        if profile.emergency_runway_months >= 3.0:
            insights.append({
                "type": "STRENGTH",
                "title": "Healthy Runway Buffer",
                "body": f"Your current savings of ${profile.current_savings:,.2f} provides {profile.emergency_runway_months:.1f} months of complete living expenses."
            })
        else:
            insights.append({
                "type": "OPPORTUNITY",
                "title": "Build Emergency Runway",
                "body": f"Your reserves only cover {profile.emergency_runway_months:.1f} months. Targeting 3.0 months (${profile.total_expenses*3:,.2f}) will boost your score by ~8 points."
            })

        return {
            "score": predicted_score,
            "status": status,
            "summary_narrative": narrative,
            "key_insights": insights,
            "attributions": attr
        }


class SuggestionEngine:
    """Synthesizes fund tracking data and XAI attributions into prioritized actionable recommendations."""

    def __init__(self, tracking_model: FundTrackingModel, explainable_engine: ExplainableEngine):
        self.tracking_model = tracking_model
        self.explainable_engine = explainable_engine

    def generate_suggestions(self, profile: FinancialProfile) -> List[Dict[str, Any]]:
        suggestions = []
        inc = profile.monthly_income

        # 1. Dining Out Optimization
        if profile.dining_expense > (inc * 0.12):
            potential_saving = round(profile.dining_expense * 0.35, 2)
            suggestions.append({
                "id": "rec_dining_trim",
                "priority": "HIGH",
                "category": "Discretionary Trim",
                "title": "Trim Dining & Takeout by 35%",
                "rationale": f"Dining expenses (${profile.dining_expense:.2f}) currently constitute {(profile.dining_expense/inc)*100:.1f}% of your monthly inflow. Replacing 2 takeout meals/week with home cooking recoups funds rapidly.",
                "monthly_savings": potential_saving,
                "projected_annual_savings": potential_saving * 12,
                "health_score_impact": "+4.8 pts",
                "goal_acceleration_days": 28,
                "action_type": "BUDGET_ADJUST",
                "target_category": "Dining Out"
            })

        # 2. Subscription Audit
        if profile.subscriptions_expense > 35.0:
            potential_saving = round(profile.subscriptions_expense - 25.0, 2)
            suggestions.append({
                "id": "rec_sub_audit",
                "priority": "MEDIUM",
                "category": "Recurring Leaks",
                "title": "Audit & Consolidate Streaming/SaaS Subscriptions",
                "rationale": f"You spend ${profile.subscriptions_expense:.2f}/mo on active digital services. Pausing 2 low-usage subscriptions saves an effortless ${potential_saving:.2f}/mo.",
                "monthly_savings": potential_saving,
                "projected_annual_savings": potential_saving * 12,
                "health_score_impact": "+2.3 pts",
                "goal_acceleration_days": 12,
                "action_type": "SUBSCRIPTION_CANCEL",
                "target_category": "Subscriptions"
            })

        # 3. Emergency Runway Acceleration
        if profile.emergency_runway_months < 3.0:
            target_buffer = profile.total_expenses * 3.0
            deficit = target_buffer - profile.current_savings
            monthly_boost = min(150.0, profile.net_cashflow * 0.40)
            suggestions.append({
                "id": "rec_emergency_boost",
                "priority": "HIGH",
                "category": "Safety Net",
                "title": "Auto-Route $100/mo into 3-Month Emergency Shield",
                "rationale": f"Your current cash runway is {profile.emergency_runway_months:.1f} months. Setting an automated transfer of ${monthly_boost:.2f}/mo hits your baseline in {(deficit/max(1, monthly_boost)):.0f} months.",
                "monthly_savings": round(monthly_boost, 2),
                "projected_annual_savings": round(monthly_boost * 12, 2),
                "health_score_impact": "+6.5 pts",
                "goal_acceleration_days": 45,
                "action_type": "AUTO_SAVINGS",
                "target_category": "Emergency Fund"
            })

        # 4. Smart Rebalancer to Savings Goal
        if profile.net_cashflow > 200.0:
            rebalance_amt = round(profile.net_cashflow * 0.50, 2)
            suggestions.append({
                "id": "rec_goal_rebalance",
                "priority": "MEDIUM",
                "category": "Goal Acceleration",
                "title": f"Rebalance ${rebalance_amt:.2f}/mo Surplus to Primary Goal",
                "rationale": f"You currently generate ${profile.net_cashflow:,.2f} in net monthly surplus. Locking in half of this surplus reaches your ${profile.savings_goal_target:,.2f} target 4 months earlier.",
                "monthly_savings": rebalance_amt,
                "projected_annual_savings": rebalance_amt * 12,
                "health_score_impact": "+3.9 pts",
                "goal_acceleration_days": 60,
                "action_type": "GOAL_REALLOCATION",
                "target_category": "Primary Savings Goal"
            })

        # 5. Grocery Basket Optimization
        if profile.groceries_expense > (inc * 0.16):
            potential_saving = round(profile.groceries_expense * 0.15, 2)
            suggestions.append({
                "id": "rec_grocery_optimize",
                "priority": "LOW",
                "category": "Smart Shopping",
                "title": "Switch to Bulk Buying for Pantry Staples",
                "rationale": f"Grocery expenses are ${profile.groceries_expense:.2f}/mo. Using weekly batch meal plans and store brands typically recovers 15% without sacrificing nutrition.",
                "monthly_savings": potential_saving,
                "projected_annual_savings": potential_saving * 12,
                "health_score_impact": "+2.1 pts",
                "goal_acceleration_days": 14,
                "action_type": "EXPENSE_OPTIMIZE",
                "target_category": "Groceries"
            })

        return suggestions


def get_default_pennywise_profile() -> FinancialProfile:
    """Returns the baseline profile aligned with PennyWise dashboard mock data."""
    return FinancialProfile(
        user_name="Alex Morgan",
        monthly_income=3450.00,
        housing_expense=950.00,
        groceries_expense=420.00,
        dining_expense=380.00,
        transport_expense=180.50,
        entertainment_expense=110.00,
        utilities_expense=80.00,
        subscriptions_expense=65.00,
        misc_expense=50.00,
        current_savings=8240.00,
        savings_goal_target=10000.00,
        monthly_savings_target=500.00,
        unusual_charges=0.00
    )


if __name__ == "__main__":
    print("=" * 70)
    print(" PennyWise AI Fund Tracking, Explaining Model & Suggestions Engine")
    print("=" * 70)

    profile = get_default_pennywise_profile()
    print(f"\nUser: {profile.user_name}")
    print(f"Monthly Income:    ${profile.monthly_income:,.2f}")
    print(f"Total Expenses:    ${profile.total_expenses:,.2f}")
    print(f"Net Cashflow:      ${profile.net_cashflow:,.2f}")
    print(f"Savings Rate:      {profile.savings_rate*100:.1f}%")
    print(f"Emergency Runway:  {profile.emergency_runway_months:.1f} months")

    # 1. Train / Initialize Models
    tracker = FundTrackingModel().fit()
    explainer = ExplainableEngine(tracker)
    suggester = SuggestionEngine(tracker, explainer)

    # 2. Score & Trajectory
    health_score = tracker.predict_health_score(profile)
    trajectory = tracker.predict_savings_trajectory(profile, months=6)
    print(f"\n[AI Fund Tracking] Evaluated Financial Health Score: {health_score:.1f}/100")
    print(f"6-Month Projected Savings: ${trajectory[-1]['projected_balance']:,.2f} ({trajectory[-1]['savings_goal_progress_pct']}% of Goal)")

    # 3. Explainable AI Breakdown
    print("\n" + "=" * 70)
    print(" [Explaining Model] SHAP-Based Feature Attribution & Narrative")
    print("=" * 70)
    narrative = explainer.generate_narrative_explanation(profile)
    print(f"Status: {narrative['status']}")
    print(f"Summary: {narrative['summary_narrative']}\n")
    print("Top Positive Drivers:")
    for p in narrative["attributions"]["top_positive_drivers"]:
        print(f"  [+] {p['display_name']:<25}: +{p['shap_impact']} pts (Raw Value: {p['raw_value']})")
    print("\nTop Negative Drags:")
    for n in narrative["attributions"]["top_negative_drags"]:
        print(f"  [-] {n['display_name']:<25}: {n['shap_impact']} pts (Raw Value: {n['raw_value']})")

    # 4. Actionable Suggestions
    print("\n" + "=" * 70)
    print(" [Smart Suggestion Engine] Prioritized AI Recommendations")
    print("=" * 70)
    suggestions = suggester.generate_suggestions(profile)
    for idx, s in enumerate(suggestions, 1):
        print(f"\n{idx}. [{s['priority']}] {s['title']}")
        print(f"   Category: {s['category']} | Score Impact: {s['health_score_impact']}")
        print(f"   Monthly Savings: ${s['monthly_savings']:.2f} | Annual: ${s['projected_annual_savings']:.2f}")
        print(f"   Rationale: {s['rationale']}")
