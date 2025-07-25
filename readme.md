# AutoApply: A Python-Powered Job Hunt Assistant

Version 1 – Entry Level but Practical

A personal tool I’m building to take the pain out of job searching. It scrapes job listings, tailors my resume using templates, and logs everything I apply to. This is my attempt to streamline the process and focus on the parts that actually matter like preparing for interviews and continuous upskilling.

---

## What It Does

- Scrapes job ads from selected sites
- Text Preprocessing
- Predict best match
- Fills in a resume and cover letter template automatically for top matching job 
- Logs job applications in a local database
- Auto-fills and submits applications with Selenium
- Sends reminders or updates when there's no response

No LLMs, no APIs, just Python, a bit of HTML scraping, and automation.

---

## Why I’m Building This


Most people miss great job opportunities because:

•	They’re overwhelmed juggling life & work

•	They don’t check job boards daily

•	They can’t tailor resumes fast enough

•	Remote roles disappear quickly

So I built a personal-use tool to help catch rare but fitting job openings especially remote ones.

---

## How It Works 

```text
1. job_scraper/     → Pulls job ads from target boards
2. preprocessor/    → Extract features.
3. job_rank/        → Rank jobs.
4. resume_maker/    → Uses templates and job keywords to generate docs
5. tracker/         → Stores applications in SQLite
6. submitter/       → Automates form submission via Selenium
7. main.py          → Glues everything together

```
---

## Instruction

1. Clone the repo

```

git clone https://github.com/shanurwan/Job-Hunt-Automation.git
cd Job-Hunt-Automation

```

2. Set up python environment 


```

# Create virtual environment (windows)
python -m venv venv
source venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt


```

3. Customize yourself

- job_scraper/remoteok.py = current link monitor analyst job, change to your desired job

- job_rank/jobrank.py = adjust user's skill and interest with yours

- resume_maker/base_resume.txt = adjust with your general resume

- submitter/autoapply.py = adjust with your personal information

---

4. Run the script = 

```
python main.py

```

---

##  Who this could benefit:

•	Parent caretakers who can’t relocate

•	Underserved or remote-region jobseekers

•	Those who can’t afford premium job tools

•	Career switchers with limited time

---
##  Upcoming version 2 upgrade 

- scrape more website






