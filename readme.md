# job-hunt-automation

A personal tool I’m building to take the pain out of job searching. It scrapes job listings, tailors my resume using templates, and logs everything I apply to .

---

## What It Does

- Scrapes job ads from selected sites
- Matches keywords between job ad and resume
- Fills in a resume and cover letter template automatically
- Logs job applications in a local database
- Auto-fills and submits applications with Selenium
- Sends reminders or updates when there's no response

No LLMs, no APIs, just Python, a bit of HTML scraping, and automation.

---

## Why I’m Building This

This is my attempt to streamline the process and focus on the parts that actually matter like preparing for interviews and continuous upskilling.

---

## How It Works (Current Plan)

```text
1. job_scraper/     → Pulls job ads from target boards
2. resume_maker/    → Uses templates and job keywords to generate docs
3. tracker/         → Stores applications in SQLite
4. submitter/       → (Coming soon) Automates form submission via Selenium
5. main.py          → Glues everything together

```
---

## I'm currently occupied with other stuff, progress will be really slow and will only speed up starting end of August

