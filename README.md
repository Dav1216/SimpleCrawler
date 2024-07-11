# SimpleCrawler

I made this Housing Bot as the housing market in the Netherlands is very competitive especially for students and I needed a fast way to start getting the necessary notifications when a new listing is published on a specific website. This is a web crawler designed to scrape housing listings from a specified URL, check for new listings, and send email notifications to two specified recipients.

## Features
- Scrapes housing listings from a specified URL.
- Checks for new listings and compares them with previously stored listings.
- Sends email notifications to specified recipients if new listings are found.
- Schedules the scraping job to run at random intervals during the day.
- Avoids running during specified night hours to minimize detection and avoid unnecessary checks.

## Prerequisites
- Docker
- Environment variables set in a `.env` file

## Environment Variables
Create a `.env` file in the project root directory with the following content:
CREATOR_EMAIL=your_email@example.com
CREATOR_PASSWORD=your_email_password
TARGET_EMAIL_1=target_email1@example.com
TARGET_EMAIL_2=target_email2@example.com
SMTP_SERVER=smtp.example.com
SMTP_SERVER_PORT=587
LINK_TO_SCRAPE=https://example.com/housing
SUBJECT="New Housing Listings Available"
MESSAGE="There are new housing listings available. Check them out!"
WAIT_FOR_ITEM="list-item"
WHAT_TO_FIND="section"
WHAT_CLASS_TO_FIND="list-item my-list-scope"


## Installation
### Using Docker

1. **Build the Docker image:**

   ```bash
   docker build -t housing-bot-alpine .
   ```

2. **Run the Docker container:**
    ```bash
    docker run -it housing-bot-alpine
    ```

## Scheduling

The script schedules the scraping job to run at random intervals during the day. It avoids running during specified night hours to minimize detection and avoid unnecessary checks.

## How It Works

* Web Scraping: The script uses Selenium to load the specified URL and mimics human behavior to avoid detection.
* HTML Parsing: BeautifulSoup is used to parse the HTML and extract the number of listings.
* Checking for New Listings: The script compares the current listings with previously stored listings to detect changes.
* Email Notifications: If new listings are found, the script sends email notifications to the specified recipients.
* Job Scheduling: The job is scheduled to run at random intervals during the day and avoids running during night hours.

