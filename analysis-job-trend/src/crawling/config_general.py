# analysis-job-trend\src\crawling\config.py
# File config tham số cho .py/1-Generate-Job-URL.py
# File .ipynb/1-Generate-Job-URL.ipynb chỉ demo 1 page, không load config này

import os

# --- CẤU HÌNH ĐƯỜNG DẪN (PATHS) ---
# Lấy đường dẫn thư mục chứa file config.py này (src/crawling)
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

# Đi ngược lên 2 cấp để về thư mục gốc dự án (analysis-job-trend)
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, '..', '..'))

# Định nghĩa các đường dẫn dữ liệu
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
JOB_LIST_DIR = os.path.join(DATA_DIR, "job-list")

# Tên file và đường dẫn file lưu danh sách job
JOB_LIST_FILE_NAME = "job_list.csv"
JOB_LIST_FILE_PATH = os.path.join(JOB_LIST_DIR, JOB_LIST_FILE_NAME)

# Tên file và đường dẫn file lưu danh sách job dạng JSON đã crawl
JOB_LIST_FILE_NAME_JSON = "job_list.json"
JOB_LIST_FILE_PATH_JSON = os.path.join(JOB_LIST_DIR, JOB_LIST_FILE_NAME_JSON)

# --- CẤU HÌNH CRAWLING (CRAWLING SETTINGS) ---
# URL gốc với placeholder {page} để thay thế số trang
BASE_URL = "https://www.topcv.vn/tim-viec-lam-cong-nghe-thong-tin-cr257?type_keyword=1&page={page}&category_family=r257"

# Số lượng trang muốn crawl
NUM_PAGES_TO_CRAWL = 71 # 3527 jobs, 50 jobs/page

# Thời gian chờ (giây)
SLEEP_TIME = 8
WAIT_TIMEOUT = 10

# --- CẤU HÌNH SELECTOR (XPATH) ---
JOB_POST_XPATH = '//h3[contains(@class,"title")]//a[@href]'

# --- CẤU HÌNH DRIVER CHROME ---
CHROME_PATH = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
CHROME_DEBUG_PORT = 8797
CHROME_PROFILE = r'C:\Users\PC\.wdm\drivers\chromedriver\win64\142.0.7444.175\chromedriver-win32\localhost'
# Another path in another VPS 
# C:\Users\Administrator\.wdm\drivers\chromedriver\win64\137.0.7151.119\chromedriver-win32\localhost

# Dùng để chạy trên nhiều VPS, mỗi máy chạy 1 khoảng
# Để None nếu muốn chạy toàn bộ file
DATA_START_INDEX = 1000   # Bắt đầu từ dòng này
DATA_END_INDEX = 2000     # Kết thúc trước dòng này (giống slice của Python)
