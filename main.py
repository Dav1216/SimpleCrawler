import os
from datetime import datetime
from dotenv import load_dotenv
import smtplib
import random
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from bs4 import BeautifulSoup
import schedule
import time
from selenium import webdriver
from selenium.common import WebDriverException
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Load environment variables from .env file
load_dotenv('.env')

# Access the variables
smtp_mail = os.getenv("CREATOR_EMAIL")
smtp_password = os.getenv("CREATOR_PASSWORD")
target_1 = os.getenv("TARGET_EMAIL_1")
target_2 = os.getenv("TARGET_EMAIL_2")
server = os.getenv("SMTP_SERVER")
port = os.getenv("SMTP_SERVER_PORT")
my_url = os.getenv("LINK_TO_SCRAPE")
my_subject = os.getenv("SUBJECT")
my_message = os.getenv("MESSAGE")

# Initialize stored listings in memory
stored_listings = None


def fetch_current_listings(url):
    """
    Fetch the current listings from the given URL using Selenium and BeautifulSoup.

    Args:
        url (str): The URL to scrape.

    Returns:
        int: The number of listings found.
    """
    chrome_options = ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")

    # Additional arguments to avoid detection
    chrome_options.add_argument(
        "--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/126.0.0.0 Safari/537.36")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)

    service = ChromeService(executable_path='/usr/bin/chromedriver')
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        driver.get(url)
        driver.maximize_window()

        # Mimic human behavior with a random pause
        initial_pause = random.uniform(0.5, 1.5)
        time.sleep(initial_pause)

        # Wait for the initial elements to load
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, 'list-item')))

        # Randomly scroll down the page to mimic human behavior
        scroll_pause_time = random.uniform(0.5, 2)
        scroll_height = driver.execute_script("return document.body.scrollHeight")
        for _ in range(random.randint(1, 3)):
            try:
                scroll_to = random.randint(5, max(0, scroll_height - 500))
                driver.execute_script(f"window.scrollTo(0, {scroll_to});")
            except WebDriverException as e:
                print(f"Scrolling failed: {e}")
            time.sleep(scroll_pause_time)

        # Get the page source after the page has fully loaded
        html_str = driver.page_source

        # Parse the HTML with BeautifulSoup
        soup = BeautifulSoup(html_str, 'html.parser')

        # Find all <div> elements with IDs starting with 'object-title-'
        section_count = len(soup.find_all('section', class_='list-item ng-scope'))
        # Return the number of listings
        print("number of listings is " + str(section_count))
        return section_count

    finally:
        driver.quit()


def check_new_listings(url):
    """
    Check for new listings by comparing the current listings with stored listings.

    Args:
        url (str): The URL to scrape.

    Returns:
        bool: True if there are new listings, False otherwise.
    """
    global stored_listings
    current_listings = fetch_current_listings(url)
    if current_listings != stored_listings:
        stored_listings = current_listings
        return True
    else:
        stored_listings = current_listings
        return False


def send_email(subject, body, to_email):
    """
    Send an email notification.

    Args:
        subject (str): The subject of the email.
        body (str): The body content of the email.
        to_email (str): The recipient's email address.
    """
    global server
    global port

    msg = MIMEMultipart("alternative")
    msg['Subject'] = subject
    msg['From'] = smtp_mail
    msg['To'] = to_email
    msg.attach(MIMEText(body))

    s = smtplib.SMTP(server, int(port))
    s.starttls()  # Upgrade the connection to TLS
    s.login(smtp_mail, smtp_password)
    s.sendmail(smtp_mail, to_email, msg.as_string())
    s.quit()


def job():
    """
    Job function to be scheduled. Checks for new listings and sends email notifications if there are any.
    """
    print("job is now executing")
    global my_url
    try:
        new_listings = check_new_listings(my_url)
        if new_listings:
            send_email(my_subject, my_message, target_1)
            send_email(my_subject, my_message, target_2)
            print("New listings processed.")
        else:
            print("No new listings found.")
    except Exception as e:
        print(f"An error occurred in job(): {str(e)}")
    finally:
        # Reschedule the jobs
        reschedule_job()


def is_night_time():
    """
    Check if the current time is night time.

    Returns:
        bool: True if it is night time, False otherwise.
    """
    current_hour = datetime.now().hour
    return current_hour >= 22 or current_hour < 6


def reschedule_job():
    """
    Reschedule the job with a random time interval.
    """
    schedule.clear('job')
    interval = random.randint(1, 10)
    schedule.every(interval).minutes.do(job).tag('job')
    print(f"Job rescheduled to run in {interval} minutes.")


# Initial scheduling of the job
reschedule_job()

# Main loop to run the scheduled jobs
while True:
    if not is_night_time():
        time.sleep(1)
        schedule.run_pending()
    else:
        print("It's night time. Skipping checks.")
        # Sleep for a while before the next check
        time.sleep(3600)  # Sleep for 1 hour (3600 seconds)
