# Login to Primex App with MetaMask autotest
# selenium
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

# setting up options and loading profile with already installed MetaMask extension
options = webdriver.ChromeOptions()
options.add_argument(r"--user-data-dir=C:\Users\Dmitr\AppData\Local\Google\Chrome\User Data")
options.add_argument('--profile-directory=Default')
options.add_argument("--start-maximized")

driver = webdriver.Chrome(options=options)
driver.implicitly_wait(10) #wait until element becomes available
actions = ActionChains(driver)

driver.get("https://app.primex.finance/")

# Accepting cookies dialog
driver.find_element(By.CLASS_NAME, 'flex justify-center cursor-pointer h-full items-center rounded-xl text-white').click()

# Waiting until button 'connect wallet' will be clickable and pressing on it
# connectBtn = WebDriverWait(driver, 10).until(
#     EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div[2]/div[2]/div[1]/div[1]/div/div[2]/p'))
# )
# connectBtn.click()
connect_button = driver.find_element(By.CSS_SELECTOR, '#root > div.flex.w-full.sticky.bg-main-dark.px-6.pb-4.pt-8.top-0.border-b.justify-between > div.flex.items-center.mr-1 > div.relative')
actions.move_to_element(connect_button).perform()
connect_button.click()
# Waiting and pressing on 'MetaMask Wallet' button
# mmWalletBtn = WebDriverWait(driver, 10).until(
#     EC.presence_of_element_located((By.XPATH, '//*[@id="modal-root"]/div/div/div/div[2]/div[1]/div/div'))
# )
# mmWalletBtn.click()
driver.find_element(By.CSS_SELECTOR, r'#modal-root > div > div > div > div.flex.flex-wrap.justify-between.-my-2\.5.w-full > div:nth-child(1) > div').click()

print(driver.title)