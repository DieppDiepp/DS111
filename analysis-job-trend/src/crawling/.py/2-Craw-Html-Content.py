from logging import config
import os
import sys
import time
import json
import random
import socket
import subprocess
from datetime import datetime, timedelta

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
    
    def get_config_strategy(self, url):
        """
        Xác định layout dựa trên URL và Elements có trên trang.
        """
        # 1. Nếu là link thường
        if "/brand/" not in url:
            return config_job_detail.STANDARD
        
        # 2. Nếu là link Brand, cần check kỹ HTML để xem là Loại 1 hay Loại 2
        try:
            # Check nhanh xem có element đặc trưng của Brand Type 1 không
            # Dùng find_elements để không bị exception nếu không thấy (trả về list rỗng)
            if len(self.driver.find_elements(By.CLASS_NAME, "premium-job-basic-information")) > 0:
                print("   -> Layout: BRAND TYPE 1 (Premium)")
                return config_job_detail.BRAND
            
            # Check xem có element đặc trưng của Brand Type 2 không
            elif len(self.driver.find_elements(By.CLASS_NAME, "box-header")) > 0:
                print("   -> Layout: BRAND TYPE 2 (Box Info)")
                return config_job_detail.BRAND_V2
            
            else:
                # Fallback về Standard nếu không nhận diện được (hiếm gặp)
                print("   -> Layout: Unknown Brand -> Fallback STANDARD")
                return config_job_detail.STANDARD
                
        except Exception as e:
            print(f"   -> Error detecting layout: {e}")
            return config_job_detail.STANDARD
    
    def extract_attribute(self, xpath, attr):
        try:
            element = self.driver.find_element(By.XPATH, xpath)
            return element.get_attribute(attr) or "Null"
        except:
            return "Null"
    
    def wait_for_cloudflare(self):
        """
        Kiểm tra xem có bị Cloudflare chặn không.
        Nếu có: Tạm dừng vòng lặp, phát âm thanh (beep) và chờ người dùng xử lý thủ công trên trình duyệt.
        """
        while True:
            try:
                # Dấu hiệu nhận biết Cloudflare: Title web đổi thành "Just a moment..."
                page_title = self.driver.title
                
                # Hoặc kiểm tra text trong body nếu title chưa kịp đổi
                # page_source = self.driver.page_source (cẩn thận dùng cái này có thể nặng)
                
                if "Just a moment" in page_title or "Attention Required" in page_title:
                    print("\n" + "="*50)
                    print("PHÁT HIỆN CLOUDFLARE! ĐANG TẠM DỪNG...")
                    print("Vui lòng mở trình duyệt và tick vào ô xác thực (Verify you are human).")
                    print("Code sẽ tự động chạy tiếp sau khi bạn vượt qua.")
                    print("="*50 + "\n")
                    
                    # Phát tiếng kêu 'beep' để báo hiệu (chỉ chạy trên Windows)
                    try:
                        import winsound
                        winsound.Beep(1000, 500) # Tần số 1000Hz, 0.5 giây
                    except:
                        pass # Bỏ qua nếu không phải Windows hoặc lỗi âm thanh

                    # Chờ 30 giây rồi check lại
                    time.sleep(30)
                else:
                    # Nếu tiêu đề bình thường -> Thoát vòng lặp, cho phép chạy tiếp
                    break
            except Exception:
                # Nếu driver lỗi lúc check (ví dụ mạng rớt), cứ break để code chính xử lý ngoại lệ
                break
    
    def expand_full_content(self):
        """
        Kiểm tra và click nút 'Xem đầy đủ mô tả công việc' nếu tồn tại.
        """
        try:
            # XPath trỏ vào nút button nằm trong div class 'content-preview__toggle'
            expand_btn_xpath = "//div[contains(@class, 'content-preview__toggle')]//button"
            
            # Dùng find_elements để kiểm tra an toàn (trả về list rỗng nếu ko có, ko gây lỗi)
            buttons = self.driver.find_elements(By.XPATH, expand_btn_xpath)
            
            if buttons:
                # Dùng Javascript Executor để click (tránh bị che bởi quảng cáo/header)
                self.driver.execute_script("arguments[0].click();", buttons[0])
                time.sleep(1)

        except Exception as e:
            # Nếu lỗi click thì bỏ qua, in warning nhẹ
            print(f"   -> Warning: Could not expand content. {e}")

    def crawl(self, url):
        try:
            self.driver.get(url)
            self.wait_for_cloudflare()

            wait = WebDriverWait(self.driver, self.timeout)
            config = self.get_config_strategy(url)
            
            # Chờ Title load
            wait.until(EC.presence_of_element_located(
                (By.XPATH, config["SINGLE_FIELDS"]['job_title'])
            ))

            # Phải gọi sau khi trang đã load xong Title, và TRƯỚC KHI bắt đầu cào data
            self.expand_full_content()
            
            time.sleep(2)
            
            data = {}
            
            # Cào dữ liệu theo Config đã chọn
            for key, xpath in config["SINGLE_FIELDS"].items():
                data[key] = self.extract_single_field(xpath)
            
            for key, xpath in config["LIST_FIELDS"].items():
                data[key] = self.extract_list_field(xpath)
            
            for key, (xpath, attr) in config["ATTRIBUTE_FIELDS"].items():
                data[key] = self.extract_attribute(xpath, attr)

            # XỬ LÝ LOGIC RIÊNG CHO BRAND V2
            # Nếu là Brand V2, deadline đang là con số (ví dụ: "23")
            # Ta cần convert: Ngày hiện tại + 23 ngày = "dd/mm/yyyy"
            if config == config_job_detail.BRAND_V2 and data.get('deadline') != "Null":
                try:
                    days_left = int(data['deadline']) # Chuyển chuỗi "23" thành số 23
                    future_date = datetime.now() + timedelta(days=days_left)
                    data['deadline'] = future_date.strftime("%d/%m/%Y") # Format lại thành ngày tháng
                except ValueError:
                    # Nếu không phải số (ví dụ đã hết hạn hoặc text lạ), giữ nguyên hoặc để Null
                    pass

            # Metadata
            data['url'] = url
            data['date_crawl'] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

            # Gắn nhãn layout để sau này dễ debug
            if config == config_job_detail.BRAND:
                data['layout_type'] = 'brand_v1'
            elif config == config_job_detail.BRAND_V2:
                data['layout_type'] = 'brand_v2'
            else:
                data['layout_type'] = 'standard'
            
            return data, None
            
        except TimeoutException:
            print(f"Timeout waiting for elements: {url}")
            return None, "Timeout"
        except Exception as e:
            print(f"Error crawling {url}: {str(e)}")
            return None, str(e)

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
    
    # Đọc dữ liệu gốc
    df = pd.read_csv(input_csv, encoding="utf-8-sig")
    total_jobs_original = len(df)

    # Áp dụng Slice từ Config (Phân chia dữ liệu cho VPS)
    start_idx = getattr(config_general, 'DATA_START_INDEX', 0)
    end_idx = getattr(config_general, 'DATA_END_INDEX', None)  # Mặc định là None (lấy hết)

    # Nếu trong config để None thì Python hiểu là lấy hết
    if start_idx is None: start_idx = 0
    
    # Cắt DataFrame
    df = df[start_idx:end_idx]
    
    # Reset index để log in ra số thứ tự đẹp (tùy chọn)
    # df.reset_index(drop=True, inplace=True) 

    print(f"Data Partitioning Configured:")
    print(f"   - Original Total: {total_jobs_original}")
    print(f"   - Processing Range: [{start_idx} -> {end_idx if end_idx else 'End'}]")
    print(f"   - Jobs to process on this VPS: {len(df)}")
    
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