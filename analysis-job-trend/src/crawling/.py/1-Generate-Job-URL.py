# analysis-job-trend\src\crawling\1-Generate-Job-URL.py

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
import pandas as pd
import os

import config 

def create_driver():
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")

    service = Service()
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def crawl_job_links(driver, urls):
    data = []
    job_id = 1

    for url in urls:
        driver.get(url)
        time.sleep(config.SLEEP_TIME) # Sử dụng config

        try:
            WebDriverWait(driver, config.WAIT_TIMEOUT).until(
                EC.presence_of_all_elements_located(
                    (By.XPATH, config.JOB_POST_XPATH)
                )
            )

            posts = driver.find_elements(By.XPATH, config.JOB_POST_XPATH)

            for post in posts:
                href = post.get_attribute("href")
                title = post.text.strip()

                data.append({
                    "ID": job_id,
                    "title": title,
                    "link": href
                })
                job_id += 1

        except Exception as e:
            print(f"Lỗi ở URL {url}: {e}")

    return pd.DataFrame(data)

# --- MAIN EXECUTION ---

# 1.1 Generate list of URLs to crawl
# Sử dụng range(1, NUM_PAGES + 1) để lấy đúng số trang mong muốn
urls = [config.BASE_URL.format(page=i) for i in range(1, config.NUM_PAGES_TO_CRAWL + 1)]

# 1.2 Start crawling
driver = create_driver()

print(f"Bắt đầu crawl {len(urls)} trang...")
df_jobs = crawl_job_links(driver, urls)
driver.quit() # Nên đóng driver sau khi xong

print(df_jobs.head())
print(f"Tổng số bài đăng thu thập được: {len(df_jobs)}")

# 1.3 Save results to CSV using Config paths
# Tạo thư mục nếu chưa tồn tại (sử dụng đường dẫn từ config)
if not os.path.exists(config.JOB_LIST_DIR):
    os.makedirs(config.JOB_LIST_DIR, exist_ok=True)

# Lưu file
df_jobs.to_csv(config.JOB_LIST_FILE_PATH, index=False, encoding="utf-8-sig")

print(f"Đã lưu file vào: {config.JOB_LIST_FILE_PATH}")