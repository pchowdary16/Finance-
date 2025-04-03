import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Set Streamlit Page Config (MUST BE THE FIRST COMMAND)
st.set_page_config(page_title="💰 AI Twin Wealth Analyzer", layout="wide")

st.title("💰 Rich or Bankrupt? AI Lifestyle Analyzer")

# Sidebar: Currency Selection
currency = st.sidebar.selectbox("Currency", ["₹ (INR)", "$ (USD)", "€ (EUR)", "£ (GBP)"])
currency_symbol = currency.split()[0]

# Sidebar: Financial Inputs
st.sidebar.header("💰 Financial Details")
income = st.number_input(f"Monthly Income ({currency_symbol})", min_value=0, step=1000)
rent = st.number_input(f"Rent ({currency_symbol})", min_value=0, step=500)
investments = st.number_input(f"Investments ({currency_symbol})", min_value=0, step=500)
entertainment = st.number_input(f"Entertainment ({currency_symbol})", min_value=0, step=500)
fun = st.number_input(f"Fun ({currency_symbol})", min_value=0, step=500)
food = st.number_input(f"Food & Groceries ({currency_symbol})", min_value=0, step=500)

# Calculate Expenses and Savings
total_expenses = rent + investments + entertainment + fun + food
net_savings = income - total_expenses
current_net_worth = investments * 12  # Annual investments accumulation

# Growth Rate Inputs
growth_rate = st.sidebar.slider("Expected Growth Rate (%)", 0.0, 15.0, 8.0) / 100
inflation_rate = st.sidebar.slider("Inflation Rate (%)", 0.0, 10.0, 3.0) / 100

# AI Twin Financial Adjustments
st.subheader("✅ Compare Your Future Net Worth vs. AI Twin’s Net Worth – Who’s richer in 10 years?")

# AI Twin reallocates 50% from entertainment & fun to investments
ai_investments = investments + (0.5 * (entertainment + fun))
ai_entertainment = entertainment * 0.5
ai_fun = fun * 0.5

# Recalculate expenses for AI Twin
ai_total_expenses = rent + ai_investments + ai_entertainment + ai_fun + food
ai_net_savings = income - ai_total_expenses
ai_current_net_worth = ai_investments * 12

# Net Worth Prediction Function
def predict_net_worth(years=10, base_net_worth=current_net_worth, invest_rate=growth_rate):
    real_growth = invest_rate - inflation_rate
    return [base_net_worth * (1 + real_growth) ** i for i in range(years + 1)]

# Calculate projected net worth over 10 years
years = np.arange(11)
user_worth_over_time = predict_net_worth()
ai_worth_over_time = predict_net_worth(base_net_worth=ai_current_net_worth, invest_rate=growth_rate + 0.02)

# Plotting Future Net Worth Comparison
fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(years, user_worth_over_time, marker='o', color='green', label="Your Net Worth")
ax.plot(years, ai_worth_over_time, marker='o', color='blue', linestyle='dashed', label="AI Twin's Net Worth")
ax.set_xlabel("Years")
ax.set_ylabel(f"Net Worth ({currency_symbol})")
ax.set_title("Projected Net Worth Growth: You vs. AI Twin")
ax.legend()
ax.grid(True)
st.pyplot(fig)

# Display Comparison Metrics
st.subheader("📊 AI Twin’s Optimized Plan vs. Your Current Plan")
col1, col2 = st.columns(2)
col1.metric("Your Monthly Investments", f"{currency_symbol}{investments}")
col2.metric("AI Twin’s Monthly Investments", f"{currency_symbol}{ai_investments}")

col1.metric("Your 10-Year Net Worth", f"{currency_symbol}{user_worth_over_time[-1]:,.0f}")
col2.metric("AI Twin’s 10-Year Net Worth", f"{currency_symbol}{ai_worth_over_time[-1]:,.0f}")

st.caption("💬 Optimize your finances like an AI and build a better future! 🚀")
