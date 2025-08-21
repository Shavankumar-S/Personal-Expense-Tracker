import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from expense_tracker import load_expenses, add_expense, get_summary, get_kpis

st.set_page_config(page_title="Personal Expense Tracker", page_icon="💰", layout="wide")

# Title
st.title("💰 Personal Expense Tracker")
st.markdown("Track, analyze, and manage your expenses with ease.")

# Tabs
tab1, tab2, tab3 = st.tabs(["➕ Add Expense", "📋 View Expenses", "📊 Summary & Insights"])

# --- TAB 1: Add Expense ---
with tab1:
    st.subheader("➕ Add New Expense")

    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        date = st.date_input("Date")
    with col2:
        category = st.selectbox("Category", ["Food", "Transport", "Entertainment", "Bills", "Other"])
    with col3:
        amount = st.number_input("Amount", min_value=0.0, format="%.2f")

    description = st.text_area("Description")

    if st.button("💾 Save Expense"):
        add_expense(date, category, amount, description)
        st.success("✅ Expense Added Successfully!")

# --- TAB 2: View Expenses ---
with tab2:
    st.subheader("📋 All Expenses")
    df = load_expenses()

    if not df.empty:
        df["date"] = pd.to_datetime(df["date"])

        # Sidebar filters
        st.sidebar.subheader("🔍 Filter Expenses")
        start_date = st.sidebar.date_input("Start Date", df["date"].min().date())
        end_date = st.sidebar.date_input("End Date", df["date"].max().date())
        category_filter = st.sidebar.multiselect("Category", df["category"].unique(), default=df["category"].unique())
        search_text = st.sidebar.text_input("Search Description")

        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)

        filtered_df = df[
            (df["date"] >= start_date) &
            (df["date"] <= end_date) &
            (df["category"].isin(category_filter)) &
            (df["description"].str.contains(search_text, case=False, na=False))
        ]

        st.dataframe(filtered_df, use_container_width=True)

        # Download option
        csv = filtered_df.to_csv(index=False).encode("utf-8")
        st.download_button("⬇️ Download CSV", data=csv, file_name="expenses.csv", mime="text/csv")
    else:
        st.info("No expenses found. Add your first expense in the **Add Expense** tab.")

# --- TAB 3: Summary & Insights ---
with tab3:
    st.subheader("📊 Expense Summary")
    summary_df = get_summary()
    kpis = get_kpis()

    # KPIs
    col1, col2, col3 = st.columns(3)
    col1.metric("💵 Total Spent", f"₹{kpis['total']:.2f}")
    col2.metric("📊 Avg Expense", f"₹{kpis['average']:.2f}")
    col3.metric("🔥 Biggest Expense", f"₹{kpis['max']:.2f}")

    if not summary_df.empty:
        col1, col2 = st.columns([2, 2])

        # Pie chart
        with col1:
            fig, ax = plt.subplots()
            ax.pie(summary_df['Amount'], labels=summary_df['Category'], autopct='%1.1f%%')
            ax.set_title("Expenses by Category")
            st.pyplot(fig)

        # Bar chart
        with col2:
            st.bar_chart(summary_df.set_index("Category")["Amount"])

        # Monthly trend
        st.markdown("### 📈 Monthly Spending Trend")
        df["Month"] = pd.to_datetime(df["date"]).dt.to_period("M")
        monthly_summary = df.groupby("Month")["amount"].sum().reset_index()
        monthly_summary["Month"] = monthly_summary["Month"].astype(str)
        st.line_chart(monthly_summary.set_index("Month")["amount"])

        # Budget Tracker
        st.markdown("### 🎯 Budget Tracker")
        budget = st.number_input("Set Monthly Budget (₹)", min_value=0.0, format="%.2f", value=5000.0)
        total_spent = kpis["total"]

        if total_spent > budget:
            st.error(f"⚠️ You have exceeded your budget by ₹{total_spent - budget:.2f}!")
        else:
            st.success(f"✅ You are within your budget. Remaining: ₹{budget - total_spent:.2f}")
    else:
        st.info("No data available for summary. Add some expenses first!")
