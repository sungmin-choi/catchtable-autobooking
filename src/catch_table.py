import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import config
import pyperclip

# 아이디와 패스워드를 여기에 입력
#다시2
ID = "namja306@naver.com"
PW = "XXXXXX"
LOGINURL = "https://app.catchtable.co.kr/ct/login"
URL = "https://app.catchtable.co.kr/ct/shop/bongyeondang"
# 월 은 숫자뒤에 '월' 자도 부텨주세요 예) 11월, 12월, 1월 
BOOKING_MONTH='12월'
BOOKING_DAY1='5'
BOOKING_DAY2='6'
BOOKING_PERSONAL_CNT = '3명'

now = datetime.now()
options = Options()
options.headless = False


def set_chrome_driver():
    chrome_options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    # driver = config.WebDriver().driver_instance
    return driver

# executable_path 부분에 브라우저 드라이버 파일 경로를 입력
driver = set_chrome_driver()
wait = WebDriverWait(driver, 10)
driver.get(URL)

def login():
    loginBtn = wait.until(
        EC.element_to_be_clickable((By.CLASS_NAME, "__kakao"))).click()

    driver.switch_to.window(driver.window_handles[1])
    id_box = wait.until(EC.element_to_be_clickable((By.ID, "input-loginKey")))
    pw_box = driver.find_element("id","input-password")
    id_box.click()

    pyperclip.copy(ID)
    ActionChains(driver).key_down(Keys.COMMAND).send_keys('v').key_up(
        Keys.COMMAND).perform()

    pw_box.click()
    pyperclip.copy(PW)
    ActionChains(driver).key_down(Keys.COMMAND).send_keys('v').key_up(
        Keys.COMMAND).perform()

    login = wait.until(EC.element_to_be_clickable(
        (By.CLASS_NAME, "highlight"))).click()

    time.sleep(0.5)

def selected_date():

    open_calendar = wait.until(
        EC.element_to_be_clickable((By.CLASS_NAME, "btn-reservation"))).click() 
    calendar = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "calendar-container")))
    time.sleep(0.6)
    
    # 원하는 월로 이동하기
    while True:

        try:
            month_element =  wait.until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div[4]/div[3]/div/div[1]/div[1]/div/div/div/div/div/div/div[1]/div/div/div[2]/button/span[2]'))
    )
        finally:
            print(month_element.text)    
        if month_element.text == BOOKING_MONTH:
            break
        print('try')
        next_btn = wait.until(
        EC.element_to_be_clickable((By.CLASS_NAME,'mbsc-calendar-button.custom-next.mbsc-reset.mbsc-font.mbsc-button.mbsc-windows.mbsc-ltr.mbsc-button-flat.mbsc-icon-button'))).click()

    # 원하는 날짜로 이동하기
    time.sleep(0.6)
    cur_table = driver.find_element(By.CLASS_NAME,'mbsc-calendar-table.mbsc-flex-col.mbsc-flex-1-1.mbsc-calendar-table-active')
    rows = cur_table.find_elements(By.CLASS_NAME,'mbsc-calendar-row.mbsc-flex.mbsc-flex-1-0')
    personal_cnt_list = driver.find_element(By.ID,'optionPersonalCntList')

    

  

    for row in rows:
        items = row.find_elements(By.CLASS_NAME,'mbsc-calendar-cell.mbsc-flex-1-0-0.mbsc-calendar-day.mbsc-windows.mbsc-ltr')
        for item in items:
            class_attribute = item.get_attribute("class")
            if ('mbsc-disabled' in class_attribute) == False and ('mbsc-calendar-day-outer' in class_attribute) == False:
                if item.text == BOOKING_DAY1:
                    booking_date1 = item
                elif item.text == BOOKING_DAY2:
                    booking_date2 = item

    booking_date1.click()

    personal_cnt_items = personal_cnt_list.find_elements(By.CLASS_NAME,'swiper-slide')
    
    for item in personal_cnt_items:
            if item.text == BOOKING_PERSONAL_CNT:
                item.click()
                break

    return [booking_date1,booking_date2]


def wait_booking(booking_date1,booking_date2):
    flag = 0
    timetable_list = 0
    timetable_list_items=0
    while True:
        try:
            print("try")
            if flag == 0:
                booking_date1.click()
                flag = 1
            elif flag == 1:
                booking_date2.click()
                flag = 0
            time.sleep(0.5)
            timetable_list = driver.find_elements(By.CLASS_NAME,'timetable-list')
            timetable_list_items = timetable_list[2].find_elements(By.CLASS_NAME,'timetable-list-item')
            print('timetable_list_items:',len(timetable_list_items))
        except:
            time.sleep(0.2)

        if timetable_list!=0 and timetable_list_items!=0:
            break

    for item in timetable_list_items:
        print(item.text)
        if len(item.text) > 0:

            ActionChains(driver).move_to_element(item).click().perform()
            break

        # time.sleep(1)
        # # print('button Text:',button.text)
        # ActionChains(driver).move_to_element(button).click()
        

    



def main():

    # login()
    [booking_date1,booking_date2]=selected_date()
    print(booking_date1.text,booking_date2.text)
    wait_booking(booking_date1,booking_date2)
    open_calendar = wait.until(
        EC.element_to_be_clickable((By.CLASS_NAME, "btn.btn-lg.btn-red"))).click() 
    open_calendar = wait.until(
        EC.element_to_be_clickable((By.CLASS_NAME, "btn.btn-lg.btn-red"))).click() 
    time.sleep(1000)
    
    # wait_booking()
    # calendar = get_calender()

    # while result != 1:
    #     result = make_booking(calendar)


if __name__ == "__main__":
    main()