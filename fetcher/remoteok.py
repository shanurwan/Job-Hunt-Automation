import requests
import pandas as pd

def scrape_analyst_jobs_only():
    url = "https://remoteok.com/api"
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(url, headers=headers)
    data = response.json()

    jobs = []
    for job in data[1:]:  # First item is metadata
        tags = job.get("tags", [])
        position = job.get("position", "").lower()

        # Filter to jobs with 'analyst' in title or tags
        if "analyst" in position or any("analyst" in tag.lower() for tag in tags):
            slug = job.get("slug")
            full_url = f"https://remoteok.com/remote-jobs/{slug}" if slug else None

            jobs.append({
                "title": job.get("position"),
                "company": job.get("company"),
                "location": job.get("location"),
                "tags": ', '.join(tags),
                "url": full_url,
                "description": job.get("description", "")  # full description now
            })

    df = pd.DataFrame(jobs)
    df.to_csv("remoteok_analyst_jobs.csv", index=False)
    print(f" Saved {len(df)} analyst jobs to remoteok_analyst_jobs.csv")

if __name__ == "__main__":
    scrape_analyst_jobs_only()
