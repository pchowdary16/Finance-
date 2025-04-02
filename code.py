import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression

# Streamlit UI
st.title("💰 Rich or Bankrupt? AI Lifestyle Analyzer")
st.subheader("Predict Your Net Worth in 5 Years! 🚀")

# User Inputs
st.sidebar.header("Enter Your Financial Details")
income = st.sidebar.number_input("Monthly Income (₹)", min_value=0, step=1000)
rent = st.sidebar.number_input("Rent/EMI (₹)", min_value=0, step=500)
food = st.sidebar.number_input("Food & Groceries (₹)", min_value=0, step=500)
fun = st.sidebar.number_input("Entertainment (₹)", min_value=0, step=500)
crypto = st.sidebar.number_input("Crypto/Investments (₹)", min_value=0, step=500)
savings = st.sidebar.number_input("Monthly Savings (₹)", min_value=0, step=500)

# Calculate Monthly & Yearly Net Savings
expenses = rent + food + fun
net_savings = income - expenses
net_worth_now = savings * 12  # Current Yearly Savings

def predict_net_worth(years=5):
    # Dummy ML Model (Linear Regression for Simplicity)
    years_array = np.array(range(1, years + 1)).reshape(-1, 1)
    savings_array = np.array([net_worth_now * (1 + 0.08) ** i for i in range(1, years + 1)]).reshape(-1, 1)
    model = LinearRegression()
    model.fit(years_array, savings_array)
    future_net_worth = model.predict(np.array([[years]])).flatten()[0]
    return future_net_worth

predicted_worth = predict_net_worth()

# Display Results
st.subheader("📊 Financial Summary")
col1, col2 = st.columns(2)
col1.metric("Monthly Net Savings", f"₹{net_savings}")
col2.metric("Predicted Net Worth in 5 Years", f"₹{predicted_worth:,.2f}")

# Expense Breakdown Pie Chart
st.subheader("📌 Where Your Money Goes")
fig, ax = plt.subplots()
labels = ["Rent", "Food", "Entertainment"]
data = [rent, food, fun]
ax.pie(data, labels=labels, autopct="%1.1f%%", startangle=140, colors=['#ff9999','#66b3ff','#99ff99'])
st.pyplot(fig)

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

for tip in advice:
    st.write("✔️", tip)

st.caption("💬 Compare with friends & improve your financial future! 🚀")
