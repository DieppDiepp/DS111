import os
import sys
import time
import json
import random
import socket
import subprocess
from datetime import datetime

import pandas as pd
from tqdm import tqdm
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

# --- SETUP PATHS ---
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

import config_general
import config_job_detail

# --- CONSTANTS ---
CHROME_PATH = config_general.CHROME_PATH
CHROME_DEBUG_PORT = config_general.CHROME_DEBUG_PORT
CHROME_PROFILE = config_general.CHROME_PROFILE


class ChromeDebugger:
    def __init__(self, port=CHROME_DEBUG_PORT, profile_path=CHROME_PROFILE):
        self.port = port
        self.profile_path = profile_path
        self.chrome_path = CHROME_PATH
    
    def is_running(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('localhost', self.port))
        sock.close()
        return result == 0
    
    def start(self):
        if self.is_running():
            print(f"Chrome debug mode already running on port {self.port}")
            return
        
        print("Starting Chrome in debug mode...")
        subprocess.Popen([
            self.chrome_path,
            f'--remote-debugging-port={self.port}',
            f'--user-data-dir={self.profile_path}'
        ])
        
        while not self.is_running():
            time.sleep(0.5)
        print("Chrome ready")
    
    def connect(self):
        opts = Options()
        opts.add_experimental_option("debuggerAddress", f"localhost:{self.port}")
        return webdriver.Chrome(options=opts)


class JobDetailCrawler:
    def __init__(self, driver, timeout=15):
        self.driver = driver
        self.timeout = timeout
    
    def extract_single_field(self, xpath):
        try:
            return self.driver.find_element(By.XPATH, xpath).text.strip()
        except:
            return "Null"
    
    def extract_list_field(self, xpath):
        try:
            elements = self.driver.find_elements(By.XPATH, xpath)
            tags = [e.text.strip() for e in elements if e.text.strip()]
            return ", ".join(tags) if tags else "Null"
        except:
            return "Null"
    
    def extract_attribute(self, xpath, attr):
        try:
            element = self.driver.find_element(By.XPATH, xpath)
            return element.get_attribute(attr) or "Null"
        except:
            return "Null"
    
    def crawl(self, url):
        try:
            self.driver.get(url)

            wait = WebDriverWait(self.driver, self.timeout)
            
            # Chờ Title load
            wait.until(EC.presence_of_element_located(
                (By.XPATH, config_job_detail.SINGLE_FIELDS['job_title'])
            ))

            # Chờ Header Sections load (Nơi chứa Lương/Địa điểm/Kinh nghiệm)
            # Logic: Phải tìm thấy cái hộp chứa 3 thông tin này thì mới cào, tránh bị index sai
            header_section_xpath = "//div[contains(@class, 'job-detail__info--sections')]"
            wait.until(EC.presence_of_element_located((By.XPATH, header_section_xpath)))
            
            time.sleep(1)
            
            data = {}
            
            for key, xpath in config_job_detail.SINGLE_FIELDS.items():
                data[key] = self.extract_single_field(xpath)
            
            for key, xpath in config_job_detail.LIST_FIELDS.items():
                data[key] = self.extract_list_field(xpath)
            
            for key, (xpath, attr) in config_job_detail.ATTRIBUTE_FIELDS.items():
                data[key] = self.extract_attribute(xpath, attr)
            
            data['url'] = url
            data['date_crawl'] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            
            return data, None
            
        except TimeoutException:
            print(f"Timeout: {url}")
            return None, url
        except Exception as e:
            print(f"Error crawling {url}: {str(e)}")
            return None, url


def load_existing_data(output_path):
    if os.path.exists(output_path):
        with open(output_path, 'r', encoding='utf-8') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {} # Return empty if file corrupted
    return {}


def save_results(data_dict, output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    data_list = list(data_dict.values())
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data_list, f, ensure_ascii=False, indent=4)


def main():
    input_csv = config_general.JOB_LIST_FILE_PATH
    output_json = config_general.JOB_LIST_FILE_PATH_JSON
    
    if not os.path.exists(input_csv):
        print(f"Input file not found: {input_csv}")
        return
    
    df = pd.read_csv(input_csv, encoding="utf-8-sig")
    df = df[1:22]  # Test mode: process only 2 rows
    
    chrome = ChromeDebugger()
    chrome.start()
    driver = chrome.connect()
    
    crawler = JobDetailCrawler(driver)


    existing_data_list = load_existing_data(output_json)
    if isinstance(existing_data_list, list):
        # Convert list to dict key by Job ID (from CSV logic) or URL if ID missing
        # Dùng URL làm key để tránh duplicate crawl
        all_results = {item['url']: item for item in existing_data_list if 'url' in item}
    else:
        all_results = {}

    batch_count = 0
    failed = []
    
    print(f"Processing {len(df)} jobs...")
    
    try:
        for idx, row in enumerate(tqdm(df.iterrows(), total=len(df)), 1):
            row_data = row[1]
            link = row_data['link']
            
            # Skip nếu đã có trong file json cũ (Resume capability)
            if link in all_results:
                continue

            data, error = crawler.crawl(link)
            
            if data:
                # Gán ID từ CSV vào JSON result luôn cho đồng bộ
                data['csv_id'] = row_data['ID'] 
                all_results[link] = data
                batch_count += 1
            if error:
                failed.append(error)
            
            # Save mỗi 10 items
            if batch_count >= 10:
                save_results(all_results, output_json)
                print(f" -> Auto-saved {len(all_results)} jobs total.")
                batch_count = 0
            
            # Tăng thời gian sleep ngẫu nhiên lên (5-8s)
            time.sleep(random.randint(5, 8))
        
        # Save final
        save_results(all_results, output_json)
        print(f"\nSuccess! Total jobs saved: {len(all_results)} in {output_json}")
        
        if failed:
            print(f"Failed: {len(failed)} URLs")
    
    finally:
        # driver.quit() 
        print("Done")

if __name__ == "__main__":
    main()