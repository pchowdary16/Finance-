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

# Financial Inputs
st.sidebar.header("Financial Details")
with st.sidebar.expander("💰 Income & Savings"):
    income = st.number_input("Monthly Income (₹)", min_value=0, step=1000)
    savings = st.number_input("Monthly Savings (₹)", min_value=0, step=500)
    savings_goal = st.number_input("Savings Goal (₹)", min_value=0, step=10000)
    crypto = st.number_input("Crypto/Investments (₹)", min_value=0, step=500)

with st.sidebar.expander("🏠 Fixed Expenses"):
    rent = st.number_input("Rent (₹)", min_value=0, step=500)
    emi = st.number_input("EMI (₹)", min_value=0, step=500)
    emergency_fund = st.number_input("Emergency Fund Contribution (₹)", min_value=0, step=500)

with st.sidebar.expander("🍔 Flexible Expenses"):
    food = st.number_input("Food & Groceries (₹)", min_value=0, step=500)
    fun = st.number_input("Entertainment (₹)", min_value=0, step=500)
    extra_expenses = st.number_input("Extra Expenses (₹)", min_value=0, step=500)
    custom_expense = st.text_input("Custom Expense Name")
    custom_expense_value = st.number_input("Custom Expense (₹)", min_value=0, step=500)

# Extras Section
st.sidebar.subheader("📂 Extras")
st.sidebar.text_area("Additional Notes")
st.sidebar.file_uploader("Upload Financial Data (CSV)")

# Calculate Net Savings
expenses = rent + emi + food + fun + extra_expenses + emergency_fund + custom_expense_value
net_savings = income - expenses
net_worth_now = savings * 12

# Predict Future Net Worth
def predict_net_worth(years=5):
    years_array = np.array(range(1, years + 1)).reshape(-1, 1)
    savings_array = np.array([net_worth_now * (1 + 0.08) ** i for i in range(1, years + 1)]).reshape(-1, 1)
    model = LinearRegression()
    model.fit(years_array, savings_array)
    future_net_worth = model.predict(np.array([[years]])).flatten()[0]
    return future_net_worth

predicted_worth = predict_net_worth()

# Display Results
st.subheader("📊 Financial Summary")
col1, col2, col3 = st.columns(3)
col1.metric("Monthly Net Savings", f"₹{net_savings}")
col2.metric("Predicted Net Worth in 5 Years", f"₹{predicted_worth:,.2f}")
progress = min((net_worth_now / savings_goal) * 100, 100) if savings_goal > 0 else 0
col3.progress(progress / 100)

# Expense Breakdown Pie Chart
st.subheader("📌 Where Your Money Goes")
fig, ax = plt.subplots()
labels = ["Rent", "EMI", "Food", "Entertainment", "Extra Expenses", "Emergency Fund", custom_expense]
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

# Money Persona Badge
st.subheader("🏆 Your Money Persona")
if predicted_worth > 5000000:
    st.success("🔥 Smart Investor! You're on track to be wealthy!")
elif predicted_worth > 1000000:
    st.info("💡 Balanced Saver! Keep up the good work!")
else:
    st.warning("⚠️ YOLO Spender! Consider saving more!")

# AI Money Coach Advice
st.subheader("💡 AI Money Coach Suggestions")
advice = []
if expenses > income:
    advice.append("You're spending more than you earn! Try cutting entertainment expenses.")
if savings < (0.2 * income):
    advice.append("Try saving at least 20% of your income for financial security.")
if crypto > (0.5 * savings):
    advice.append("High crypto investment! Diversify your portfolio.")
if emi > (0.4 * income):
    advice.append("Your EMI is too high! Consider refinancing or paying off loans earlier.")
if emergency_fund < (0.1 * income):
    advice.append("Increase your emergency fund contributions for financial safety.")

for tip in advice:
    with st.expander(f"✔️ {tip}"):
        st.write("Suggested Action: Take steps to optimize your spending and savings!")

# Download Financial Report
st.subheader("📜 Download Your Financial Report")
if st.button("📥 Download Report"):
    report_content = f"""
    Financial Summary Report
    ==========================
    Monthly Net Savings: ₹{net_savings}
    Predicted Net Worth in 5 Years: ₹{predicted_worth:,.2f}
    """
    st.download_button(label="Download Report as TXT", data=report_content, file_name="financial_report.txt")

st.caption("💬 Compare with friends & improve your financial future! 🚀")
