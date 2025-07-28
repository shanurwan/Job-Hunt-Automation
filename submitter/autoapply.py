from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import os

def auto_apply_to_job(
    job_url,
    resume_path,
    full_name="John Doe",
    email="johndoe@gmail.com",
    phone="0123456789",
    location="Singapore",
    pronouns="He/him",
    linkedin="https://linkedin.com/in/yourprofile"
):
    


    options = Options()

# Use your Chrome profile, 
    options.add_argument(
    r"--user-data-dir=C:\Users\wan\AppData\Local\Google\Chrome\User Data"
)
    options.add_argument("--profile-directory=Default")  

# Optional: show browser during test
    options.add_argument("--headless")  # Comment if you want to see browser
    options.add_argument("--window-size=1280,800")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    driver = webdriver.Chrome(options=options)

    wait = WebDriverWait(driver, 15)

    try:
        print(f"Opening job URL: {job_url}")
        driver.get(job_url)
        time.sleep(2)

        # Step 1: Click the 'Apply' anchor
        try:
            apply_btn = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "a.action-apply"))
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", apply_btn)
            time.sleep(1)
            driver.execute_script("arguments[0].click();", apply_btn)
            print("Clicked 'Apply' to open application form")
        except Exception as e:
            print("Failed to click 'Apply' link")
            print(f"Error: {e}")
            driver.save_screenshot("apply_button_error.png")
            return  # early return ONLY if Apply fails

        # Fill in form fields
        wait.until(EC.presence_of_element_located((By.NAME, "name"))).send_keys(full_name)
        driver.find_element(By.NAME, "email").send_keys(email)
        driver.find_element(By.NAME, "phone").send_keys(phone)

        # Optional fields
        try:
            driver.find_element(By.NAME, "pronouns").send_keys(pronouns)
        except:
            pass
        try:
            driver.find_element(By.NAME, "location").send_keys(location)
        except:
            pass
        try:
            driver.find_element(By.NAME, "linkedin").send_keys(linkedin)
        except:
            pass

        # Upload resume
        file_input = driver.find_element(By.NAME, "resume")
        file_input.send_keys(os.path.abspath(resume_path))
        print("Resume uploaded")

        time.sleep(2)

        # Final submit
        try:
            final_submit = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "#btn-submit"))
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", final_submit)
            time.sleep(1)
            final_submit.click()
            print(" Application submitted!")
        except Exception as e:
            print(" Failed to click final submit button")
            print(f"Error: {e}")
            driver.save_screenshot("final_submit_error.png")
            with open("final_debug_page.html", "w", encoding="utf-8") as f:
                f.write(driver.page_source)

    except Exception as e:
        print(f" Unexpected error: {e}")
    finally:
        driver.quit()

