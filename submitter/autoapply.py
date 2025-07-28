import os
import time
import logging
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

# Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

def apply_to_job(job_url, resume_path, full_name, email, phone, location, pronouns, linkedin, chrome_user_dir, chrome_profile_dir):
    options = Options()
    options.add_argument(f"--user-data-dir={chrome_user_dir}")
    options.add_argument(f"--profile-directory={chrome_profile_dir}")
    options.add_argument("--window-size=1280,800")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 15)

    try:
        logging.info(f"Opening job URL: {job_url}")
        driver.get(job_url)
        time.sleep(2)

        # Click Apply button
        try:
            apply_btn = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "a.action-apply")))
            driver.execute_script("arguments[0].scrollIntoView(true);", apply_btn)
            time.sleep(1)
            driver.execute_script("arguments[0].click();", apply_btn)
            logging.info("Clicked 'Apply'")
        except Exception as e:
            logging.warning(f"Couldn't click 'Apply': {e}")
            driver.save_screenshot("apply_button_error.png")
            return

        # Fill form
        wait.until(EC.presence_of_element_located((By.NAME, "name"))).send_keys(full_name)
        driver.find_element(By.NAME, "email").send_keys(email)
        driver.find_element(By.NAME, "phone").send_keys(phone)

        # Optional
        for field, value in {"pronouns": pronouns, "location": location, "linkedin": linkedin}.items():
            try:
                driver.find_element(By.NAME, field).send_keys(value)
            except:
                pass

        # Upload resume
        file_input = driver.find_element(By.NAME, "resume")
        file_input.send_keys(os.path.abspath(resume_path))
        logging.info("Uploaded resume")

        time.sleep(2)

        # Final submit
        try:
            final_submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#btn-submit")))
            driver.execute_script("arguments[0].scrollIntoView(true);", final_submit)
            time.sleep(1)
            final_submit.click()
            logging.info("✅ Submitted application")
        except Exception as e:
            logging.error("Failed final submit")
            driver.save_screenshot("final_submit_error.png")
            with open("final_debug_page.html", "w", encoding="utf-8") as f:
                f.write(driver.page_source)

    except Exception as e:
        logging.critical(f"Unexpected error: {e}")
    finally:
        driver.quit()


def autoapply_batch(csv_path="top_jobs.csv"):
    resume_path = os.environ["RESUME_PATH"]
    full_name = os.environ.get("FULL_NAME", "John Doe")
    email = os.environ["EMAIL"]
    phone = os.environ["PHONE"]
    location = os.environ.get("LOCATION", "Singapore")
    pronouns = os.environ.get("PRONOUNS", "He/him")
    linkedin = os.environ.get("LINKEDIN", "")
    chrome_user_dir = os.environ["CHROME_USER_DATA"]
    chrome_profile_dir = os.environ.get("CHROME_PROFILE_DIR", "Default")

    df = pd.read_csv(csv_path)

    for i, row in df.iterrows():
        job_url = row.get("job_url")
        if job_url:
            logging.info(f"--- Applying to: {row['title']} at {row['company']} ---")
            apply_to_job(job_url, resume_path, full_name, email, phone, location, pronouns, linkedin, chrome_user_dir, chrome_profile_dir)
            time.sleep(5)  # optional: to avoid being flagged for rapid submissions


if __name__ == "__main__":
    autoapply_batch()

