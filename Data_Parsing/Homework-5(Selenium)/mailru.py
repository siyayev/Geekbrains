from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
from pymongo import MongoClient

client = MongoClient('127.0.0.1',27017)
db = client['letters']
jj = db.mailru

chrome_options = Options()
chrome_options.add_argument('start-maximized')
driver = webdriver.Chrome('./chromedriver.exe',options=chrome_options)
driver.get('https://mail.ru/')

login = driver.find_element_by_id('mailbox:login-input')
login.send_keys('study.ai_172@mail.ru')
login.send_keys(Keys.ENTER)


passw = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.NAME,'password')))
passw.send_keys('NextPassword172')
passw.send_keys(Keys.ENTER)
time.sleep(5)
letters = driver.find_elements_by_class_name('ll-sj__normal')
first_letter = letters[0]
first_letter.click()
action = ActionChains(driver)

while True:
    try:
        time.sleep(3)
        letter_title = driver.find_element_by_class_name('thread__subject').text
        letter_sender = driver.find_element_by_class_name('letter-contact').get_attribute('title')
        letter_date = driver.find_element_by_class_name('letter__date').text
        letter_body = driver.find_element_by_class_name('html-parser').text
        letter = {'Title':letter_title, 'Sender':letter_sender, 'Date':letter_date, 'Body':letter_body}
        jj.insert_one(letter)
        next_letter = driver.find_element_by_xpath("//div[contains(@class,'portal-menu-element_next')]")
        next_letter.click()
    except:
        break

action.perform()
