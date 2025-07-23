import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

def scrape_remoteok():
    url = "https://remoteok.com/remote-analyst-jobs"
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    jobs = []

    # Loop through all job rows (rows with data-id attribute are real jobs)
    for row in soup.select("tr.job[data-id]"):
        try:
            title = row.find("h2").text.strip()
            company = row.find("h3").text.strip()
            tags = [tag.text.strip() for tag in row.select("div.tags > h3")]
            date_posted = row.find("time")["datetime"]
            job_url = "https://remoteok.com" + row["data-href"]

            # Fetch job description
            job_resp = requests.get(job_url, headers=headers)
            job_soup = BeautifulSoup(job_resp.text, "html.parser")
            desc_div = job_soup.find("div", {"class": "description"})
            description = desc_div.decode_contents().strip() if desc_div else "N/A"

            jobs.append({
                "title": title,
                "company": company,
                "tags": tags,
                "date_posted": date_posted,
                "job_url": job_url,
                "description": description
            })

            print(f"Scraped: {title}")
            time.sleep(1)  # Respect crawl-delay
        except Exception as e:
            print(f" Error scraping job row: {e}")

    df = pd.DataFrame(jobs)
    df.to_csv("remoteok_analyst_jobs.csv", index=False)
    print(f"✅ Saved {len(df)} analyst jobs to remoteok_analyst_jobs.csv")

if __name__ == "__main__":
    scrape_analyst_jobs_only()