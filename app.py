import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Page config
st.set_page_config(page_title="Sri Lanka Tourism Analysis", page_icon="🇱🇰", layout="wide")

# Title
st.title("🇱🇰 Sri Lanka Tourism Analysis Dashboard")
st.markdown("**Analyzing 24 years of tourism trends (2000–2023)**")
st.markdown("---")

# Load data
@st.cache_data
def load_data():
    data = {
        "year": list(range(2000, 2024)),
        "total_arrivals": [400000, 436000, 393000, 500000, 566000, 549000, 559000,
                           494000, 438000, 448000, 654000, 856000, 1006000, 1275000,
                           1527000, 1798000, 2051000, 2116000, 2334000, 1913000,
                           507000, 194000, 719000, 1500000],
        "revenue_usd_million": [247, 272, 259, 320, 380, 385, 411, 384, 318, 350,
                                 576, 830, 1039, 1360, 1629, 1921, 2238, 2270, 2564,
                                 2021, 682, 438, 1335, 2100],
        "avg_stay_days": [9.2, 9.5, 9.1, 9.8, 10.2, 10.0, 10.3, 9.9, 9.5, 9.7,
                          10.5, 11.2, 11.8, 12.1, 12.5, 12.8, 13.0, 12.9, 13.2,
                          12.8, 10.5, 8.9, 11.5, 12.8],
        "india_arrivals": [56000, 62000, 58000, 71000, 82000, 80000, 85000, 76000,
                           68000, 72000, 113000, 161000, 195000, 263000, 329000,
                           394000, 473000, 455000, 503000, 424000, 105000, 39000,
                           158000, 350000],
        "uk_arrivals": [52000, 55000, 51000, 62000, 68000, 66000, 69000, 63000,
                        57000, 61000, 82000, 98000, 114000, 138000, 159000, 178000,
                        195000, 198000, 212000, 176000, 48000, 18000, 65000, 140000],
        "germany_arrivals": [28000, 31000, 29000, 35000, 40000, 38000, 41000, 37000,
                              33000, 36000, 51000, 65000, 78000, 95000, 112000, 128000,
                              143000, 148000, 159000, 131000, 35000, 13000, 48000, 100000],
        "china_arrivals": [5000, 6000, 5500, 7000, 9000, 8500, 10000, 9000, 8000,
                           9500, 15000, 22000, 35000, 55000, 80000, 115000, 158000,
                           178000, 195000, 145000, 28000, 10000, 38000, 95000],
        "season": ["low", "high", "low", "high", "high", "high", "high", "low",
                   "low", "low", "high", "high", "high", "high", "high", "high",
                   "high", "high", "high", "high", "low", "low", "high", "high"]
    }
    df = pd.DataFrame(data)
    df["revenue_per_tourist"] = (df["revenue_usd_million"] * 1000000) / df["total_arrivals"]
    df["revenue_per_tourist"] = df["revenue_per_tourist"].round(2)
    return df

df = load_data()

# Sidebar filters
st.sidebar.header(" Filters")
season_filter = st.sidebar.selectbox("Select Season", ["All", "high", "low"])
year_range = st.sidebar.slider("Select Year Range", 2000, 2023, (2000, 2023))

# Apply filters
filtered_df = df[(df["year"] >= year_range[0]) & (df["year"] <= year_range[1])]
if season_filter != "All":
    filtered_df = filtered_df[filtered_df["season"] == season_filter]

# KPI Cards
st.subheader(" Key Statistics")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Arrivals", f"{filtered_df['total_arrivals'].sum():,}")
col2.metric("Total Revenue", f"${filtered_df['revenue_usd_million'].sum():,}M")
col3.metric("Avg Stay Days", f"{filtered_df['avg_stay_days'].mean():.1f} days")
col4.metric("Peak Year", f"{filtered_df.loc[filtered_df['total_arrivals'].idxmax(), 'year']}")

st.markdown("---")

# Charts
col_left, col_right = st.columns(2)

with col_left:
    st.subheader(" Tourist Arrivals Over Time")
    fig1, ax1 = plt.subplots(figsize=(8, 4))
    ax1.plot(filtered_df["year"], filtered_df["total_arrivals"], marker="o", color="steelblue", linewidth=2)
    ax1.fill_between(filtered_df["year"], filtered_df["total_arrivals"], alpha=0.2, color="steelblue")
    ax1.set_xlabel("Year")
    ax1.set_ylabel("Arrivals")
    st.pyplot(fig1)

with col_right:
    st.subheader(" Revenue Over Time")
    fig2, ax2 = plt.subplots(figsize=(8, 4))
    ax2.bar(filtered_df["year"], filtered_df["revenue_usd_million"], color="coral", alpha=0.8)
    ax2.set_xlabel("Year")
    ax2.set_ylabel("Revenue (USD Million)")
    st.pyplot(fig2)

col_left2, col_right2 = st.columns(2)

with col_left2:
    st.subheader(" Arrivals by Country")
    fig3, ax3 = plt.subplots(figsize=(8, 4))
    ax3.plot(filtered_df["year"], filtered_df["india_arrivals"], marker="o", label="India", linewidth=2)
    ax3.plot(filtered_df["year"], filtered_df["uk_arrivals"], marker="s", label="UK", linewidth=2)
    ax3.plot(filtered_df["year"], filtered_df["germany_arrivals"], marker="^", label="Germany", linewidth=2)
    ax3.plot(filtered_df["year"], filtered_df["china_arrivals"], marker="D", label="China", linewidth=2)
    ax3.set_xlabel("Year")
    ax3.set_ylabel("Arrivals")
    ax3.legend()
    st.pyplot(fig3)

with col_right2:
    st.subheader("Revenue Per Tourist")
    fig4, ax4 = plt.subplots(figsize=(8, 4))
    ax4.plot(filtered_df["year"], filtered_df["revenue_per_tourist"], marker="o", color="green", linewidth=2)
    ax4.fill_between(filtered_df["year"], filtered_df["revenue_per_tourist"], alpha=0.2, color="green")
    ax4.set_xlabel("Year")
    ax4.set_ylabel("USD per Tourist")
    st.pyplot(fig4)

st.markdown("---")
st.markdown(" Built by Vaishavi | BSc IT (Data Science) | SLIIT")
