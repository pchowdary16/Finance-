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

# Extras Section
st.sidebar.subheader("📂 Extras")
st.sidebar.text_area("Additional Notes")
uploaded_file = st.sidebar.file_uploader("Upload Financial Data (CSV)")
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.sidebar.write("Uploaded Data Preview:", df.head())
    if "Income" in df.columns:
        income = st.number_input(f"Monthly Income ({currency_symbol})", min_value=0, value=int(df["Income"].mean()))

# Reset Button
if st.sidebar.button("Reset All"):
    for key in st.session_state.keys():
        del st.session_state[key]
    st.experimental_rerun()

# Calculate Net Savings
expenses = rent + emi + food + fun + extra_expenses + emergency_fund + custom_expense_value
net_savings = income - expenses
net_worth_now = savings * 12

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

# Display Results
st.subheader("📊 Financial Summary")
col1, col2, col3 = st.columns(3)
col1.metric("Monthly Net Savings", f"{currency_symbol}{net_savings}")
col2.metric("Predicted Net Worth in 5 Years", f"{currency_symbol}{predicted_worth:,.2f}")
progress = min((net_worth_now / savings_goal) * 100, 100) if savings_goal > 0 else 0
col3.progress(progress / 100)

# Expense Breakdown Pie Chart
st.subheader("📌 Where Your Money Goes")
fig, ax = plt.subplots()
labels = ["Rent", "EMI", "Food", "Entertainment", "Extra Expenses", "Emergency Fund", custom_expense or "Custom"]
data = [rent, emi, food, fun, extra_expenses, emergency_fund, custom_expense_value]
filtered_data = [(label, value) for label, value in zip(labels, data) if value > 0]
if filtered_data:
    filtered_labels, filtered_values = zip(*filtered_data)
    colors = sns.color_palette("pastel", len(filtered_values))
    ax.pie(filtered_values, labels=filtered_labels, autopct='%1.1f%%', colors=colors, startangle=140)
    ax.set_title("Expense Breakdown")
    st.pyplot(fig)
else:
    st.write("No expenses to display.")

# Net Worth Trend Line
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

# Money Persona Badge
st.subheader("🏆 Your Money Persona")
if predicted_worth > 5000000:
    persona = "🔥 Smart Investor! You're on track to be wealthy!"
    st.success(persona)
elif predicted_worth > 1000000:
    persona = "💡 Balanced Saver! Keep up the good work!"
    st.info(persona)
else:
    persona = "⚠️ YOLO Spender! Consider saving more!"
    st.warning(persona)

# AI Money Coach Advice
st.subheader("💡 AI Money Coach Suggestions")
advice = []
if expenses > income:
    advice.append("You're spending more than you earn! Try cutting entertainment expenses.")
if savings < (0.2 * income):
    advice.append("Try saving at least 20% of your income for financial security.")
elif savings > (0.3 * income):
    advice.append("Great job! You're saving more than 30% of your income!")
if crypto > (0.5 * savings):
    advice.append("High crypto investment! Diversify your portfolio.")
if emi > (0.4 * income):
    advice.append("Your EMI is too high! Consider refinancing or paying off loans earlier.")
if emergency_fund < (0.1 * income):
    advice.append("Increase your emergency fund contributions for financial safety.")
elif emergency_fund > (0.2 * income):
    advice.append("Awesome! Your emergency fund is strong!")

for tip in advice:
    with st.expander(f"✔️ {tip}"):
        st.write("Suggested Action: Take steps to optimize your spending and savings!")

# Download Financial Report
st.subheader("📜 Download Your Financial Report")
if st.button("📥 Download Report"):
    report_content = f"""
    Financial Summary Report
    ==========================
    Monthly Income: {currency_symbol}{income}
    Total Expenses: {currency_symbol}{expenses}
    Monthly Net Savings: {currency_symbol}{net_savings}
    Predicted Net Worth in 5 Years: {currency_symbol}{predicted_worth:,.2f}
    Expense Breakdown: {', '.join([f'{l}: {currency_symbol}{v}' for l, v in zip(labels, data) if v > 0])}
    Money Persona: {persona}
    AI Suggestions: {'; '.join(advice) if advice else 'None'}
    """
    st.download_button(label="Download Report as TXT", data=report_content, file_name="financial_report.txt")

st.caption("💬 Compare with friends & improve your financial future! 🚀")
