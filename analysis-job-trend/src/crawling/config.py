# analysis-job-trend\src\crawling\config.py
import os

# --- CẤU HÌNH ĐƯỜNG DẪN (PATHS) ---
# Lấy đường dẫn thư mục chứa file config.py này (src/crawling)
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

# Đi ngược lên 2 cấp để về thư mục gốc dự án (analysis-job-trend)
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, '..', '..'))

# Định nghĩa các đường dẫn dữ liệu
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
JOB_LIST_DIR = os.path.join(DATA_DIR, "job-list")
JOB_LIST_FILE_NAME = "job_list.csv"
JOB_LIST_FILE_PATH = os.path.join(JOB_LIST_DIR, JOB_LIST_FILE_NAME)

# --- CẤU HÌNH CRAWLING (CRAWLING SETTINGS) ---
# URL gốc với placeholder {page} để thay thế số trang
BASE_URL = "https://www.topcv.vn/tim-viec-lam-cong-nghe-thong-tin-cr257?type_keyword=1&page={page}&category_family=r257"

# Số lượng trang muốn crawl
NUM_PAGES_TO_CRAWL = 2 

# Thời gian chờ (giây)
SLEEP_TIME = 3
WAIT_TIMEOUT = 10

# --- CẤU HÌNH SELECTOR (XPATH) ---
JOB_POST_XPATH = '//h3[contains(@class,"title")]//a[@href]'