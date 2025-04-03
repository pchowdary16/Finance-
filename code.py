import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression

# Set Streamlit Page Config (Must be the first command)
st.set_page_config(page_title="💰 Rich or Bankrupt? AI Lifestyle Analyzer", layout="wide")

st.markdown("""
    <style>
        body {
            background-color: white !important;
        }
    </style>
""", unsafe_allow_html=True)

st.title("💰 Rich or Bankrupt? AI Lifestyle Analyzer")

# Sidebar Profile Section
if "show_account" not in st.session_state:
    st.session_state.show_account = False

def toggle_account_details():
    st.session_state.show_account = not st.session_state.show_account

st.sidebar.image("https://via.placeholder.com/100", width=100)
st.sidebar.button("👤 Profile", on_click=toggle_account_details)

if st.session_state.show_account:
    with st.sidebar.expander("Account Details", expanded=True):
        name = st.text_input("Name")
        email = st.text_input("Email")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

# Currency Selection
currency = st.sidebar.selectbox("Currency", ["₹ (INR)", "$ (USD)", "€ (EUR)", "£ (GBP)"])
currency_symbol = currency.split()[0]

# Financial Inputs
st.sidebar.header("Financial Details")
with st.sidebar.expander("💰 Income & Savings", expanded=False):
    income = st.number_input(f"Monthly Income ({currency_symbol})", min_value=0, step=1000)
    savings = st.number_input(f"Monthly Savings ({currency_symbol})", min_value=0, step=500)
    savings_goal = st.number_input(f"Savings Goal ({currency_symbol})", min_value=0, step=10000)
    crypto = st.number_input(f"Crypto/Investments ({currency_symbol})", min_value=0, step=500)
    growth_rate = st.slider("Expected Growth Rate (%)", 0.0, 15.0, 8.0) / 100
    inflation_rate = st.slider("Inflation Rate (%)", 0.0, 10.0, 3.0) / 100

with st.sidebar.expander("🏠 Fixed Expenses", expanded=False):
    rent = st.number_input(f"Rent ({currency_symbol})", min_value=0, step=500)
    emi = st.number_input(f"EMI ({currency_symbol})", min_value=0, step=500)
    emergency_fund = st.number_input(f"Emergency Fund Contribution ({currency_symbol})", min_value=0, step=500)

with st.sidebar.expander("🍔 Flexible Expenses", expanded=False):
    food = st.number_input(f"Food & Groceries ({currency_symbol})", min_value=0, step=500)
    fun = st.number_input(f"Entertainment ({currency_symbol})", min_value=0, step=500)
    extra_expenses = st.number_input(f"Extra Expenses ({currency_symbol})", min_value=0, step=500)
    custom_expense = st.text_input("Custom Expense Name")
    custom_expense_value = st.number_input(f"Custom Expense ({currency_symbol})", min_value=0, step=500)

# Major Life Event Planner
st.sidebar.subheader("💎 Life Event Planner")
life_event = st.sidebar.selectbox("Plan for a major life event:", ["None", "Marriage", "Kids", "Home Purchase"])
if life_event != "None":
    additional_cost = st.sidebar.number_input(f"Estimated Additional Cost for {life_event} ({currency_symbol})", min_value=0, step=1000)
else:
    additional_cost = 0

# Calculate Financial Metrics
expenses = rent + emi + food + fun + extra_expenses + emergency_fund + custom_expense_value + additional_cost
net_savings = income - expenses
net_worth_now = savings * 12

debt_to_income_ratio = (emi / income * 100) if income > 0 else 0
savings_rate = (savings / income * 100) if income > 0 else 0

# Display Financial Metrics
st.subheader("📊 Financial Summary")
col1, col2, col3 = st.columns(3)
col1.metric("Monthly Net Savings", f"{currency_symbol}{net_savings}")
col2.metric("Debt-to-Income Ratio", f"{debt_to_income_ratio:.2f}%")
col3.metric("Savings Rate", f"{savings_rate:.2f}%")

# Predict Future Savings
st.subheader("💰 How Much Can You Save in 5 Years?")
future_savings = savings * 12 * 5
st.metric("Projected Savings in 5 Years", f"{currency_symbol}{future_savings}")

# Predict Future Net Worth
st.subheader("📈 Net Worth Growth Over Time")
def predict_net_worth(years=10, growth_rate=growth_rate, inflation_rate=inflation_rate):
    real_growth = growth_rate - inflation_rate
    return [net_worth_now * (1 + real_growth) ** i for i in range(years + 1)]

worth_over_time = predict_net_worth()
years = np.arange(11)
fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(years, worth_over_time, marker='o', color='green', label="Your Net Worth")
ax.set_xlabel("Years")
ax.set_ylabel(f"Net Worth ({currency_symbol})")
ax.set_title("Projected Net Worth Growth")
ax.grid(True)
ax.legend()
st.pyplot(fig)

# Set Streamlit Page Config
st.set_page_config(page_title="💰 AI Twin Wealth Analyzer", layout="wide")

st.title("✅ Compare Your Future Net Worth vs. AI Twin’s Net Worth – Who’s Richer in 10 Years?")

# User Inputs
income = st.number_input("Monthly Income ($)", min_value=1000, step=500, value=10000)
rent = st.number_input("Rent ($)", min_value=0, step=100, value=1000)
investments = st.number_input("Investments ($)", min_value=0, step=500, value=3000)
entertainment = st.number_input("Entertainment ($)", min_value=0, step=500, value=2000)
fun = st.number_input("Fun & Leisure ($)", min_value=0, step=500, value=2000)
food = st.number_input("Food & Groceries ($)", min_value=0, step=500, value=2000)

# User Expense Breakdown
expenses = rent + investments + entertainment + fun + food
savings = income - expenses

# AI Twin Optimization
ai_investments = investments + (entertainment * 0.5) + (fun * 0.5)  # AI reallocates 50% from fun & entertainment to investments
ai_entertainment = entertainment * 0.5  # AI reduces entertainment spending
ai_fun = fun * 0.5  # AI reduces fun spending
ai_expenses = rent + ai_investments + ai_entertainment + ai_fun + food
ai_savings = income - ai_expenses

# Growth Simulation
def calculate_net_worth(starting_savings, monthly_savings, growth_rate, years=10):
    net_worth = [starting_savings]
    for i in range(1, years + 1):
        net_worth.append(net_worth[-1] * (1 + growth_rate) + monthly_savings * 12)
    return net_worth

# Growth Rates
user_growth_rate = 0.07  # 7% annual return
ai_growth_rate = 0.10  # 10% annual return due to better investment allocation

# Net Worth Calculation
years = np.arange(11)
user_net_worth = calculate_net_worth(0, savings, user_growth_rate)
ai_net_worth = calculate_net_worth(0, ai_savings, ai_growth_rate)

# Plotting
fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(years, user_net_worth, marker='o', color='green', label="Your Net Worth")
ax.plot(years, ai_net_worth, marker='o', color='blue', linestyle='dashed', label="AI Twin's Net Worth")
ax.set_xlabel("Years")
ax.set_ylabel("Net Worth ($)")
ax.set_title("Projected Net Worth Growth: You vs. AI Twin")
ax.legend()
ax.grid(True)

st.pyplot(fig)

# Display Comparison Metrics
st.subheader("📊 Financial Comparison")
col1, col2 = st.columns(2)
col1.metric("Your 10-Year Net Worth", f"${user_net_worth[-1]:,.2f}")
col2.metric("AI Twin's 10-Year Net Worth", f"${ai_net_worth[-1]:,.2f}")

st.caption("💡 AI Twin optimizes your spending for a better financial future! 🚀")
