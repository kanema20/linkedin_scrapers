from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

#import parameters
import time
from parsel import Selector
import csv
import os
import random
import pandas as pd

driver = webdriver.Chrome('/Users/kanem/chromedriver')
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')


def validate_field(field):
	if (field == ""):
		field = 'no results'
		return field
	else:
		return field

def log_in_sales_nav(): #log in to linkedin and go to sales navigator
    driver.get('https://www.linkedin.com/login?trk=guest_homepage-basic_nav-header-signin')
    username = driver.find_element_by_id('username')
    username.send_keys('kanema20@gmail.com')
	#username.send_keys('kobirapu@gmail.com')
    time.sleep(0.5)
    
    password = driver.find_element_by_id('password')
	#password.send_keys('bl73yo8thld')
    password.send_keys('Tesla2020')
    log_in = driver.find_element_by_tag_name('button')
    log_in.click()
    time.sleep(0.5)

    driver.get('https://www.linkedin.com/sales/homepage')

def search_leads(keyw):
    all_filters = driver.get('https://www.linkedin.com/sales/search/people?viewAllFilters=true')
    all_filters.click()

    search_page = driver.get('https://www.linkedin.com/sales/search/people')

    keyword_filter = driver.find_element_by_xpath('//div/main/div/form/div/div/div/div/div/div/input')
    keyword_filter.send_keys(keyw)
    time.sleep(3)

    #seniority_level = driver.find_element_by_xpath('//section/ul/li[3]/div/div/div/div/label')
    seniority_level =  driver.find_element_by_xpath('//form/ul/li[9]/div/div/div/div')
    seniority_level.click()

    owner = driver.find_element_by_xpath('//div/div/ol/li[1]/button')
    owner.click()
    time.sleep(2)
    cxo = driver.find_element_by_xpath('//div/div/ol/li[1]/button')
    cxo.click()
    time.sleep(2)
    partner = driver.find_element_by_xpath('//div/div/ol/li[1]/button')
    partner.click()
    time.sleep(2)

def traverse_leads():
    

log_in_sales_nav()
keyw = 'dentist'
search_leads(keyw)
traverse_leads()

