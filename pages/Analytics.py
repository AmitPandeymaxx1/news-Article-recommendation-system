import streamlit as st
import pandas as pd
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import plotly.express as px

# -----------------------------
# Page Title
# -----------------------------

st.title("📊 Analytics Dashboard")

# -----------------------------
# Load Data
# -----------------------------

news = pd.read_csv("news_small.csv")

# Safety Fixes
news["title"] = news["title"].fillna("").astype(str)
news["description"] = news["description"].fillna("").astype(str)

# -----------------------------
# Metrics
# -----------------------------

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "📰 Total Articles",
        f"{len(news):,}"
    )

with col2:
    st.metric(
        "📂 Categories",
        news["category"].nunique()
    )

# -----------------------------
# Category Distribution
# -----------------------------

st.subheader("📈 Category Distribution")

category_count = news["category"].value_counts()

st.bar_chart(category_count)

# -----------------------------
# Top Categories
# -----------------------------

top_category = news["category"].value_counts().idxmax()

st.metric(
    "🏆 Top Category",
    top_category
)

# -----------------------------
# Word Cloud
# -----------------------------

st.subheader("☁️ News Word Cloud")

# Use sample for faster processing
sample_news = news.sample(
    min(5000, len(news)),
    random_state=42
)

text = " ".join(
    sample_news["title"]
    + " "
    + sample_news["description"]
)

if len(text.strip()) > 0:

    wordcloud = WordCloud(
        width=1200,
        height=600,
        background_color="white",
        max_words=200,
        colormap="viridis"
    ).generate(text)

    fig, ax = plt.subplots(
        figsize=(15, 8)
    )

    ax.imshow(
        wordcloud,
        interpolation="bilinear"
    )

    ax.axis("off")

    st.pyplot(fig)

else:
    st.error(
        "No text available for word cloud."
    )

# -----------------------------
# Dataset Preview
# -----------------------------

with st.expander("📂 View Dataset Sample"):

    st.dataframe(
        news.head(20),
        use_container_width=True
    )
from wordcloud import WordCloud, STOPWORDS

custom_stopwords = set(STOPWORDS)

custom_stopwords.update([
    "news",
    "said",
    "say",
    "one",
    "will",
    "new",
    "time",
    "year",
    "day",
    "week",
    "people"
])

wordcloud = WordCloud(
    width=1200,
    height=600,
    background_color="white",
    stopwords=custom_stopwords,
    max_words=150,
    colormap="viridis"
).generate(text)
st.subheader("🥧 Category Distribution Pie Chart")

category_count = (
    news["category"]
    .value_counts()
    .reset_index()
)

category_count.columns = [
    "category",
    "count"
]

fig = px.pie(
    category_count.head(10),
    values="count",
    names="category",
    title="Top 10 News Categories",
    hole=0.4
)

fig.update_traces(
    textposition="inside",
    textinfo="percent+label"
)
# -----------------------------
# Pie Chart
# -----------------------------

st.subheader("🥧 Category Distribution Pie Chart")

category_df = (
    news["category"]
    .value_counts()
    .reset_index()
)

category_df.columns = [
    "category",
    "count"
]

fig = px.pie(
    category_df.head(10),
    values="count",
    names="category",
    hole=0.5,
    color_discrete_sequence=px.colors.qualitative.Set3
)

fig.update_traces(
    textposition="inside",
    textinfo="percent+label"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# -----------------------------
# Word Cloud
# -----------------------------

st.subheader("☁️ News Word Cloud")

from wordcloud import STOPWORDS

custom_stopwords = set(STOPWORDS)

custom_stopwords.update([
    "news",
    "said",
    "say",
    "one",
    "will",
    "new",
    "time",
    "year",
    "day",
    "week",
    "people"
])

sample_news = news.sample(
    min(5000, len(news)),
    random_state=42
)

text = " ".join(
    sample_news["title"]
    + " "
    + sample_news["description"]
)

wordcloud = WordCloud(
    width=1200,
    height=600,
    background_color="white",
    stopwords=custom_stopwords,
    max_words=150,
    colormap="viridis"
).generate(text)

fig_wc, ax = plt.subplots(
    figsize=(14, 7)
)

ax.imshow(
    wordcloud,
    interpolation="bilinear"
)

ax.axis("off")

st.pyplot(fig_wc)
