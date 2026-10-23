from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import random


def recommend_news(news_df, user_interest):

    # Create a copy
    news_df = news_df.copy()

    # Handle missing values
    news_df["title"] = (
        news_df["title"]
        .fillna("")
        .astype(str)
    )

    news_df["description"] = (
        news_df["description"]
        .fillna("")
        .astype(str)
    )

    # Combine title and description
    news_df["content"] = (
        news_df["title"]
        + " "
        + news_df["description"]
    )

    # Remove empty rows
    news_df = news_df[
        news_df["content"].str.strip() != ""
    ]

    # Use sample for faster performance
    news_df = news_df.sample(
        min(20000, len(news_df)),
        random_state=42
    )

    # TF-IDF Vectorization
    vectorizer = TfidfVectorizer(
        stop_words="english",
        max_features=5000
    )

    tfidf_matrix = vectorizer.fit_transform(
        news_df["content"]
    )

    # Convert user interest to vector
    user_vector = vectorizer.transform(
        [user_interest]
    )

    # Calculate similarity
    similarity = cosine_similarity(
        user_vector,
        tfidf_matrix
    )

    news_df["similarity_score"] = similarity[0]

    # Generate popularity score
    news_df["views"] = [
        random.randint(1000, 50000)
        for _ in range(len(news_df))
    ]

    news_df["popularity_score"] = (
        news_df["views"]
        / news_df["views"].max()
    )

    # Ranking formula
    news_df["rank_score"] = (
        0.8 * news_df["similarity_score"]
        +
        0.2 * news_df["popularity_score"]
    )

    # Sort results
    recommendations = news_df.sort_values(
        by="rank_score",
        ascending=False
    )

    return recommendations
    st.info(
       f"Recommended because it matches your interest '{interest}'."
)