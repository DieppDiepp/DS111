import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from config_general import CHROME_DEBUG_PORT
DEBUG_PORT = CHROME_DEBUG_PORT

def connect_to_local_chrome(port=DEBUG_PORT):
    # Lấy ChromeDriver nếu chưa có
    driver_path = ChromeDriverManager().install()
    print("Driver nằm ở:", driver_path)

    # Tạo ChromeOptions để attach vào Chrome đang mở
    opts = Options()
    opts.add_experimental_option("debuggerAddress", f"localhost:{port}")

    # Kết nối vào Chrome local
    driver = webdriver.Chrome(service=Service(driver_path), options=opts)

    print("Đã kết nối vào Chrome local!")
    return driver


if __name__ == "__main__":
    # Kết nối
    driver = connect_to_local_chrome()

    # Mở web test
    driver.get("https://google.com")

    # Giữ cửa sổ lại
    input("Nhấn Enter để đóng trình duyệt...")
