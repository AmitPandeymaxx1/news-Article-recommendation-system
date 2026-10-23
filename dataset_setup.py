import pandas as pd

print("Loading dataset...")

df = pd.read_json(
    "News_Category_Dataset_v3.json",
    lines=True
)

print("Original Shape:", df.shape)

# Keep only needed columns
df = df[
    [
        "headline",
        "category",
        "short_description"
    ]
]

# Rename columns
df.rename(
    columns={
        "headline": "title",
        "short_description": "description"
    },
    inplace=True
)

# Remove empty rows
df.dropna(inplace=True)

# Remove duplicates
df.drop_duplicates(inplace=True)

print("Cleaned Shape:", df.shape)

# Save CSV
df.to_csv(
    "news.csv",
    index=False
)

print("✅ news.csv created successfully")
print(df.head())