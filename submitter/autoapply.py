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

# 5. SUBMITTER (Now Active)
from submitter.submit import auto_apply_to_job

for _, row in top_jobs.iterrows():
    resume_filename = f"{row['title'].replace(' ', '_')}-{row['company'].replace(' ', '_')}.pdf"
    resume_path = resume_dir / resume_filename
    try:
        auto_apply_to_job(
            job_url=row["job_url"],
            resume_path=resume_path,
            full_name="Your Name",
            email="you@example.com",
            phone="0123456789",
            location="Malaysia",
            pronouns="He/him",
            linkedin="https://linkedin.com/in/yourprofile"
        )
    except Exception as e:
        print(f"Failed to submit for job at {row['company']}: {e}")

# 6. TRACKER
from tracker.tracker import init_db, log_application
init_db()

for _, row in top_jobs.iterrows():
    resume_filename = f"{row['title'].replace(' ', '_')}-{row['company'].replace(' ', '_')}.pdf"
    resume_path = f"resumes/{resume_filename}"
    log_application(
        job_title=row["title"],
        company=row["company"],
        job_url=row["job_url"],
        resume_file=resume_path,
        status="SUBMITTED"
    )

print("  Done.")
