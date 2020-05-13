import sys
import re

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
import clipboard

#import parameters
import time
from parsel import Selector
import csv
import os
import random
import pandas as pd
import sensitive_info.credentials

driver = webdriver.Chrome('/Users/kanem/chromedriver')
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')
options.add_argument('--headless')
options.add_argument("--window-size=1920,1080")

SCROLL_PAUSE_TIME = 0.7

def log_in_sales_nav(): #log in to linkedin and go to sales navigator
    driver.get('https://www.linkedin.com/login?trk=guest_homepage-basic_nav-header-signin')
    username = driver.find_element_by_id('username')
    username.send_keys(sensitive_info.credentials.user)
    time.sleep(0.5)
    
    password = driver.find_element_by_id('password')
    password.send_keys(sensitive_info.credentials.passw)
    log_in = driver.find_element_by_tag_name('button')
    log_in.click()
    print("logged in")
    time.sleep(0.5)

    driver.get('https://www.linkedin.com/sales/homepage')


def get_profile_info(lead_list, new_data):
    #website  - make sure to get .text
    with open(lead_list, 'r', encoding='utf-8', newline='') as open_file:
        csv_reader = csv.reader(open_file, delimiter=',')

        with open(new_data, 'w', encoding='utf-8', newline='') as write_file:
            csv_writer = csv.writer(write_file, delimiter=',')
            count = 1

            csv_writer.writerow(["first_name", "last_name", "jobTitle", "company", "linkedin_profile", "linkedincompanypageurl", "companywebsite", "city", "state", "companycountry"])
            #next(csv_reader)

            for row in csv_reader:
                print('reading row ' + str(count))
            #linkedin sales nav personal page
                driver.get(row[4])
                time.sleep(2)

                try:
                    menu_buttons = driver.find_element_by_class_name('right-actions-overflow-menu-trigger')
                    menu_buttons.click()
                    ac = ActionChains(driver)
                    ac.move_to_element(menu_buttons).move_by_offset(0,140).click().perform()
                    time.sleep(0.5)
                    linkedin_url = clipboard.paste()
                except NoSuchElementException:
                    company_url = "none"
                    print('no linkedin url?')

            #linkedin sales nav company page
                driver.get(row[5])
                time.sleep(2)
                try:
                    company = driver.find_element_by_class_name('result-lockup__name')
                    company_page = company.find_element_by_css_selector('a').get_attribute('href')
                    driver.get(company_page)
                except NoSuchElementException:
                    print('straight to company page, or no company page')

                try: #get company website
                    time.sleep(2)
                    web = driver.find_element_by_class_name('topcard-hoverable-meta-links')
                    website = web.find_element_by_css_selector('a').get_attribute('href')
                    #web = driver.find_element_by_link_text('Website')
                    #website = web.get_attribute('href')
                except NoSuchElementException:
                    website = "NONE"
                    print("no website")
                
                #company linkedin page url
                try:
                    menu_buttons = driver.find_element_by_class_name('right-actions-overflow-menu-trigger')
                    menu_buttons.click()
                    ac = ActionChains(driver)
                    ac.move_to_element(menu_buttons).move_by_offset(0,100).click().perform()
                    time.sleep(0.5)
                    company_url = clipboard.paste()
                except NoSuchElementException:
                    company_url = "none"
                    print('no company page url?')

                #driver.execute_script("window.history.go(-1)")
                #or driver.close()
                #time.sleep(2)
                count = count+1
                csv_writer.writerow([row[0], row[1], row[2], row[3], linkedin_url, company_url, website, row[6], row[7], row[8]])
                #csv_writer.writerow([website, company_url, linkedin_url])


rows = ["website", "company_linkedin", "linkedin_profile"]


lead_file = 'attorney_sales_nav_beta_page_one.csv'
new_data = 'attorney_sales_nav_page_one_individual.csv'
log_in_sales_nav()
get_profile_info(lead_file, new_data)

