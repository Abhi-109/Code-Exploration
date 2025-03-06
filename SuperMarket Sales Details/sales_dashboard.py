import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

st.set_page_config(page_title="Supermarket Sales Dashboard", layout="wide")


@st.cache_data
def load_data():
    df = pd.read_csv('supermarket_sales - Sheet1.csv')
    df['Date'] = pd.to_datetime(df['Date']) 
    return df

df = load_data()

# Sidebar for filters
st.sidebar.header("Filters")
branch = st.sidebar.multiselect("Select Branch", options=df['Branch'].unique(), default=df['Branch'].unique())
city = st.sidebar.multiselect("Select City", options=df['City'].unique(), default=df['City'].unique())
customer_type = st.sidebar.multiselect("Select Customer Type", options=df['Customer type'].unique(), default=df['Customer type'].unique())
gender = st.sidebar.multiselect("Select Gender", options=df['Gender'].unique(), default=df['Gender'].unique())

# Apply filters
filtered_df = df[
    (df['Branch'].isin(branch)) &
    (df['City'].isin(city)) &
    (df['Customer type'].isin(customer_type)) &
    (df['Gender'].isin(gender))
]

# Main dashboard title
st.title("Supermarket Sales Dashboard")
st.markdown("Explore sales trends, customer ratings, and product performance across branches.")

# Key Metrics
col1, col2, col3 = st.columns(3)
with col1:
    total_sales = filtered_df['Total'].sum()
    st.metric(label="Total Sales", value=f"${total_sales:,.2f}")
with col2:
    avg_rating = filtered_df['Rating'].mean()
    st.metric(label="Average Rating", value=f"{avg_rating:.2f}")
with col3:
    total_transactions = filtered_df.shape[0]
    st.metric(label="Total Transactions", value=f"{total_transactions:,}")

# Sales and Rating Trends
st.subheader("Sales and Rating Trends Over Time")
col4, col5 = st.columns(2)

# Sales over time
daily_sales = filtered_df.groupby('Date')['Total'].sum().reset_index()
fig_sales = px.line(daily_sales, x='Date', y='Total', title="Daily Sales Trend", 
                    labels={'Total': 'Sales ($)'}, template="plotly_white")
fig_sales.update_traces(line_color='#00cc96')
with col4:
    st.plotly_chart(fig_sales, use_container_width=True)

# Rating over time
daily_ratings = filtered_df.groupby('Date')['Rating'].mean().reset_index()
fig_ratings = px.line(daily_ratings, x='Date', y='Rating', title="Daily Average Rating Trend", 
                      labels={'Rating': 'Average Rating'}, template="plotly_white")
fig_ratings.update_traces(line_color='#ff5733')
with col5:
    st.plotly_chart(fig_ratings, use_container_width=True)

# Sales by Product Line
st.subheader("Sales by Product Line")
product_sales = filtered_df.groupby('Product line')['Total'].sum().reset_index()
fig_product = px.bar(product_sales, x='Product line', y='Total', title="Sales by Product Line", 
                     labels={'Total': 'Sales ($)'}, template="plotly_white", color='Product line')
st.plotly_chart(fig_product, use_container_width=True)

# Payment Method Distribution
st.subheader("Payment Method Distribution")
payment_dist = filtered_df['Payment'].value_counts().reset_index()
payment_dist.columns = ['Payment', 'Count']
fig_payment = px.pie(payment_dist, values='Count', names='Payment', title="Payment Method Distribution",
                     template="plotly_white", color_discrete_sequence=px.colors.sequential.RdBu)
st.plotly_chart(fig_payment, use_container_width=True)


st.subheader("Branch Comparison")
branch_sales = filtered_df.groupby('Branch')['Total'].sum().reset_index()
fig_branch = px.bar(branch_sales, x='Branch', y='Total', title="Sales by Branch", 
                    labels={'Total': 'Sales ($)'}, template="plotly_white", color='Branch')
st.plotly_chart(fig_branch, use_container_width=True)

st.markdown("""
---
**Powered by Streamlit** | Data Source: Supermarket Sales Dataset
""")