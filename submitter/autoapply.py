from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from pathlib import Path
import time

def auto_apply_to_job(
    job_url,
    resume_path,
    full_name="John Doe",
    email="JohnDoe@gmail.com",
    phone="0123456789",
    location="Singapore",
    pronouns="He/him",
    linkedin="https://linkedin.com/in/yourprofile"
):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Comment this if you want to watch the browser
    driver = webdriver.Chrome(options=options)

    try:
        driver.get(job_url)
        wait = WebDriverWait(driver, 15)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        time.sleep(2)  # Ensure page is fully rendered

        # Click the 'Submit your application' button
        try:
            submit_btn = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-qa='btn-apply']"))
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", submit_btn)
            time.sleep(1)
            submit_btn.click()
        except Exception as e:
            print("Failed to click 'Submit your application' button")
            print(f"Error: {e}")
            driver.save_screenshot("submit_button_error.png")
            with open("debug_page.html", "w", encoding="utf-8") as f:
                f.write(driver.page_source)
            return

        # Upload resume
        try:
            resume_input = wait.until(
                EC.presence_of_element_located((By.XPATH, "//input[@type='file']"))
            )
            resume_input.send_keys(str(Path(resume_path).resolve()))
        except Exception as e:
            print("Failed to upload resume")
            print(f"Error: {e}")
            return

        # Fill name
        try:
            name_input = driver.find_element(By.XPATH, "//input[@placeholder='Full name']")
            name_input.send_keys(full_name)
        except Exception as e:
            print("Failed to fill name")
            print(f"Error: {e}")
            return

        # Pronouns (optional)
        try:
            pronoun_select = Select(driver.find_element(By.XPATH, "//select[contains(@name,'pronouns')]"))
            pronoun_select.select_by_visible_text(pronouns)
        except:
            pass  # Not all forms require this

        # Email
        try:
            email_input = driver.find_element(By.XPATH, "//input[@placeholder='Email']")
            email_input.send_keys(email)
        except Exception as e:
            print("Failed to fill email")
            print(f"Error: {e}")
            return

        # Phone
        try:
            phone_input = driver.find_element(By.XPATH, "//input[@placeholder='Phone']")
            phone_input.send_keys(phone)
        except Exception as e:
            print("Failed to fill phone")
            print(f"Error: {e}")
            return

        # Current Location (optional)
        try:
            loc_input = driver.find_element(By.XPATH, "//input[contains(@placeholder, 'location')]")
            loc_input.send_keys(location)
        except:
            pass

        # LinkedIn (optional)
        try:
            linkedin_input = driver.find_element(By.XPATH, "//input[contains(@placeholder,'LinkedIn')]")
            linkedin_input.send_keys(linkedin)
        except:
            pass

        # Final submit button
        try:
            final_submit = driver.find_element(By.XPATH, "//button[contains(text(),'Submit')]")
            driver.execute_script("arguments[0].scrollIntoView(true);", final_submit)
            time.sleep(1)
            final_submit.click()
        except Exception as e:
            print("Failed to click final 'Submit' button")
            print(f"Error: {e}")
            return

        print(f"Successfully submitted to: {job_url}")

    except Exception as e:
        print(f" General failure while processing: {job_url}")
        print(f"Error: {e}")

    finally:
        time.sleep(3)
        driver.quit()

