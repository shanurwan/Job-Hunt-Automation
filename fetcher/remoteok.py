# remoteok.py

import requests
import pandas as pd

def fetch_remote_jobs(tag="data+analyst"):
    url = f"https://remoteok.com/api?tags={tag}"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    data = response.json()

    jobs = []
    for job in data:
        if "position" in job:
            jobs.append({
                "company": job.get("company"),
                "position": job.get("position"),
                "location": job.get("location"),
                "url": f"https://remoteok.com{job.get('url')}",
                "tags": ", ".join(job.get("tags", []))
            })

    return pd.DataFrame(jobs)

if __name__ == "__main__":
    df = fetch_remote_jobs()
    print(df.head())
    df.to_csv("remoteok_jobs.csv", index=False)
    print("Saved to remoteok_jobs.csv")
