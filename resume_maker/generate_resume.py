import pandas as pd
from pathlib import Path

def generate_resume(job_row, base_resume_text, output_dir):
    
    job_title = job_row["title"]
    company = job_row["company"]
    keywords = job_row["top_keywords"]
    match_score = job_row["match_score"]

    # Insert dynamic skills section
    skills_section = "Key Skills:\n" + "\n".join(f"- {kw}" for kw in keywords)

    customized_resume = base_resume_text.replace("{{skills_section}}", skills_section)
    customized_resume = customized_resume.replace("{{job_title}}", job_title)
    customized_resume = customized_resume.replace("{{company}}", company)

    # Save to output file
    safe_title = job_title.lower().replace(" ", "_").replace("/", "-")
    filename = f"{safe_title}_{company.lower().replace(' ', '_')}.txt"
    filepath = Path(output_dir) / filename
    filepath.write_text(customized_resume)

    return str(filepath)