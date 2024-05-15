from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException, TimeoutException, NoAlertPresentException, UnexpectedAlertPresentException
import json, time
from settings import (
    URL, URL1,
    CARD_NUM1, CARD_NUM2, CARD_NUM3, CARD_NUM4, 
    VALID_MONTH, VALID_YEAR, VALID_CODE
)
card_inputs = ["#cardNo_1", "#cardNo_2", "#cardNo_3_temp", "#cardNo_4"]
card_numbers = [CARD_NUM1, CARD_NUM2, CARD_NUM3, CARD_NUM4]

### 設定 Chrome 選項
chrome_options = Options()
chrome_options.add_argument("--disable-extensions")  
chrome_options.add_experimental_option("prefs", {
    "profile.managed_default_content_settings.images": 2,  
    "profile.managed_default_content_settings.stylesheets": 2,  
    "profile.managed_default_content_settings.animations": 2, 
    "profile.default_content_setting_values.fonts": 2, 
})

    
def autobuy(driver):
    try:
        buy_button = WebDriverWait(driver, 0.1).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".buynow"))
        )
        buy_button.click()
        print("成功點擊購買")
        try:
            checkout_button = WebDriverWait(driver, 0.1).until(
                EC.element_to_be_clickable((By.XPATH, "//td[contains(@class, 'checkoutButton') and contains(@class, 'selected')]/a"))
            )
            checkout_button.click()
            print("成功點擊結帳")
            ### 跳出結帳畫面，填入信用卡資料。
            for card_input_selector, card_number in zip(card_inputs, card_numbers):
                card_input = WebDriverWait(driver, 0.1).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, card_input_selector))
                )
                card_input.send_keys(card_number)
            driver.execute_script("document.getElementById('cardValidMonth').value = arguments[0];", VALID_MONTH) ### 有效日期-月
            try:
                valid_year_dropdown = driver.find_element(By.CSS_SELECTOR, "#cardValidYear")
                select = Select(valid_year_dropdown)
                select.select_by_value(str(VALID_YEAR)) ### 有效日期-年
                try:
                    cvv_input = WebDriverWait(driver, 0.1).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, "#cardCVV"))
                    )
                    cvv_input.send_keys(VALID_CODE)
                    try:
                        order_save_button = WebDriverWait(driver, 0.1).until(
                            EC.element_to_be_clickable((By.CSS_SELECTOR, "#orderSave"))
                        )
                        # order_save_button.click()  ### 真的要買才解除註解！
                        time.sleep(5) ### 成功後的畫面停留時間，看你想要多久。
                        # print("已成功下單！") 

                    except TimeoutException:
                        print("下單按鈕未在預期時間內出現。")
                        raise 
                except TimeoutException:
                    print("CVV 輸入框未在預期時間內出現。")
                    raise 
            except NoSuchElementException:
                print("年份選單未在預期時間內出現。")
                raise 
        except TimeoutException:
            print("結帳按鈕未在預期時間內出現。")
            raise
    except TimeoutException:
        print("購買按鈕未在預期時間內出現。")
        raise
    return 


MAX_TRIES = 100 ### 最大重試(刷新)次數，自訂，越多跑越久。

if __name__ == "__main__":
    ### 預先加載 cookie 
    retries = 0
    sucess_state = False
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(URL)
    with open ("momo.json", "r") as f: # 讀取 cookie
        cookies = json.loads(f.read())
    for c in cookies:
        driver.add_cookie(c)
    driver.refresh() 
    checkbox_ids = ["insureChkBox", "insureChkBox2"]
    for checkbox_id in checkbox_ids:
        try:
            checkbox = driver.find_element(By.ID, checkbox_id)
            if not checkbox.is_selected():
                checkbox.click()
                print(f"點擊按鈕 {checkbox_id}")
                # print(f"未找到原因: {str(e)}")
        except Exception as e:
            print(f"未找到按钮 {checkbox_id}")
            pass
    while (retries < MAX_TRIES) and (sucess_state == False):
        try:
            # start_time = time.time()
            autobuy(driver)
            driver.quit()
            Sucess_state = True  
            # end_time = time.time()
            # print(f"程序執行時間：{end_time - start_time} 秒")
            break  # 如果成功，跳出迴圈
        except Exception as e:
            driver.refresh()  # 刷新页面
            retries += 1  # 增加重试次数
            print(f"第 {retries} 次重試...")

    if retries == MAX_TRIES:
        print("達到最大刷新次數，結束程式。")


    