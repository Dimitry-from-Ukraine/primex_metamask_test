# Login to Primex App with MetaMask wallet autotest
# selenium
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options

options = Options()
options.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'

driver = webdriver.Firefox(options=options)
driver.implicitly_wait(10)
#installing MetaMask addon
driver.install_addon(r'C:\Users\Dmitr\AppData\Local\Temp\rust_mozprofileNYgzqR\extensions\webextension@metamask.io.xpi', temporary=True)

driver.get("https://app.primex.finance/")

# MetaMask login function
#
primex_window_handle = driver.current_window_handle

for handle in driver.window_handles:
    driver.switch_to.window(handle)
    if(driver.title=='MetaMask'):
        break

driver.find_element(By.CSS_SELECTOR, '.button').click()
# agree with metamask terms and create test wallet
driver.find_element(By.CSS_SELECTOR, 'button.button:nth-child(2)').click()
driver.find_element(By.CSS_SELECTOR, 'div.select-action__select-button:nth-child(2) > button:nth-child(2)').click()

# input and confirm password, check on checkbox and click on button Create
driver.find_element(By.ID, 'create-password').send_keys("iddqd666")
driver.find_element(By.ID, 'confirm-password').send_keys("iddqd666")
driver.find_element(By.CLASS_NAME, 'first-time-flow__checkbox').click()
driver.find_element(By.CSS_SELECTOR, '.button').click()

#wait until next page is loaded by checking video box
WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '.seed-phrase-intro__left > div:nth-child(3)'))
)
# press Next button
driver.find_element(By.CSS_SELECTOR, '.button').click()
# remind me later button click
driver.find_element(By.CSS_SELECTOR, 'button.button:nth-child(1)').click()

driver.switch_to.window(primex_window_handle)


# Accepting cookies dialog and release notes
driver.find_element(By.CSS_SELECTOR, 'div.text-state-active > p:nth-child(2)').click()
driver.find_element(By.CSS_SELECTOR, 'div.bg-main-primary:nth-child(2)').click()

# Click on Create Wallet icon and then 'MetaMask Wallet' button
driver.find_element(By.CSS_SELECTOR, '.no-js-icon-wallet_24px_regular_dafault').click()
driver.find_element(By.CSS_SELECTOR, r'#modal-root > div > div > div > div.flex.flex-wrap.justify-between.-my-2\.5.w-full > div:nth-child(1) > div').click()


#switch to MetaMask notification window
for handle in driver.window_handles:
    driver.switch_to.window(handle)
    if(driver.title=='MetaMask Notification'):
        break

# wait until MetaMask Connect dialog is loaded
WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '.permissions-connect-header__title'))
)
#press Next button in notification window
driver.find_element(By.CSS_SELECTOR, 'button.button:nth-child(2)').click()

# press Connect button
# if need to wait for the next dialog .permissions-connect-header__title
driver.find_element(By.CSS_SELECTOR, 'button.button:nth-child(2)').click()

driver.switch_to.window(primex_window_handle)

# checking if Selected Network is wrong and confirming network switch than
network_status = driver.find_element(By.CSS_SELECTOR, r'.lm\:inline-block').get_attribute("innerHTML")
if (network_status=='Wrong Network'):
    for handle in driver.window_handles:
        driver.switch_to.window(handle)
        if(driver.title=='MetaMask Notification'):
            break

    # wait until MetaMask Connect dialog is loaded
    WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'h3.box'))
    )
    # confirm network switch
    driver.find_element(By.CSS_SELECTOR, 'button.button:nth-child(2)').click()

driver.switch_to.window(primex_window_handle)

# Test passes if network will be switched to Goerli it takes some delay for the page to refresh 
# I used sleep 5 in this case because it's more easy and only for one time check
time.sleep(5)
network_status = driver.find_element(By.CSS_SELECTOR, r'.lm\:inline-block').get_attribute("innerHTML")
print(network_status)
if (network_status=='Goerli'):
    print('Test passed successfully: Primex is connected')



# to prevent browser from autoclose, continue by input in console
keyword = input("enter a character or press enter in console to continue")