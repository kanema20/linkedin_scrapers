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


def validate_field(field):
	if (field == ""):
		field = 'no results'
		return field
	else:
		return field

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

def search_leads(keyw):
    search_page = driver.get('https://www.linkedin.com/sales/search/people')
    time.sleep(2)
    #keyword_filter = driver.find_element_by_class_name('search-filter-keywords-typeahead').click()
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
    #we could do by state
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
    print("search is set up")

def traverse_leads_page_one(file_name):
    #refactoring code to write the csv row after each call to get_leads_info()
    print('time to traverse page 1')
    with open(file_name, 'w', encoding='utf-8', newline='') as open_file:
        time.sleep(1)
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight/80)")
        time.sleep(SCROLL_PAUSE_TIME)
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight/12)")
        time.sleep(SCROLL_PAUSE_TIME)
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight/10)")
        time.sleep(SCROLL_PAUSE_TIME)
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight/8)")
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
            writer = csv.writer(open_file)
            writer.writerow(get_lead_info(x, lead_count)) 
    

def traverse_leads(file_name):
    last_page = driver.find_element_by_xpath('//section/div[2]/nav/ol/li[11]/button').text
    lead_count = 1
    page_count = 1
    #for x in range(int(last_page)):
    with open(file_name, 'w', encoding='utf-8', newline='') as open_file:
        print("time to traverse")
        writer = csv.writer(open_file)

        writer.writerow(["first_name", "last_name", "jobtitle", "employeecompany",
                        "lead_salesnav_page", "company_salesnav_page",
                        "city", "state", "country"])

        for x in range(int(last_page)):
            next_page()
            time.sleep(1)
            driver.execute_script("window.scrollTo(0,document.body.scrollHeight/82)")
            time.sleep(SCROLL_PAUSE_TIME)
            driver.execute_script("window.scrollTo(0,document.body.scrollHeight/12)")
            time.sleep(SCROLL_PAUSE_TIME)
            driver.execute_script("window.scrollTo(0,document.body.scrollHeight/10)")
            time.sleep(SCROLL_PAUSE_TIME)
            driver.execute_script("window.scrollTo(0,document.body.scrollHeight/8)")
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
                writer.writerow(get_lead_info(x, lead_count))

def get_lead_info(x, lead_count):
    #get leads name          
        try:  
            name = driver.find_elements_by_class_name("result-lockup__name")[x].text
            print(name)
            #first name          
            first_last = name.split(" ", 1)
            first_name = first_last[0]
            #last name
            last_name = first_last[1]
            lead_snp = driver.find_element_by_link_text(name)
        #get leads sales nav profile 
            lead_sales_page = lead_snp.get_attribute('href')
            print(lead_sales_page)
        except NoSuchElementException:
            name = "NONE" 
            print("Error: No name")
        
        location = driver.find_elements_by_class_name('result-lockup__misc-item')[x].text
        comma_locations = [m.start(0) for m in re.finditer(',', location)]
        country = "United States"
    #get location - handle variation
        try:
            city =  location[:comma_locations[0]]
            state = location[comma_locations[0]+2: comma_locations[1]]
            print("City: "+ city)
            print("State: " + state)
            print("Country: " + country)
        except IndexError:
            city = location
            state = "None"
            print("City: " + city)
            print("State: " + state)
            print("Country: "+ country)

        #get leads job title
            
        try:
            job_title = driver.find_elements_by_class_name("result-lockup__highlight-keyword")[x].text
            job_truncate = job_title.find('at')
            job_title = job_title[:job_truncate]
            print("Job Title: " + job_title)
        except IndexError:
            print('Error: job title cannot be truncated')            

    #get leads company - clean up this later
        try:
            company = driver.find_elements_by_class_name("result-lockup__position-company")[x].text
            company_truncate = company[:company.find('\n')] #truncate string to only have company name
            print("Company: " + company_truncate)

            company_link = driver.find_element_by_link_text(company)
            company_sales_nav_page = company_link.get_attribute('href')
            print("Company Sales Nav Page: " + company_sales_nav_page)
        except NoSuchElementException:
            print("error: no company")
                
    #keep track of lead count
        print("# of leads: " + str(lead_count))
        lead_count = lead_count + 1

    #validate fields
        first_name = validate_field(first_name)
        last_name = validate_field(last_name)
        jobtitle = validate_field(job_title)
        employeecompany = validate_field(company_truncate)
        lead_salesnav_page = validate_field(lead_sales_page)
        company_salesnav_page = validate_field(company_sales_nav_page)
        city = validate_field(city)
        state = validate_field(state)
        country = validate_field(country)

        list_of_elem = [first_name, last_name, jobtitle, employeecompany,
                        lead_salesnav_page, company_salesnav_page,
                        city, state, country]
        
        return list_of_elem
        
 

def next_page():
    #go to next page of sales nav results
    #up to page 6
    #then page 7, 4 on each side
    nextpage = driver.find_element_by_class_name('search-results__pagination-next-button')
    nextpage.click()

#execution!!!!!
log_in_sales_nav()


keyw = 'dentist'
file_name = "dentists_sales_nav_beta.csv"

#with open(file_name, 'w', encoding='utf-8', newline='') as open_file:
#    writer = csv.writer(open_file)
#    writer.writerow(['name', 'jobtitle', 'employeecompany', 'personal_salesnav_page', 'company_salesnav_page','city', 'state','country'])

search_leads(keyw)
traverse_leads_page_one(file_name)
traverse_leads(file_name)


