from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

from selenium.webdriver.chrome.options import Options 

import random
import time
import os
import csv 
import re
import pandas as pd


def validate_field(field):
	if (field == ""):
		field = 'no results'
		return field
	else:
		return field

driver = webdriver.Chrome('/Users/kanem/chromedriver')

chrome_options = webdriver.ChromeOptions()
prefs = {"profile.default_content_setting_values.notifications" : 2}
chrome_options.add_experimental_option("prefs",prefs)
#driver = webdriver.Chrome(options=chrome_options)



def login():

    driver.get('https://rocketreach.co/login')

    google_login = driver.find_element_by_class_name('oauth-google-icon')
    google_login.click()

    try:
        email = driver.find_element_by_name('identifier')
    except NoSuchElementException as exception:     
        email = driver.find_element_by_name('Email')
        
    email.send_keys("kma@kamodigital.com")

    try:
        next_button = driver.find_element_by_id('identifierNext')
    except NoSuchElementException as exception:
        next_button = driver.find_element_by_id('next')
            
    next_button.click()
        
    time.sleep(7)
    try:
        passw = driver.find_element_by_name('password')
    except NoSuchElementException as exception:
        passw = driver.find_element_by_id('password')
        
    passw.send_keys("na84up9yjaf")
    
    try:
        next_pass = driver.find_element_by_id('passwordNext')
    except NoSuchElementException as exception:
        next_pass = driver.find_element_by_id('submit')
        
    next_pass.click()
    

login()

def infofinder(linkedinurls):
    #search each lead via linkedin url from csv, then add to new csv file
    driver.get('https://rocketreach.co')
    time.sleep(2)
    driver.get('https://rocketreach.co/search')
    with open('dentistownercaryrocketreach.csv', 'w', encoding='utf-8', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['LinkedIn URL', 'Email / Phone', 'Email / Phone', 'Email/Phone'])	

        for i in range(len(linkedinurls)):
            inputname = driver.find_element_by_id('searchInput')
            inputname.clear()
            inputname.send_keys(linkedinurls[i])

            search = driver.find_element_by_id('searchButton')
            search.click()

         #   while (!driver.find_element_by_class_name('ng-hide')):
         #       time.sleep(2)
            time.sleep(15)
            #lookup contact
            try:
                get_contact = driver.find_element_by_id('firstLookupButton')
                get_contact.click()
                print('new contact')
                time.sleep(2)
            except NoSuchElementException as exception:
                print('already added')
                continue
        #or
            #while(driver.find_element_by_class_name('btn-outreach') == None):
            #    time.sleep(2)
            
            time.sleep(15)    
#get valid emails
            emails = driver.find_elements_by_class_name('contact-list')
            for x in range(len(emails)):
                try:
                    verified = driver.find_element_by_class_name('verified')
                           
                    if (verified):
                        vemail = driver.find_element_by_class_name('entry_text').text
                        writer.writerow([linkedinurls[i], vemail])
                except NoSuchElementException as exception:
                    print('no verified emails')
                    continue
                
    driver.close()
    driver.quit()

linkedinurls = []
with open('dentistryownercary.csv', 'r') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=",")        
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            print(f'column names are {", ".join(row)}')
            line_count += 1
        else:
            print(f'\t{row[0]}\t{row[7]}')
            linkedinurls.append(row[7])
            line_count += 1
    print(f'processed {line_count} lines')
    infofinder(linkedinurls)

            



        #using regular expressions - we want quality data (names) going in, and quality results coming out
        #with the needed information

        ##pattern matching?
        ##if last name "durusky" is in the name, then we can scrape the information


#how diff. names are formed
#Some have "Dr." "D.D.S." "[middle name]" [middle name initial] and/or all of the above
#check through each as if they have all of the possibilities
#ex.
#John Taylor****
#John L. Taylor*
#John Larry Taylor
#john taylor, MD check
#Dr. John Taylor*
#Dr. John L. Taylor
#Dr. John Larry Taylor
#Dr. John L. Taylor, D.D.S, md, dd.
#Dr. John Larry Taylor, D.D.S.
#
