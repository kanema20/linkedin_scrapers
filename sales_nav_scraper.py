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

sys.path.insert(1, 'sensitive_info/credentials') #local file for user/pass 
import credentials

driver = webdriver.Chrome('/Users/kanem/chromedriver')
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')
SCROLL_PAUSE_TIME = 0.6


def validate_field(field):
	if (field == ""):
		field = 'no results'
		return field
	else:
		return field

def log_in_sales_nav(): #log in to linkedin and go to sales navigator
    driver.get('https://www.linkedin.com/login?trk=guest_homepage-basic_nav-header-signin')
    username = driver.find_element_by_id('username')
    username.send_keys(credentials.user)
    time.sleep(0.5)
    
    password = driver.find_element_by_id('password')
    password.send_keys(credentials.passw)
    log_in = driver.find_element_by_tag_name('button')
    log_in.click()
    time.sleep(0.5)

    driver.get('https://www.linkedin.com/sales/homepage')

def search_leads(keyw):
    search_page = driver.get('https://www.linkedin.com/sales/search/people')

    keyword_filter = driver.find_element_by_xpath('//div/main/div/form/div/div/div/div/div/div/input')
    keyword_filter.send_keys(keyw)
    time.sleep(2)

    ac = ActionChains(driver)
    ac.move_to_element(keyword_filter).move_by_offset(-100,0).click().perform()
    time.sleep(2)
    #united states only
    geo =  driver.find_element_by_xpath('//form/ul/li[4]/div/div/div/div')
    geo.click()
    geo.click()
    time.sleep(2)
    us = driver.find_element_by_xpath('//div/div/ol/li[1]/button')
    us.click()

    time.sleep(1.5)
    #seniority_level = driver.find_element_by_xpath('//section/ul/li[3]/div/div/div/div/label')
    seniority_level =  driver.find_element_by_xpath('//form/ul/li[9]/div/div/div/div')
    seniority_level.click()
    time.sleep(2)
    owner = driver.find_element_by_xpath('//div/div/ol/li[1]/button')
    owner.click()
    time.sleep(2)
    cxo = driver.find_element_by_xpath('//div/div/ol/li[1]/button')
    cxo.click()
    time.sleep(2)
    partner = driver.find_element_by_xpath('//div/div/ol/li[1]/button')
    partner.click()
    time.sleep(2)

def traverse_leads_page_one():
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight/9)")
    time.sleep(SCROLL_PAUSE_TIME)   
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight/7)")
    time.sleep(SCROLL_PAUSE_TIME)        
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight/6)")
    time.sleep(SCROLL_PAUSE_TIME)
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight/5)")
    time.sleep(SCROLL_PAUSE_TIME)
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight/4)")
    time.sleep(SCROLL_PAUSE_TIME)
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight/3)")
    time.sleep(SCROLL_PAUSE_TIME)
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight/2)")
    time.sleep(SCROLL_PAUSE_TIME)
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight/1.5)")
    time.sleep(SCROLL_PAUSE_TIME)
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    
    lead_boxes = driver.find_elements_by_class_name('search-results__result-item')
    print(lead_boxes)

    print("page: 1")
    lead_count = 1
    for x in range(len(lead_boxes)):
    #get leads name                      
        name = driver.find_elements_by_class_name("result-lockup__name")[x].text
        print(name)
        lead_snp = driver.find_element_by_link_text(name)
    #get leads sales nav profile 
        lead_sales_page = lead_snp.get_attribute('href')
        print(lead_sales_page)

        location = driver.find_elements_by_class_name('result-lockup__misc-item')[x].text
        comma_locations = [m.start(0) for m in re.finditer(',', location)]
        try:
            city =  location[:comma_locations[0]]
            state = location[comma_locations[0]+2: comma_locations[1]]
            print("City: "+ city)
            print("State: " + state)
        except IndexError:
            city = location
            print("City: " + city)


    #get leads job title
        job_title = driver.find_elements_by_class_name("result-lockup__highlight-keyword")[x].text
        job_truncate = job_title.find('at')
        job_title = job_title[:job_truncate]
        print("Job Title: " + job_title)
        
    #get leads company - clean up this later
        company = driver.find_elements_by_class_name("result-lockup__position-company")[x].text
        company_truncate = company[:company.find('\n')] #truncate string to only have company name
        print("Company: " + company_truncate)

        company_link = driver.find_element_by_link_text(company)
        company_sales_nav_page = company_link.get_attribute('href')
        print("Company Sales Nav Page: " + company_sales_nav_page)
        
    #keep track of lead count
        print("# of leads: " + str(lead_count))
        lead_count = lead_count + 1

    

def traverse_leads():
    last_page = driver.find_element_by_xpath('//section/div[2]/nav/ol/li[11]/button').text
    lead_count = 1
    page_count = 1
    #for x in range(int(last_page)):
    for x in range(3):
        next_page()
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight/9)")
        time.sleep(SCROLL_PAUSE_TIME)   
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight/7)")
        time.sleep(SCROLL_PAUSE_TIME)        
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight/6)")
        time.sleep(SCROLL_PAUSE_TIME)
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight/5)")
        time.sleep(SCROLL_PAUSE_TIME)
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight/4)")
        time.sleep(SCROLL_PAUSE_TIME)
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight/3)")
        time.sleep(SCROLL_PAUSE_TIME)
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight/2)")
        time.sleep(SCROLL_PAUSE_TIME)
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight/1.5)")
        time.sleep(SCROLL_PAUSE_TIME)
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        
        lead_boxes = driver.find_elements_by_class_name('search-results__result-item')
        print(lead_boxes)

        print("page: " + str(page_count))
        page_count = page_count + 1

        #traverse individual leads in page
        for x in range(len(lead_boxes)):
        #get leads name                      
            name = driver.find_elements_by_class_name("result-lockup__name")[x].text
            print(name)
            lead_snp = driver.find_element_by_link_text(name)
        #get leads sales nav profile 
            lead_sales_page = lead_snp.get_attribute('href')
            print(lead_sales_page)

            location = driver.find_elements_by_class_name('result-lockup__misc-item')[x].text
            comma_locations = [m.start(0) for m in re.finditer(',', location)]
            try:
                city =  location[:comma_locations[0]]
                state = location[comma_locations[0]+2: comma_locations[1]]
                print("City: "+ city)
                print("State: " + state)
            except IndexError:
                city = location
                print("City: " + city)


        #get leads job title
            job_title = driver.find_elements_by_class_name("result-lockup__highlight-keyword")[x].text
            job_truncate = job_title.find('at')
            job_title = job_title[:job_truncate]
            print("Job Title: " + job_title)
            
        #get leads company - clean up this later
            company = driver.find_elements_by_class_name("result-lockup__position-company")[x].text
            company_truncate = company[:company.find('\n')] #truncate string to only have company name
            print("Company: " + company_truncate)

            company_link = driver.find_element_by_link_text(company)
            company_sales_nav_page = company_link.get_attribute('href')
            print("Company Sales Nav Page: " + company_sales_nav_page)
                
            #keep track of lead count
            print("# of leads: " + str(lead_count))
            lead_count = lead_count + 1

def next_page():
    #go to next page of sales nav results
    #up to page 6
    #then page 7, 4 on each side
    nextpage = driver.find_element_by_class_name('search-results__pagination-next-button')
    nextpage.click()

def csv_export(file_name, ):
    open_file = open(file_name, 'w')

    with open_file:
        writer = csv.writer(file_name)
        writer.writerow()



def get_lead_info():
    #website  - make sure to get .text
    web = driver.find_element_by_link_text('Website')
    website = web.get_attribute('href')

    #company url
    menu_buttons = driver.find_element_by_class_name('right-actions-overflow-menu-trigger')
    ac = ActionChains(driver)
    ac.move_to_element(menu_buttons).move_by_offset(0,100).click().perform()
    company_url = clipboard.paste()

    driver.execute_script("window.history.go(-1)")
    time.sleep(2)



log_in_sales_nav()
keyw = 'dentist'
file_name = "dentists_sales_nav_beta.csv"
search_leads(keyw)
traverse_leads_page_one()
traverse_leads()


