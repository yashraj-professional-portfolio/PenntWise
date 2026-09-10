# PennyWise Finance - AI-Powered Personal Finance Manager

A modern, student-friendly personal finance management web application featuring Explainable AI (XAI) Fund Tracking, Cashflow Forecasting, and Smart Action Recommendations.

---

## 🌟 Features

1. **AI Fund Advisor & Explainer** (`ai_fund_advisor_pennywise_finance/code.html`):
   - **Composite Financial Health Index** (0-100) with 4-pillar dimensional scoring.
   - **Explaining Model (XAI)**: SHAP-powered feature attribution displaying positive boosters vs negative drags with natural-language causal reasoning.
   - **Prioritized Recommendations**: High/Medium/Low impact actionable advice with 1-click budget integration.
   - **Interactive "What-If" Fund Simulator**: Real-time reactive sliders for income and discretionary spending.
   - **AI Financial Copilot Chat**: Conversational AI assistant for instant financial queries and scenario analysis.

2. **Overview Dashboard** (`dashboard_pennywise_finance/code.html`):
   - Net cashflow snapshots, income/expense breakdown, monthly trend graphs, and AI summary widget.

3. **Budgets** (`budgets_pennywise_finance/code.html`):
   - Category-level envelope budgeting, real-time burn rate gauges, and alerts.

4. **Savings Goals** (`savings_goals_pennywise_finance/code.html`):
   - Milestone tracking, target completion dates, and automatic surplus allocations.

5. **Transactions** (`transactions_pennywise_finance/code.html`):
   - Complete transaction ledger, categorization badges, search, and expense filtering.

---

## 🚀 How to Run the Website

### Option 1: Direct Browser Launch (Zero Installation Required)
Simply double-click or open **`index.html`** in any modern web browser (Google Chrome, Microsoft Edge, Firefox, Safari).

You can also directly open any of the individual screen files:
- `index.html` - Main Navigation Hub
- `ai_fund_advisor_pennywise_finance/code.html` - AI Fund Advisor & Explainer
- `dashboard_pennywise_finance/code.html` - Financial Overview Dashboard
- `budgets_pennywise_finance/code.html` - Budget Planner
- `savings_goals_pennywise_finance/code.html` - Savings Goals Tracker
- `transactions_pennywise_finance/code.html` - Transaction Ledger

### Option 2: Local HTTP Server (Optional)
```bash
python -m http.server 8000
```
Then navigate to `http://localhost:8000` in your web browser.

---

## 🧠 Python AI Model & Test Suite

The project includes a full Python ML and Explainable AI pipeline using `scikit-learn`, `shap`, `pandas`, and `numpy`.

### Run the AI Fund Tracking & XAI Explainer:
```bash
python ai_fund_model.py
```

### Run Automated Unit & Integration Tests:
```bash
python test_ai_fund_model.py
```

---

## 🎨 Design System

Built on the **Equilibrium Finance Design System** (`equilibrium_finance/DESIGN.md`):
- **Typography**: Manrope (Headlines/Hero Numbers), Work Sans (Body/Labels), JetBrains Mono (Data/Metrics)
- **Palette**: Modern tonal layering with Trust Blue (`#004ac6`), Growth Green (`#006c49`), Alert Amber (`#784b00`), and Crisp Canvas (`#f8f9ff`).
