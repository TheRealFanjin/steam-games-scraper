from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.options import Options


game = input('Type the game you want to find here: ')

# configure browser
print('Starting Browser')
firefox_options = Options()
firefox_options.headless = True
browser = webdriver.Firefox(options=firefox_options, service_log_path='/tmp/geckodriver.log')
print('Retrieving website')
browser.get('https://store.steampowered.com/')

# input & click
print('Waiting for website to load')
WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input#store_nav_search_term"))).send_keys(game)
WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div#search_suggestion_contents>a"))).click()
print('Navigating to game page')

# supported platforms
print('Retrieving supported platforms')
mac = False
linux = False
try:
    browser.find_element_by_css_selector('div.game_area_purchase_game_wrapper:nth-child(1) > div:nth-child(1) > div:nth-child(2) > '
                                         'span:nth-child(2)')
    mac = True
except NoSuchElementException:
    pass

try:
    browser.find_element_by_css_selector('div.game_area_purchase_game_wrapper:nth-child(1) > div:nth-child(1) > div:nth-child(2) > '
                                         'span:nth-child(3)')
    linux = True
except NoSuchElementException:
    pass

# price
print('Retrieving price')
discounted = False
try:
    price = browser.find_element_by_css_selector('div.game_purchase_action:nth-child(4) > div:nth-child(1) > div:nth-child(1)').text
except NoSuchElementException:
    original_price = browser.find_element_by_css_selector('div.game_purchase_action:nth-child(6) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > '
                                                          'div:nth-child(1)')
    discounted_price = browser.find_element_by_css_selector('div.game_purchase_action:nth-child(6) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > '
                                                            'div:nth-child(2)')
    discounted = True

# system requirements
print('Retrieving system requirements')
browser.find_element_by_css_selector('div.sysreq_tab:nth-child(3)').click()
specs = browser.find_element_by_css_selector('div.game_area_sys_req:nth-child(3)').text

# close browser
print('Finished Retrieving data, closing browser \n')
browser.close()

# printing supported platforms
if mac and linux:
    print('Supported Platforms: Windows, Mac and Linux')
elif mac:
    print('Supported Platforms: Windows and Mac')
elif linux:
    print('Supported Platforms: Windows and Linux')
else:
    print('Supported Platforms: Windows Only')
print('\n')

# printing price
if discounted:
    print('Price: Discount $' + discounted_price + ' from $' + original_price)
else:
    print('Price: ' + price)
print('\n')

# printing system requirements
print('System Requirements: \n')
print('-------------------------------- \n')
print(specs)
print('-------------------------------- \n')

print('Finished Successfully')
