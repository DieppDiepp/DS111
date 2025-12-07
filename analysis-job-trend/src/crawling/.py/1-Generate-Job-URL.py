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
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
import config

def create_driver():
    """Khởi tạo Chrome Driver với các options."""
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")

    service = Service()
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def crawl_job_links(driver, urls):
    """Thực hiện crawl link bài đăng từ danh sách URL trang."""
    data = []
    job_id = 1

    for url in urls:
        print(f"Đang xử lý trang: {url}")
        driver.get(url)
        time.sleep(config.SLEEP_TIME)

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
            
            print(f" -> Tìm thấy {len(posts)} bài đăng.")

        except Exception as e:
            print(f" -> Lỗi ở URL {url}: {e}")

    return pd.DataFrame(data)

def main():
    """Hàm thực thi chính."""
    print("=== BẮT ĐẦU QUÁ TRÌNH CRAWL URL ===")
    
    # 1. Tạo danh sách URL dựa trên config
    # range(1, x + 1) để chạy từ trang 1 đến trang x
    urls = [config.BASE_URL.format(page=i) for i in range(1, config.NUM_PAGES_TO_CRAWL + 1)]
    print(f"Tổng số trang cần quét: {len(urls)}")

    # 2. Khởi tạo Driver và Crawl
    driver = create_driver()
    
    try:
        df_jobs = crawl_job_links(driver, urls)
        print(f"\nTổng số bài đăng thu thập được: {len(df_jobs)}")
        
        # In thử 5 dòng đầu
        if not df_jobs.empty:
            print(df_jobs.head())

        # 3. Lưu kết quả
        # Tạo thư mục nếu chưa có
        if not os.path.exists(config.JOB_LIST_DIR):
            os.makedirs(config.JOB_LIST_DIR, exist_ok=True)
            print(f"Đã tạo thư mục: {config.JOB_LIST_DIR}")

        # Lưu file CSV
        df_jobs.to_csv(config.JOB_LIST_FILE_PATH, index=False, encoding="utf-8-sig")
        print(f"Đã lưu file thành công tại: {config.JOB_LIST_FILE_PATH}")

    except Exception as e:
        print(f"Có lỗi nghiêm trọng xảy ra: {e}")
    
    finally:
        # Luôn đóng trình duyệt dù chạy thành công hay thất bại
        driver.quit()
        print("=== ĐÃ ĐÓNG TRÌNH DUYỆT & KẾT THÚC ===")

if __name__ == "__main__":
    main()

# python src\crawling\1-Generate-Job-URL.py