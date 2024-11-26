import logging
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from dotenv import load_dotenv
import os

# 加載 .env 檔案
load_dotenv()

# 讀取環境變數
ZUVIO_URL = os.getenv("ZUVIO_URL")
USER_EMAIL = os.getenv("USER_EMAIL")
USER_PASSWORD = os.getenv("USER_PASSWORD")
GOOGLE_USERNAME = os.getenv("GOOGLE_USERNAME")
GOOGLE_PASSWORD = os.getenv("GOOGLE_PASSWORD")
COURSE_NAME = os.getenv("COURSE_NAME")

# 設置 logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def initialize_driver():
    """初始化 WebDriver"""
    driver = webdriver.Chrome()
    logging.info("初始化 WebDriver")
    return driver


def open_website(driver, url):
    """打開指定的網址"""
    driver.get(url)
    logging.info(f"打開網站: {url}")


def click_element(driver, xpath):
    """等待並點擊指定的元素"""
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, xpath))
    ).click()
    logging.info(f"點擊元素: {xpath}")


def switch_to_new_window(driver):
    """切換到新打開的窗口"""
    driver.switch_to.window(driver.window_handles[-1])
    logging.info("切換到新窗口")


def enter_text(driver, xpath, text):
    """在指定的輸入框中輸入文字"""
    input_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, xpath))
    )
    input_field.send_keys(text)
    logging.info(f"輸入文字 '{text}' 到元素: {xpath}")


def wait_for_element(driver, by, value):
    """等待指定的元素加載"""
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((by, value))
    )
    logging.info(f"元素已加載: {value}")
    return element


def select_course(driver, course_name):
    """選擇特定課程"""
    course_list_container = wait_for_element(
        driver, By.CLASS_NAME, "i-m-p-c-a-course-list"
    )
    course_boxes = course_list_container.find_elements(
        By.CLASS_NAME, "i-m-p-c-a-c-l-course-box"
    )

    for course_box in course_boxes:
        course_title = course_box.find_element(
            By.CLASS_NAME, "i-m-p-c-a-c-l-c-b-t-course-name"
        ).text
        if course_name in course_title:
            driver.execute_script("arguments[0].scrollIntoView(true);", course_box)
            time.sleep(1)  # 等待滾動完成
            driver.execute_script("arguments[0].click();", course_box)
            logging.info(f"已選擇課程: {course_name}")
            return
    logging.warning(f"未找到目標課程: {course_name}")


def main():
    """主流程"""
    driver = initialize_driver()
    try:
        # 打開 Zuvio 主頁
        open_website(driver, ZUVIO_URL)

        # 點擊跳轉按鈕
        click_element(driver, "/html/body/div/div[3]/div[3]/div[2]")

        # 切換到新頁面
        switch_to_new_window(driver)

        # 輸入帳號
        enter_text(
            driver, "/html/body/div[1]/div[3]/form/input[1]", USER_EMAIL
        )

        # 點擊登入按鈕
        click_element(driver, '//*[@id="login-btn"]')

        # 切換到 Google 登入頁面
        switch_to_new_window(driver)

        # 輸入 Google 帳號
        enter_text(
            driver,
            "/html/body/div[1]/div[1]/div[2]/c-wiz/div/div[2]/div/div/div[1]/form/span/section/div/div/div[1]/div/div[1]/div/div[1]/input",
            GOOGLE_USERNAME,
        )

        # 點擊 "下一步"
        click_element(
            driver,
            "/html/body/div[1]/div[1]/div[2]/c-wiz/div/div[3]/div/div[1]/div/div/button/span",
        )

        # 輸入 Google 密碼
        enter_text(
            driver,
            "/html/body/div[1]/div[1]/div[2]/c-wiz/div/div[2]/div/div/div[1]/form/span/section[2]/div/div/div[1]/div[1]/div/div/div/div/div[1]/div/div[1]/input",
            GOOGLE_PASSWORD,
        )

        # 點擊 "下一步"
        click_element(
            driver,
            "/html/body/div[1]/div[1]/div[2]/c-wiz/div/div[3]/div/div[1]/div/div/button/span",
        )

        wait_for_element(driver, By.CLASS_NAME, "i-m-p-c-a-course-list")

        select_course(driver, COURSE_NAME)

        click_element(driver, "/html/body/div[2]/div[3]/div[1]/div[2]")

        # 滑動到第一個輸入框並輸入文字
        textarea1 = driver.find_element(
            By.XPATH, "/html/body/div[2]/div[3]/div[2]/div[3]/div[3]/div/textarea"
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", textarea1)
        time.sleep(1)
        enter_text(
            driver,
            "/html/body/div[2]/div[3]/div[2]/div[3]/div[3]/div/textarea",
            "資管/四技/三年甲班",
        )

        # 滑動到第二個輸入框並輸入文字
        textarea2 = driver.find_element(
            By.XPATH, "/html/body/div[2]/div[3]/div[2]/div[4]/div[3]/div/textarea"
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", textarea2)
        time.sleep(1)
        enter_text(
            driver,
            "/html/body/div[2]/div[3]/div[2]/div[4]/div[3]/div/textarea",
            "資管個案研討",
        )

        checkboxes = [
            "/html/body/div[2]/div[3]/div[2]/div[5]/div[3]/div[1]/div",
            "/html/body/div[2]/div[3]/div[2]/div[6]/div[3]/div[1]/div/div[1]",
            "/html/body/div[2]/div[3]/div[2]/div[7]/div[3]/div[1]/div/div[1]",
            "/html/body/div[2]/div[3]/div[2]/div[8]/div[3]/div[1]/div/div[1]",
            "/html/body/div[2]/div[3]/div[2]/div[9]/div[3]/div[1]/div/div[1]",
            "/html/body/div[2]/div[3]/div[2]/div[10]/div[3]/div[1]/div/div[1]",
            "/html/body/div[2]/div[3]/div[2]/div[11]/div[3]/div[1]/div/div[1]",
            "/html/body/div[2]/div[3]/div[2]/div[12]/div[3]/div[1]/div/div[1]",
            "/html/body/div[2]/div[3]/div[2]/div[13]/div[3]/div[1]/div/div[1]",
            "/html/body/div[2]/div[3]/div[2]/div[14]/div[3]/div[1]/div/div[1]",
            "/html/body/div[2]/div[3]/div[2]/div[15]/div[3]/div[1]/div/div[1]",
        ]

        for checkbox_xpath in checkboxes:
            checkbox = driver.find_element(By.XPATH, checkbox_xpath)
            driver.execute_script("arguments[0].scrollIntoView(true);", checkbox)
            time.sleep(1)
            click_element(driver, checkbox_xpath)

        time.sleep(3)

        textarea3 = driver.find_element(
            By.XPATH, "/html/body/div[2]/div[3]/div[2]/div[16]/div[3]/div/textarea"
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", textarea3)
        time.sleep(1)
        enter_text(
            driver,
            "/html/body/div[2]/div[3]/div[2]/div[16]/div[3]/div/textarea",
            "無",
        )

        textarea4 = driver.find_element(
            By.XPATH, "/html/body/div[2]/div[3]/div[2]/div[17]/div[3]/div/textarea"
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", textarea4)
        time.sleep(1)
        enter_text(
            driver,
            "/html/body/div[2]/div[3]/div[2]/div[17]/div[3]/div/textarea",
            "無",
        )

        time.sleep(1)

        click_element(driver, "/html/body/div[2]/div[3]/div[3]/div[2]")

    except Exception as e:
        logging.error(f"執行過程中出錯: {e}")
    finally:
        driver.quit()
        logging.info("關閉瀏覽器")


if __name__ == "__main__":
    main()
