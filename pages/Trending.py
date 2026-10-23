import streamlit as st
import pandas as pd
import random

st.metric(
    "🔥 Trending Articles",
    "20"
)

st.title("🔥 Trending News")

try:

    news = pd.read_csv("news_small.csv")

    st.success(f"Loaded {len(news):,} articles")

    # Create fake view counts
    news["views"] = [
        random.randint(1000, 100000)
        for _ in range(len(news))
    ]

    trending = (
        news
        .sort_values(
            by="views",
            ascending=False
        )
        .head(20)
    )

    st.subheader("🏆 Top 20 Trending Articles")

    for _, row in trending.iterrows():

        st.markdown(f"""
### 📰 {row['title']}

🏷️ **Category:** {row['category']}

📈 **Views:** {row['views']:,}

📄 {row['description']}

---
""")

except Exception as e:

    st.error(f"Error: {e}")
