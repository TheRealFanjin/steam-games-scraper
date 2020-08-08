from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.options import Options
from sys import exit

games = {}
x = 0

while True:
    if x == 0:
        game = input('Type the game you want to find here: ')
    else:
        game = input('Type the game you want to find here (or enter nothing to continue): ')
    if not game:
        break
    games[game] = {}
    x += 1
# configure browser
print('Starting Browser')
firefox_options = Options()
firefox_options.headless = True
browser = webdriver.Firefox(service_log_path='/tmp/geckodriver.log')
print('Retrieving website')
browser.get('https://store.steampowered.com/')

for a_game in games:
    print('Finding info for "' + a_game + '"')

    # input & click
    print('Waiting for page to load')
    WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input#store_nav_search_term"))).send_keys(a_game)
    WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div#search_suggestion_contents>a"))).click()
    print('Navigating to game page')

    # if age-restricted:
    try:
        browser.find_element_by_css_selector('.agegate_birthday_selector')
        age_query = input('"' + a_game + '" is age-restricted, do you want to continue? y/n ')
        if age_query != 'y':
            print('Abort')
            exit()
        select = Select(browser.find_element_by_id('ageYear'))
        select.select_by_value('2000')
        browser.find_element_by_css_selector('a.btnv6_blue_hoverfade:nth-child(1)').click()
    except NoSuchElementException:
        pass

    print('Waiting for game page to load')
    # name of game
    games[a_game]['name'] = WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.apphub_AppName'))).text

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

    if mac and linux:
        games[a_game]['platform'] = 'all'
    elif mac:
        games[a_game]['platform'] = 'mac'
    elif linux:
        games[a_game]['platform'] = 'linux'
    else:
        games[a_game]['platform'] = 'windows'

    # price
    print('Retrieving price')
    discounted = False
    try:
        games[a_game]['price'] = browser.find_element_by_css_selector('div.game_purchase_action:nth-child(4) > div:nth-child(1) > div:nth-child(1)').text
    except NoSuchElementException:
        try:
            games[a_game]['before_price'] = browser.find_element_by_class_name('discount_original_price').text
            games[a_game]['after_price'] = browser.find_element_by_class_name('discount_final_price').text
        except NoSuchElementException:
            try:
                games[a_game]['price'] = 'FREE'
            except NoSuchElementException:
                games[a_game]['bundle_price'] = browser.find_element_by_css_selector('div.game_purchase_action_bg:nth-child(2) > div:nth-child(1)')
    except Exception:
        games[a_game]['price'] = 'Error: Unable to get price'

    # system requirements
    print('Retrieving system requirements')
    games[a_game]['specs'] = browser.find_element_by_css_selector('.game_area_sys_req').text

# close browser
print('Finished Retrieving data, closing browser \n')
print('********************************************')
browser.close()

for each_game in games.keys():
    print('GAME: ' + games[each_game]['name'].upper())

    # printing supported platforms
    if games[each_game]['platform'] == 'all':
        print('Supported Platforms: Windows, Mac and Linux')
    elif games[each_game]['platform'] == 'mac':
        print('Supported Platforms: Windows and Mac')
    elif games[each_game]['platform'] == 'linux':
        print('Supported Platforms: Windows and Linux')
    else:
        print('Supported Platforms: Windows Only')
    print('\n')

    # printing price
    try:
        print('Price: Discounted ' + games[each_game]['after_price'] + ' from ' + games[each_game]['before_price'])
    except KeyError:
        print('Price: ' + games[each_game]['price'])
    except Exception:
        print('Bundled Price: ' + games[each_game]['bundle_price'])
    print('\n')

    # printing system requirements
    print('System Requirements: \n')
    print('-------------------------------- \n')
    print(games[each_game]['specs'])
    print('--------------------------------')
    input('Press enter to continue ')

print('Finished Successfully')
