import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

# Load scraped & cleaned data 
df = pd.read_csv("remoteok_jobs_cleaned.csv")

# Preprocess: fillna and clean format 
df["preprocessed_description"] = df["clean_description"].fillna("").astype(str)

# TF-IDF Keyword Extraction
vectorizer = TfidfVectorizer(stop_words="english", max_features=1000)
tfidf_matrix = vectorizer.fit_transform(df["preprocessed_description"])
feature_names = vectorizer.get_feature_names_out()

def get_top_keywords(text, top_n=10):
    vec = vectorizer.transform([text])
    scores = vec.toarray()[0]
    top_indices = scores.argsort()[::-1][:top_n]
    return [feature_names[i] for i in top_indices if scores[i] > 0]

df["top_keywords"] = df["preprocessed_description"].apply(lambda x: get_top_keywords(x))

# Define Skills
user_skills = ["python", "sql", "data analysis", "tableau", "power bi",
               "business", "forecasting", "market research"]

def match_score(keywords, skills):
    return len(set(keywords).intersection(set(skills)))

df["match_score"] = df["top_keywords"].apply(lambda x: match_score(x, user_skills))

# Sort by Match Score & Save 
ranked_jobs = df.sort_values(by="match_score", ascending=False)
ranked_jobs.to_csv("ranked_jobs.csv", index=False)

# Test if it works
# print("Top Matching Jobs:")
# print(ranked_jobs[["title", "company", "match_score", "top_keywords", "job_url"]].head(5))