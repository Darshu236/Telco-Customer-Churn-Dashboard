import streamlit as st
import pandas as pd
import plotly.express as px

# Set page config
st.set_page_config(
    page_title="Telco Churn Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Telco Customer Churn Dashboard")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("WA_Fn-UseC_-Telco-Customer-Churn.csv")
    df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
    df.dropna(inplace=True)
    return df

df = load_data()

# Sidebar filters
st.sidebar.header("Filter Data")
gender = st.sidebar.multiselect("Gender", options=df["gender"].unique(), default=df["gender"].unique())
contract = st.sidebar.multiselect("Contract Type", options=df["Contract"].unique(), default=df["Contract"].unique())
internet = st.sidebar.multiselect("Internet Service", options=df["InternetService"].unique(), default=df["InternetService"].unique())

# Filtered dataframe
filtered_df = df[
    (df["gender"].isin(gender)) &
    (df["Contract"].isin(contract)) &
    (df["InternetService"].isin(internet))
]

# KPIs
total_customers = len(filtered_df)
churned_customers = filtered_df[filtered_df["Churn"] == "Yes"].shape[0]
churn_rate = churned_customers / total_customers * 100
avg_tenure = filtered_df["tenure"].mean()
avg_monthly_charge = filtered_df["MonthlyCharges"].mean()

# KPIs display
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Customers", total_customers)
col2.metric("Churned Customers", churned_customers)
col3.metric("Churn Rate (%)", f"{churn_rate:.2f}")
col4.metric("Avg. Monthly Charges", f"${avg_monthly_charge:.2f}")

st.markdown("---")

# Visualizations
col1, col2 = st.columns(2)

with col1:
    fig1 = px.histogram(filtered_df, x="Contract", color="Churn", barmode="group",
                        title="Churn by Contract Type", color_discrete_sequence=["green", "red"])
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    fig2 = px.box(filtered_df, x="Churn", y="MonthlyCharges", color="Churn",
                  title="Monthly Charges vs Churn", color_discrete_sequence=["green", "red"])
    st.plotly_chart(fig2, use_container_width=True)

col3, col4 = st.columns(2)

with col3:
    fig3 = px.pie(filtered_df, names='InternetService', title='Internet Service Distribution',
                  color_discrete_sequence=px.colors.sequential.RdBu)
    st.plotly_chart(fig3, use_container_width=True)

with col4:
    fig4 = px.histogram(filtered_df, x="SeniorCitizen", color="Churn",
                        title="Senior Citizen Churn Distribution", barmode="group")
    st.plotly_chart(fig4, use_container_width=True)

st.markdown("---")
st.subheader("💡 Detailed Churn Breakdown Table")
st.dataframe(filtered_df[['customerID', 'gender', 'SeniorCitizen', 'Partner', 'Contract', 'MonthlyCharges', 'Churn']])
