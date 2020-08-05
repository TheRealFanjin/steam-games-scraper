from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.options import Options
from sys import exit
import time

game = input('Type the game you want to find here: ')

# configure browser
print('Starting Browser')
firefox_options = Options()
firefox_options.headless = True
browser = webdriver.Firefox(options=firefox_options, service_log_path='/tmp/geckodriver.log')
print('Retrieving website')
browser.get('https://store.steampowered.com/')

# input & click
print('Waiting for home page to load')
WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input#store_nav_search_term"))).send_keys(game)
WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div#search_suggestion_contents>a"))).click()
print('Navigating to game page')

# if age-restricted:
try:
    browser.find_element_by_css_selector('.agegate_birthday_selector')
    age_query = input('This game is age-restricted, do you want to continue? y/n ')
    if age_query != 'y':
        print('Abort')
        exit()
    select = Select(browser.find_element_by_id('ageYear'))
    select.select_by_value('2000')
    browser.find_element_by_css_selector('a.btnv6_blue_hoverfade:nth-child(1)').click()
except NoSuchElementException:
    pass

print('Waiting for game page to load')
time.sleep(10)

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
    original_price = browser.find_element_by_class_name('discount_original_price').text
    discounted_price = browser.find_element_by_class_name('discount_final_price').text
    discounted = True

# system requirements
print('Retrieving system requirements')
specs = browser.find_element_by_css_selector('.game_area_sys_req').text

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
