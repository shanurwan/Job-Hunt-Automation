# AutoApply: A Python-Powered Job Hunt Assistant

A personal tool I’m building to take the pain out of job searching. It scrapes job listings, tailors my resume using templates, and logs everything I apply to .

---

## What It Does

- Scrapes job ads from selected sites
- Text Preprocessing
- Predict best match
- Fills in a resume and cover letter template automatically for job with matching percentage above 85% only
- Logs job applications in a local database
- Auto-fills and submits applications with Selenium
- Sends reminders or updates when there's no response

No LLMs, no APIs, just Python, a bit of HTML scraping, and automation.

---

## Why I’m Building This

This is my attempt to streamline the process and focus on the parts that actually matter like preparing for interviews and continuous upskilling.

Key Takeaway :

🔍 Built as a learning project to study jobseeker behavior, optimize resume targeting, and explore real-world automation ethics.

⚠️ Not a spam bot. Not built for mass blind submissions. This is a **controlled, personal-use tool** focused on workflow automation and learning.

---

## How It Works (Current Plan)

```text
1. job_scraper/     → Pulls job ads from target boards
2. text_preprocessor/  → Extract features.
3. job_rank/ → Rank jobs.
4. resume_maker/    → Uses templates and job keywords to generate docs
5. tracker/         → Stores applications in SQLite
6. submitter/       → Automates form submission via Selenium
7. main.py          → Glues everything together

```
---

## I'm currently occupied with other priority, progress will be really slow and will only speed up starting mid of August

