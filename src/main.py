from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from scraper import *
import pandas as pd
import os
import csv


"""
------------------------------------------------------------------------
Checks to see if an Excel list of dealership's websites are still using the Motocommerce API or not.
------------------------------------------------------------------------
Author: Andrei Secara & Naftal Kerecha - Data & Automation
Updated: June 23, 2021
------------------------------------------------------------------------
Notes:
- To use this program, you must navigate to ./src and type in python run.py

- Excel input file should be placed in ./input

- Excel file should containg 'Account Name' column, containing the dealership name to check

- After that, you must pick an EXCEL file (.xlsx) to input from the list that appears
- *** MAKE SURE TO WAIT FOR AD BLOCK TO FINISH INSTALLING ***
- (Please type the file name accurately including the extension)

- Let it run. It will take a while depending on how many sites you are checking,
but it is tested to avoid hanging / freezing. 

* In the case of a crash / unexpected faliure, all data gets saved to the respective spreadsheet name in the ./save folder

------------------------------------------------------------------------
"""

# For removing bugs. Found solution at https://stackoverflow.com/questions/64927909/failed-to-read-descriptor-from-node-connection-a-device-attached-to-the-system
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_extension('../crx/adblock.crx')


class ContactScraper:
    def setup_method(self):
        print("Launching driver...")
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        print("*** PLEASE WAIT UNTIL ADBOCK FINISHES INSTALLING ***")
        self.outputLoc = "../output/"
        self.tempSaveFileLocation = '../save/'
        self.vars = {}
        
        # Placeholder for dataframe object
        self.df = None
        return


    def teardown_method(self):
        print("Shutting down driver...")
        self.driver.quit()
        return

    
    def readFromExcel(self):
        print("Type in the name of the spreadsheet you want to domain check: \n")

        print(os.listdir("../input"))

        excel_file_name = input("File name: ")
        self.excel_file_path = "../input/" + excel_file_name

        self.tempSaveFileLocation += excel_file_name.replace('.xlsx', '') + '.csv'

        self.df = pd.read_excel(self.excel_file_path)

        # Update temporary save file to have the same name as the input excel file
        self.outputLoc += excel_file_name[0:-5] + '.xlsx'

        print("File read into object dataframe from: " + self.excel_file_path)
        print()
        return


    def saveRow(self, dealer_name, url, siteMap, motoCommerceActive):
        try:
            with open(self.tempSaveFileLocation, 'a+') as saveFile:
                output_writer = csv.writer(saveFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
                # Append one line containing the following information
                output_writer.writerow([dealer_name, url, siteMap, motoCommerceActive])
        except:
            return
        return


    def motocommerceScraper(self):
        isActiveList = []
        urlList = []
        siteMaps = []
        cur = 1
        numRows = len(self.df.index)
        for index, row in self.df.iterrows():
            print("Page: ", cur, " / ", numRows)
            
            dealer_name = row['Account Name']
            # Check if row is empty
            if pd.isnull(dealer_name):
                isActiveList.append(None)
                urlList.append(None)
                siteMaps.append(None)
                cur += 1
                continue
            url = None

            # This is here because of weird errors
            while url is None:
                try:
                    url = find_website(self.driver, dealer_name)
                except:
                    pass
            # This is also here because of a timed out receiving message
            # from renderer error
            success = False
            while success == False:
                try:
                    self.driver.get(url)
                    success = True
                except:
                    pass
            
            new_url = ''

            # Check if site is in french
            if 'fr' in self.driver.current_url.split('/')[-1]:
                for piece in self.driver.current_url.split('/')[0:-1]:
                    new_url += piece
                new_url += '/'
                new_url += self.driver.current_url.split('/')[-1].replace('fr', 'en')
                self.driver.get(new_url)

            
            # hasSiteMap = getSiteMap(self.driver)
            hasSiteMap = 'Not needed right now'
            active = isActive(self.driver, url)

            if active == False:
                hasSiteMap = getSiteMap(self.driver)
                find_car_with_site_map(self.driver, url)
                active = isActive_with_site_map(self.driver, url)
                

            # Append to rows that will later be added to the dataframe
            isActiveList.append(active)
            urlList.append(url)
            siteMaps.append(hasSiteMap)
            print(url + " Is Active: ", active)
            self.saveRow(dealer_name, url, hasSiteMap, active)
            cur += 1
        
        # Add new completed columns to dataframe
        self.df['URL'] = urlList
        self.df['Is Active Motocommerce'] = isActiveList
        self.df['Has Sitemap'] = siteMaps
        return
    
    def saveToExcel(self):
        print("Saving to excel file: " + self.outputLoc)
        writer = pd.ExcelWriter(self.outputLoc)
        self.df.to_excel(writer)
        writer.save()
        return