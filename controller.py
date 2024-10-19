from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


url = 'https://www.artplast.ru'
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 YaBrowser/24.7.0.0 Safari/537.36'
options = Options()
options.add_argument('start maximized')
options.add_argument(f'user-agent={user_agent}')
driver = webdriver.Chrome(options=options)

driver.get(url)

wait = WebDriverWait(driver, timeout=10)
search_box = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "form.relative input")))
#search_box = driver.find_element(By.CSS_SELECTOR, "form.relative input")

search_box.send_keys("ПОС60165")

search_button = driver.find_element(By.CSS_SELECTOR, "form.relative button") #submit
search_button.submit()

name = driver.find_element(By.XPATH, "//div[@class='space-y-3']/a")
price = driver.find_elements(By.XPATH, "//div[@class='text-[20px] leading-5 whitespace-nowrap min-w-[110px]']/span")

print(name.text)

for p in price:
    print(p.text)