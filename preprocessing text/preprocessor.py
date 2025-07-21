import re
from bs4 import BeautifulSoup
import html
import pandas as pd

# Define skill keywords
SKILL_SET = [
    "python", "sql", "excel", "powerbi", "power bi", "tableau", "vba", "dax", 
    "ai", "data", "data analysis", "data analytics", "analytics", "machine learning",
    "pipeline", "etl", "web scraping", "selenium", "data entry", "admin", 
    "aws", "gcp", "azure", "api", "cloud", "linux", "golang", 
    "salesforce", "wordpress", "jira", "scrum", "snowflake", "looker", 
    "dbt", "rstudio", "matplotlib", "pandas", "numpy", "statistical analysis"
]


def clean_html(raw_html: str) -> str:
    try:
        soup = BeautifulSoup(str(raw_html), "html.parser")
        clean_text = soup.get_text(separator=" ")
        return html.unescape(clean_text.encode('latin1').decode('utf-8', errors='ignore'))
    except Exception:
        return str(raw_html)


def extract_skills(text: str, skill_set=SKILL_SET) -> list:
    """Extract matching skills from text"""
    text = str(text).lower()
    found = [skill for skill in skill_set if re.search(rf'\b{re.escape(skill)}\b', text)]
    return list(set(found))

def preprocess_job_row(row: pd.Series) -> dict:
    """Process one job row: clean + extract"""
    desc = row.get("description", "")
    tags = row.get("tags", "")
    cleaned_desc = clean_html(desc)
    combined_text = f"{cleaned_desc} {tags}"
    skills = extract_skills(combined_text)

    return {
        "title": row.get("title", ""),
        "company": row.get("company", ""),
        "location": row.get("location", ""),
        "skills": skills,
        "url": row.get("url", ""),
        "clean_description": cleaned_desc
    }

def preprocess_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Preprocess entire DataFrame"""
    return df.apply(preprocess_job_row, axis=1, result_type="expand")