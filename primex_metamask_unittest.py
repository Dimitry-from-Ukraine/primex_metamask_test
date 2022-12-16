# Login to Primex App with MetaMask wallet autotest
# Pass condition: after login to Primex and network change, it should be connected with Goerli network

import time
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options

class PrimexMetaMaskLogin(unittest.TestCase):

    def setUp(self):
        options = Options()
        options.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'
        self.driver = webdriver.Firefox(options=options)
        self.driver.implicitly_wait(10)
        #installing MetaMask addon
        self.driver.install_addon(r'C:\Users\Dmitr\AppData\Local\Temp\rust_mozprofileNYgzqR\extensions\webextension@metamask.io.xpi', temporary=True)
        self.driver.get("https://app.primex.finance/")  
    
    def test_login_primex_with_metamask(self):
        driver = self.driver
        self.create_metamask_wallet()
    
        # Accepting cookies dialog and release notes
        driver.find_element(By.CSS_SELECTOR, 'div.text-state-active > p:nth-child(2)').click()
        driver.find_element(By.CSS_SELECTOR, 'div.bg-main-primary:nth-child(2)').click()
        # Click on Connect Wallet icon and then 'MetaMask Wallet' button
        driver.find_element(By.CSS_SELECTOR, '.no-js-icon-wallet_24px_regular_dafault').click()
        driver.find_element(By.CSS_SELECTOR, r'#modal-root > div > div > div > div.flex.flex-wrap.justify-between.-my-2\.5.w-full > div:nth-child(1) > div').click()

        self.connect_with_metamask()
        self.switch_to_goerli_network()

        # Test passes if network will be switched to Goerli
        # It takes some time for the page to refresh the network type
        # I used sleep 5 because have no time right now for proper handling implementation
        time.sleep(5)
        network_status = driver.find_element(By.CSS_SELECTOR, r'.lm\:inline-block').get_attribute("innerHTML")
        self.assertIn("Goerli", network_status)


    # MetaMask login method: switch to MetaMask tab and create new wallet
    def create_metamask_wallet(self):
        driver = self.driver

        # Starts creation of a new wallet, agrees with metamask terms and creates test wallet
        self.switch_to_tab('MetaMask')
        driver.find_element(By.CSS_SELECTOR, '.button').click()
        driver.find_element(By.CSS_SELECTOR, 'button.button:nth-child(2)').click()
        driver.find_element(By.CSS_SELECTOR, 'div.select-action__select-button:nth-child(2) > button:nth-child(2)').click()

        # input and confirm password, check on Terms and finish with click on button Create
        driver.find_element(By.ID, 'create-password').send_keys("iddqd666")
        driver.find_element(By.ID, 'confirm-password').send_keys("iddqd666")
        driver.find_element(By.CLASS_NAME, 'first-time-flow__checkbox').click()
        driver.find_element(By.CSS_SELECTOR, '.button').click()

        # Wait until the next page about SEED and finish creation with buttons Next and Remind Me Later
        WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '.seed-phrase-intro__left > div:nth-child(3)'))
        )
        driver.find_element(By.CSS_SELECTOR, '.button').click()
        driver.find_element(By.CSS_SELECTOR, 'button.button:nth-child(1)').click()

        self.switch_to_tab('Primex App')

    # Method connects to Primex with MetaMask wallet 
    def connect_with_metamask(self):
        driver = self.driver     

        self.switch_to_tab('MetaMask Notification')
        # wait until MetaMask Connect dialog is loaded
        WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '.permissions-connect-header__title'))
        )
        # Click on  Next and Connect buttons
        driver.find_element(By.CSS_SELECTOR, 'button.button:nth-child(2)').click()
        driver.find_element(By.CSS_SELECTOR, 'button.button:nth-child(2)').click()

        self.switch_to_tab('Primex App')

    # Method switches to proper network - Goerli
    def switch_to_goerli_network(self):
        driver = self.driver
        # checking if Selected Network is wrong and confirming network switch than
        network_status = driver.find_element(By.CSS_SELECTOR, r'.lm\:inline-block').get_attribute("innerHTML")
        if (network_status=='Wrong Network'):
            self.switch_to_tab('MetaMask Notification')
            # wait until MetaMask Connect dialog is loaded
            WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'button.button:nth-child(2)'))
            )
            # confirm network switch
            driver.find_element(By.CSS_SELECTOR, 'button.button:nth-child(2)').click()

        self.switch_to_tab('Primex App')

    # Method allows to switch between browser tabs/notification windows by checking its title 
    def switch_to_tab(self, tab_title):
        time.sleep(0.5) #should be investigated and handled properly
        for handle in self.driver.window_handles:
            self.driver.switch_to.window(handle)
            if(self.driver.title==tab_title):
                break

    def tearDown(self):
        self.driver.close()

if __name__ == "__main__":
    unittest.main()
