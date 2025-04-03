import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression

# Set Streamlit Page Config
st.set_page_config(page_title="💰 Rich or Bankrupt? AI Lifestyle Analyzer", layout="wide")
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

# Securely Store Credentials
if "secrets" in st.secrets:
    stored_username = st.secrets["username"]
    stored_password = st.secrets["password"]
    if username == stored_username and password == stored_password:
        st.sidebar.success("✅ Logged in successfully!")
    else:
        st.sidebar.error("❌ Incorrect credentials")

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

# Calculate Financial Metrics
expenses = rent + emi + food + fun + extra_expenses + emergency_fund + custom_expense_value
net_savings = income - expenses
net_worth_now = savings * 12

debt_to_income_ratio = (emi / income) * 100 if income > 0 else 0
savings_rate = (savings / income) * 100 if income > 0 else 0

# Display Financial Metrics
st.subheader("📊 Financial Summary")
col1, col2, col3 = st.columns(3)
col1.metric("Monthly Net Savings", f"{currency_symbol}{net_savings}")
col2.metric("Debt-to-Income Ratio", f"{debt_to_income_ratio:.2f}%")
col3.metric("Savings Rate", f"{savings_rate:.2f}%")

# Predict Future Net Worth with Inflation
def predict_net_worth(years=5, growth_rate=growth_rate, inflation_rate=inflation_rate):
    real_growth = growth_rate - inflation_rate
    years_array = np.array(range(1, years + 1)).reshape(-1, 1)
    savings_array = np.array([net_worth_now * (1 + real_growth) ** i for i in range(1, years + 1)]).reshape(-1, 1)
    model = LinearRegression()
    model.fit(years_array, savings_array)
    future_net_worth = model.predict(np.array([[years]])).flatten()[0]
    return future_net_worth

predicted_worth = predict_net_worth()
st.subheader("📈 Net Worth Growth Over Time")
years = np.array(range(1, 6))
worth_over_time = [net_worth_now * (1 + (growth_rate - inflation_rate)) ** i for i in range(6)]
fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(np.array([0] + list(years)), [net_worth_now] + worth_over_time, marker='o', color='green')
ax.set_xlabel("Years")
ax.set_ylabel(f"Net Worth ({currency_symbol})")
ax.set_title("Projected Net Worth Growth")
ax.grid(True)
st.pyplot(fig)

st.caption("💬 Compare with friends & improve your financial future! 🚀")
