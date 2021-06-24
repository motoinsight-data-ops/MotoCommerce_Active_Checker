from scraper import *
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

url1 = 'https://www.vwlaurentides.com/en/sitemap'


url2 = 'https://www.richmondhillvw.ca/sitemap/'


url3 = 'https://www.vwvicto.com/en/sitemap'

url4 = 'https://www.midstatemitsu.com/sitemap/'


url5 = 'https://www.midstatemitsu.com'

url = url5

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

driver.get(url)

new_url = ''

# Check if site is in french
if 'fr' in driver.current_url.split('/')[-1]:
    for piece in driver.current_url.split('/')[0:-1]:
        new_url += piece
    new_url += '/'
    new_url += driver.current_url.split('/')[-1].replace('fr', 'en')
    driver.get(new_url)


# hasSiteMap = getSiteMap(driver)

active = isActive(driver, url)

print(active)