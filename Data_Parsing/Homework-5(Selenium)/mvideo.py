from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import time
from pymongo import MongoClient

client = MongoClient('127.0.0.1',27017)
db = client['mvideo']
jj = db.tops

chrome_options = Options()
chrome_options.add_argument('start-maximized')
driver = webdriver.Chrome('./chromedriver.exe',options=chrome_options)
main_link = 'https://www.mvideo.ru'
driver.get(main_link)
time.sleep(5)
div_hits = driver.find_elements_by_xpath("//div[contains(@class,'gallery-layout sel-hits-block')]")

#ХИТ ПРОДАЖ ВТОРОЙ ПО СПИСКУ, ЕСЛИ ПОМЕНЯЕТСЯ ВЕРСТКА ПРИДЕТСЯ МЕНЯТЬ
hp = div_hits[1]

action = ActionChains(driver)
action.move_to_element(hp)
action.perform()

#ПРОГРУЖАЕМ ВЕСЬ СПИСОК
while True:
    try:
        next_button = hp.find_element_by_xpath(".//a[@class='next-btn sel-hits-button-next']")
        next_button.click()
    except:
        break

#ПО ЭЛЕМЕНТНО ПЕРЕБИРАЕМ ТОВАРЫ И ГРУЗИМ В БАЗУ
items = hp.find_elements_by_xpath(".//li[@class='gallery-list-item height-ready']")
for item in items:
    product_title = item.find_element_by_class_name("sel-product-tile-title").text
    product_link = item.find_element_by_class_name("sel-product-tile-title").get_attribute('href')
    product_info = item.find_element_by_class_name("sel-product-tile-title").get_attribute('data-product-info')
    product = {'Name': product_title, 'Link': product_link, 'Details': product_info}
    jj.insert_one(product)

driver.close()