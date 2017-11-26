import selenium
import time
from selenium import webdriver
import os
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
import csv
import requests
import pandas as pd


driver = webdriver.Firefox()
###Change file to your search word file
data = pd.read_csv('SearchWord_tweets.csv')


IDs = (data['ID'].values)  # as a numpy arra


for ID in IDs:
    print(ID)
    url = "https://twitter.com/statuses/"+str(ID)
    driver.get(url)
    driver.save_screenshot("Screenshots/"+str(ID)+"_.png")
    time.sleep(4)
