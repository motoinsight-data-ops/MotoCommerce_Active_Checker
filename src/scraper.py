from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By



def getSiteMap(driver):
    """
    -------------------------------------------------------
    Scans home page of dealer site for a site map, returns True is found and False if not found.
    -------------------------------------------------------
    Args: 
    Driver: Selenium Web Driver - The web driver passed in should already be at the dealership home page.
    Url: Str - The url of the dealer sites home page
        
    Returns: 
        True if a site map is found
        False if not
            
    ------------------------------------------------------
    """
    # Get all elements of page to iterate through and find the sitemap
    elems = driver.find_elements(By.XPATH, './/*')
    completed = 0
    for elem in elems:
        try:
            # Try getting the elements href attribute
            href = elem.get_attribute('href').lower()
            completed = 0
            
            # See if href contains substring with sitemap in it.
            if ('site' in href and 'map' in href) and 'xml' not in href:
                completed = 1
                # Navigate driver to dealerships sitemap
                print("Sitemap found")
                driver.get(href)
                return True
            
        # If it can't get href from this element, go to the next
        except:
            continue
    # If scan through all elements and no sitemap link found
    if completed == 0:
        print("No sitemap found")
        return False




def find_website(driver, website_name):
    url = None
    try:
        driver.get('http://www.google.com')
    except:
        time.sleep(10)
        driver.get('http://www.google.com')

    search = driver.find_element_by_name('q')
    search.send_keys(website_name)
    search.send_keys(Keys.RETURN) # hit return after you enter search text

    time.sleep(2)
    results = []
    all_elements = driver.find_elements(By.XPATH, './/*')
    for element in all_elements:
        try:
            # Search all google search results elements to find first link
            if element.get_attribute('class') == 'LC20lb DKV0Md':
                # Append parent to results
                results.append(element.find_element(By.XPATH, './..'))
                break
        except:
            continue
    
    # results = driver.find_elements(By.CLASS_NAME, 'LC20lb DKV0Md')  # finds webresults
    url = results[0].get_attribute('href')
    # results[0].click() # clicks the first one

    return url



def is_Majority_String(stringtoCompareTo):
    if len(stringtoCompareTo) * 0.5 <= len('new') + len('vehicles'):
        return True
    else:
        return False


def find_car_with_site_map(driver, url):
    # getSiteMap(driver)

    active = False
    # Find new inventory page


    # Check if sitemap has accordion

    all_elements = driver.find_elements(By.XPATH, './/*')
    accordion = None
    for element in all_elements:
        try:
            # Search all google search results elements to find first link
            if element.get_attribute('id') == 'accordion':
                accordion = element
                # print("Accordian found")
                break
        except:
            continue

    # new_vehicles_accordian_element_class_name = ''    
    found = False

    if accordion is not None:
        # accordion_children = accordion.find_elements(By.XPATH, './*')
        for element in all_elements:
            # print(element.text)
            try:
                # Search all elements of accordion to open the 'new vehicles' section
                if 'New Vehicle Inventory' in element.get_attribute('title') or 'Demonstrator Vehicles' in element.get_attribute('title'):
                    # element.click()
                    # print('Expanding Accordion')
                    # new_vehicles_accordian_element_class_name = element.get_attribute('class')
                    # all_elements = element.find_elements(By.XPATH, './/*')
                    driver.get(element.get_attribute('href'))
                    found = True
                    break
            except:
                continue

    else:
        for element in all_elements:
            try:
                # Search all elements to find new car inventory
                if 'new' in element.text.lower() and ('inventory' in element.text.lower() or 'vehicles' in element.text.lower()) and 'tool' not in element.text.lower() and is_Majority_String(element.text.lower()):
                    # Navigate to new inventory page
                    # print(element.text)
                    driver.get(element.get_attribute('href'))
                    found = True
                    break
            except:
                continue
    
    if found == False:
        errorCount = 0
        success = False
        while success == False:
            if errorCount > 10:
                print("Fatal error with site: " + url)
                print("Error number reached while trying to get new inventory page")
                return False
            try:
                driver.get(url.replace('/eng/', '')+'/new/inventory/search.html')
                errorCount += 1
                success = True
            except:
                pass
        

    # for element in all_elements:
    #     try:
    #         # Search all google search results elements to find first link
    #         if 'inventory' in element.text.lower() or 'inventaire' in element.text.lower():
    #             driver.get(element.get_attribute('href'))
    #             print("Inventory Found")
    #             break
    #     except:
    #         continue



    # Scan for motocommerce here
    html_source = driver.page_source.lower()
    if 'motocommerce' in html_source or 'motoinsight' in html_source:
        return True
    
    # Next if not found on new cars inventory page, find a page of a specific new car and check there
    all_elements = driver.find_elements(By.XPATH, './/*')
    for element in all_elements:
        try:
            # Scan all elements to find the new car page
            if '2021' in element.text or '2022' in element.text:
                element.click()
                break
        except:
            continue

    return False

def find_car(driver, url):

    # getSiteMap(driver)

    active = False
    # Find new inventory page


    # Check if sitemap has accordion

    all_elements = driver.find_elements(By.XPATH, './/*')
    # accordion = None
    # for element in all_elements:
    #     try:
    #         # Search all google search results elements to find first link
    #         if element.get_attribute('id') == 'accordion':
    #             accordion = element
    #             # print("Accordian found")
    #             break
    #     except:
    #         continue

    # # new_vehicles_accordian_element_class_name = ''    
    # found = False

    # if accordion is not None:
    #     # accordion_children = accordion.find_elements(By.XPATH, './*')
    #     for element in all_elements:
    #         # print(element.text)
    #         try:
    #             # Search all elements of accordion to open the 'new vehicles' section
    #             if 'New Vehicle Inventory' in element.get_attribute('title') or 'Demonstrator Vehicles' in element.get_attribute('title'):
    #                 # element.click()
    #                 # print('Expanding Accordion')
    #                 # new_vehicles_accordian_element_class_name = element.get_attribute('class')
    #                 # all_elements = element.find_elements(By.XPATH, './/*')
    #                 driver.get(element.get_attribute('href'))
    #                 found = True
    #                 break
    #         except:
    #             continue

    # else:
    #     for element in all_elements:
    #         try:
    #             # Search all elements to find new car inventory
    #             if 'new' in element.text.lower() and ('inventory' in element.text.lower() or 'vehicles' in element.text.lower()) and 'tool' not in element.text.lower() and is_Majority_String(element.text.lower()):
    #                 # Navigate to new inventory page
    #                 # print(element.text)
    #                 driver.get(element.get_attribute('href'))
    #                 found = True
    #                 break
    #         except:
    #             continue
    
    # if found == False:
    #     driver.get(url+'new/')

    for element in all_elements:
        try:
            # print(element.text)
            # Search all google search results elements to find first link
            if 'inventory' in element.text.lower() or 'inventaire' in element.text.lower():
                driver.get(element.get_attribute('href'))
                print("Inventory Found")
                break
        except:
            continue



    # Scan for motocommerce here
    html_source = driver.page_source.lower()
    if 'motocommerce' in html_source or 'motoinsight' in html_source:
        return True
    
    # Next if not found on new cars inventory page, find a page of a specific new car and check there
    all_elements = driver.find_elements(By.XPATH, './/*')
    for element in all_elements:
        try:
            # Scan all elements to find the new car page
            if '2021' in element.text or '2022' in element.text:
                element.click()
                break
        except:
            continue

    return False

def isActive_with_site_map(driver, url):
    active = False
    html_source = driver.page_source.lower()
    if 'motocommerce' in html_source or 'motoinsight' in html_source:
        active = True

    return active


def isActive(driver, url):
    active = False



    active = find_car(driver, url)


    if not active:
        # Scan for motocommerce here
        html_source = driver.page_source.lower()
        if 'motocommerce' in html_source or 'motoinsight' in html_source:
            active = True



    return active
