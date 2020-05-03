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

def validate_field(field):
	if (field == ""):
		field = 'no results'
		return field
	else:
		return field


file_name = ''

#