import subprocess
import time
import socket
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from config_general import CHROME_DEBUG_PORT, CHROME_PROFILE, CHROME_PATH

CHROME_PATH = CHROME_PATH
PROFILE_PATH = CHROME_PROFILE
DEBUG_PORT = CHROME_DEBUG_PORT

def is_running(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(("localhost", port))
    sock.close()
    return result == 0


def start_chrome_debug():
    if is_running(DEBUG_PORT):
        print(f"Chrome debug đã chạy trên port {DEBUG_PORT}")
        return

    print("Đang mở Chrome debug mode...")
    subprocess.Popen([
        CHROME_PATH,
        f"--remote-debugging-port={DEBUG_PORT}",
        f"--user-data-dir={PROFILE_PATH}"
    ])

    # đợi Chrome bật xong
    while not is_running(DEBUG_PORT):
        time.sleep(0.3)

    print("Chrome debug ready!")


def connect_to_chrome():
    driver_path = ChromeDriverManager().install()
    print("ChromeDriver:", driver_path)

    opts = Options()
    opts.add_experimental_option("debuggerAddress", f"localhost:{DEBUG_PORT}")

    driver = webdriver.Chrome(
        service=Service(driver_path),
        options=opts
    )

    print("Đã kết nối Selenium vào Chrome local!")
    return driver


if __name__ == "__main__":
    start_chrome_debug()
    driver = connect_to_chrome()

    driver.get("https://google.com")
    input("Nhấn Enter để đóng...")
