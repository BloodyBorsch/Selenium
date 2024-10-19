from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from pprint import pprint
import pandas as pd
import time


url = 'https://www.artplast.ru'
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 YaBrowser/24.7.0.0 Safari/537.36'
options = Options()
#options.add_argument(f'user-agent={user_agent}')
options.add_argument('start-maximized')
driver = webdriver.Chrome(options=options)

def find_text(get_from: list, push_to: list, name):    
    temp_dict = {}        
    temp_dict["Наименование"] = name
    for i in range(len(get_from)):        
        if i % 2 == 0 or i == 0:
            dict_category = (get_from[i].text).replace(":", " ")
            temp_dict[dict_category] = get_from[i+1].text    
    push_to.append(temp_dict)

def create_csv(clean_list: list):   
    keys = list()
    for x in clean_list:
        keys.append(list(x.keys())[0])

    df = pd.DataFrame(clean_list)
    df.to_csv(f"goods.csv", encoding='utf-8', index=False)
    # with open("goods.csv", "w", newline="") as file:
    #     writer = csv.DictWriter(file, keys)
    #     writer.writeheader()
    #     writer.writerows(clean_list)

driver.get(url)

wait = WebDriverWait(driver, timeout=10)
search_box = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "form.relative input")))
#search_box = driver.find_element(By.CSS_SELECTOR, "form.relative input")

search_box.send_keys("ПОС60165")

search_button = driver.find_element(By.CSS_SELECTOR, "form.relative button") #submit
search_button.submit()

name = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='space-y-3']/a"))).text
price = driver.find_elements(By.XPATH, "//div[@class='text-[20px] leading-5 whitespace-nowrap min-w-[110px]']/span")
value = driver.find_element(By.XPATH, './/div[contains(@x-show, "thing")]/button[contains(@class, "rounded-br-lg")]')
[value.click() for _ in range(3)]

print(name)

for p in price:
    print(p.text)

actions = ActionChains(driver)
add_to_cart = driver.find_element(By.XPATH, './/div[@class="space-y-2"]/div/button[contains(@x-show, "!in_cart")]')
go_to_cart = driver.find_element(By.XPATH, './/a[@class="relative group"]/div[@class="space-y-2"]')


time.sleep(4)

actions.move_to_element(add_to_cart).click(add_to_cart).move_to_element(go_to_cart)
actions.perform()

time.sleep(3)

go_to_cart.click()

cart_info_dirty = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//ul[@class="space-y-4"]/li[contains(@class, "flex items-center justify")]/span')))
#cart_info_dirty = driver.find_elements(By.XPATH, '//ul[@class="space-y-4"]/li[contains(@class, "flex items-center justify")]/span')
cart_info_clean = []

find_text(cart_info_dirty, cart_info_clean, name)
pprint(cart_info_clean)

create_csv(cart_info_clean)

print()

