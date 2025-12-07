from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
import pandas as pd
import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
import config_general


class ChromeDriver:
    def __init__(self):
        opts = Options()
        opts.add_argument("--no-sandbox")
        opts.add_argument("--disable-dev-shm-usage")
        opts.add_argument("--disable-blink-features=AutomationControlled")
        
        self.driver = webdriver.Chrome(service=Service(), options=opts)
    
    def get(self):
        return self.driver
    
    def quit(self):
        self.driver.quit()


class JobLinkScraper:
    def __init__(self, driver, wait_timeout=10, sleep_time=3):
        self.driver = driver
        self.wait_timeout = wait_timeout
        self.sleep_time = sleep_time
        self.job_counter = 1
    
    def scrape_page(self, url):
        print(f"Scraping: {url}")
        self.driver.get(url)
        time.sleep(self.sleep_time)
        
        try:
            WebDriverWait(self.driver, self.wait_timeout).until(
                EC.presence_of_all_elements_located(
                    (By.XPATH, config_general.JOB_POST_XPATH)
                )
            )
            
            posts = self.driver.find_elements(By.XPATH, config_general.JOB_POST_XPATH)
            jobs = []
            
            for post in posts:
                href = post.get_attribute("href")
                title = post.text.strip()
                
                jobs.append({
                    "ID": self.job_counter,
                    "title": title,
                    "link": href
                })
                self.job_counter += 1
            
            print(f"Found {len(posts)} jobs")
            return jobs
            
        except Exception as e:
            print(f"Error on {url}: {e}")
            return []
    
    def scrape_multiple(self, urls):
        all_jobs = []
        for url in urls:
            jobs = self.scrape_page(url)
            all_jobs.extend(jobs)
        return all_jobs


def build_urls(base_url, num_pages):
    return [base_url.format(page=i) for i in range(1, num_pages + 1)]


def save_to_csv(data, output_dir, output_path):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)
    
    df = pd.DataFrame(data)
    df.to_csv(output_path, index=False, encoding="utf-8-sig")
    return df


def main():
    urls = build_urls(config_general.BASE_URL, config_general.NUM_PAGES_TO_CRAWL)
    print(f"Pages to scrape: {len(urls)}")
    
    chrome = ChromeDriver()
    scraper = JobLinkScraper(
        chrome.get(),
        wait_timeout=config_general.WAIT_TIMEOUT,
        sleep_time=config_general.SLEEP_TIME
    )
    
    try:
        jobs = scraper.scrape_multiple(urls)
        print(f"\nTotal jobs collected: {len(jobs)}")
        
        df = save_to_csv(
            jobs,
            config_general.JOB_LIST_DIR,
            config_general.JOB_LIST_FILE_PATH
        )
        
        if not df.empty:
            print(df.head())
        
        print(f"Saved to: {config_general.JOB_LIST_FILE_PATH}")
        
    except Exception as e:
        print(f"Critical error: {e}")
    
    finally:
        chrome.quit()


if __name__ == "__main__":
    main()