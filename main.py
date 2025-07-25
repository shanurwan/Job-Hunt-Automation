from pathlib import Path
import pandas as pd

# 1. SCRAPER
from job_scraper.scraper import scrape_jobs
df = scrape_jobs(query="data analyst", num_jobs=20)

# Output folder
data_dir = Path("data")
data_dir.mkdir(exist_ok=True)
scraped_path = data_dir / "remoteok_analyst_jobs.csv"
df.to_csv(scraped_path, index=False)
print(f" Scraped jobs saved to: {scraped_path}")

# 2. PREPROCESSOR
from preprocessor.cleaner import clean_description
from preprocessor.pipeline import preprocess

df["clean_description"] = df["description"].apply(clean_description)
df["preprocessed_description"] = df["clean_description"].apply(preprocess)

cleaned_path = data_dir / "remoteok_jobs_cleaned.csv"
df.to_csv(cleaned_path, index=False)
print(f" Cleaned data saved to: {cleaned_path}")

# 3. JOB RANKING
from job_rank.rank import rank_jobs
ranked_df = rank_jobs(cleaned_path)

ranked_path = data_dir / "ranked_jobs.csv"
ranked_df.to_csv(ranked_path, index=False)
print(f" Ranked jobs saved to: {ranked_path}")

# 4. RESUME GENERATION
from resume_maker.maker import generate_resume
resume_dir = Path("resumes")
resume_dir.mkdir(exist_ok=True)

template = Path("resume_maker/base_resume.txt").read_text()
top_jobs = ranked_df.head(5)

for _, row in top_jobs.iterrows():
    resume_path = generate_resume(row, template, resume_dir)
    print(f" Resume generated: {resume_path}")

# 5. SUBMISSION (will update after Submitter module ready)
# from submitter.submit import auto_apply_to_job
# for _, row in top_jobs.iterrows():
#     pdf_path = resume_dir / generate_resume_filename(row)
#     auto_apply_to_job(row["job_url"], pdf_path)

#  TRACKER
from tracker.tracker import init_db, log_application
init_db()

for _, row in top_jobs.iterrows():
    resume_path = f"resumes/{row['title'].replace(' ', '_')}-{row['company'].replace(' ', '_')}.pdf"
    log_application(
        job_title=row["title"],
        company=row["company"],
        job_url=row["job_url"],
        resume_file=resume_path,
        status="RESUME_READY"
    )

print(" Done.")
