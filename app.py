import streamlit as st
import pandas as pd
from recommendation import recommend_news

# -------------------------
# PAGE CONFIG
# -------------------------

st.markdown("""
<style>

/* App Background */
.stApp {
    background: linear-gradient(135deg, #0f172a, #1e293b);
}

/* News Cards */
.news-card {
    background: linear-gradient(135deg, #2563eb, #7c3aed);
    padding: 20px;
    border-radius: 15px;
    margin-bottom: 15px;
    color: white;
}

/* Metrics */
[data-testid="metric-container"] {
    background: linear-gradient(135deg,#1d4ed8,#7c3aed);
    padding: 15px;
    border-radius: 12px;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(90deg,#3b82f6,#8b5cf6);
    color: white;
    border-radius: 10px;
    border: none;
}

/* Inputs */
.stTextInput input {
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)

# -------------------------
# LOAD DATA
# -------------------------

@st.cache_data
def load_data():
    return pd.read_csv("news.csv")

news = load_data()

# -------------------------
# SIDEBAR
# -------------------------

st.sidebar.title("🔥 Trending News")

for _, row in news.head(5).iterrows():
    st.sidebar.write("•", row["title"])

st.sidebar.divider()

st.sidebar.subheader("🕒 Recent Searches")

try:
    with open("history.txt", "r") as f:

        searches = f.readlines()

        for item in searches[-5:]:
            st.sidebar.write(item.strip())

except:
    st.sidebar.write("No searches yet")

# -------------------------
# HEADER
# -------------------------

st.markdown("""
<h1 style='text-align:center;color:#60a5fa'>
📰 AI News Recommendation System
</h1>
""", unsafe_allow_html=True)

st.info(
    "🚀 Explore more than 209,000 news articles and get personalized recommendations."
)

# -------------------------
# METRICS
# -------------------------

col1, col2, col3, col4 = st.columns(4)

col1.metric("📰 Articles", f"{len(news):,}")
col2.metric("📂 Categories", news["category"].nunique())
col3.metric("🤖 Engine", "TF-IDF")
col4.metric("📊 Dataset", "Kaggle")

st.divider()

# -------------------------
# SEARCH
# -------------------------

st.subheader("🔍 Search News")

search = st.text_input(
    "Search any news title"
)

if search:

    results = news[
        news["title"].str.contains(
            search,
            case=False,
            na=False
        )
    ]

    st.success(
        f"{len(results)} Result(s) Found"
    )

    for _, row in results.head(10).iterrows():

        st.markdown(f"""
<div class="news-card">

<h3>📰 {row['title']}</h3>

<b>🏷 Category:</b> {row['category']}

<br><br>

{row['description']}

<br><br>

⭐ Similarity Score:
<b>{row['similarity_score']:.4f}</b>

<br>

🔥 Rank Score:
<b>{row['rank_score']:.4f}</b>

</div>
""", unsafe_allow_html=True)

st.divider()

# -------------------------
# RECOMMENDATION
# -------------------------

st.subheader("🎯 News Recommendation")

col1, col2 = st.columns(2)

with col1:

    interest = st.text_input(
        "Enter Your Interest",
        placeholder="Politics, AI, Sports..."
    )

with col2:

    category = st.selectbox(
        "Choose Category",
        ["All"] + list(news["category"].unique())
    )

if st.button("🚀 Recommend News"):

    if interest:

        with open("history.txt", "a") as f:
            f.write(interest + "\n")

        recommendations = recommend_news(
            news,
            interest
        )

        if category != "All":

            recommendations = recommendations[
                recommendations["category"] == category
            ]

        st.subheader("📰 Recommended Articles")

        for _, row in recommendations.head(10).iterrows():

            st.markdown(f"""
### 📰 {row['title']}

🏷️ **Category:** {row['category']}

📄 {row['description']}

⭐ **Similarity Score:** {row['similarity_score']:.4f}

🔥 **Rank Score:** {row['rank_score']:.4f}

---
""")

    else:

        st.warning(
            "Please enter an interest first."
        )

# -------------------------
# CATEGORY CHART
# -------------------------

st.divider()

st.subheader("📊 News Category Distribution")

st.bar_chart(
    news["category"].value_counts()
)

# -------------------------
# DATASET SAMPLE
# -------------------------

with st.expander("📂 View Dataset Sample"):

    st.dataframe(
        news.head(20),
        use_container_width=True
    )