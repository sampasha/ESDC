#!/usr/bin/env python


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from parsel import Selector
from collections import defaultdict
import json
import time

def get_registry_data(companyname):
    # specifies the path to the chromedriver.exe
    driver = webdriver.Chrome('chromedriver')
    # driver.get method() will navigate to a page given by the URL address
    driver.get('https://beta.canadasbusinessregistries.ca/search')

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@class='btn btn-primary action action__accept']"))).click()
    search_bar = driver.find_element_by_id('searchTerm')
    search_bar.send_keys(companyname)

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@class='search-field__btn btn btn-info btn-lg']"))).click()

    time.sleep(4)
    sel = Selector(text=driver.page_source)

    card = driver.find_elements_by_xpath(
        ( "//div[@class='primary-card__inner']")
      )
    ls = ['Business Number', 'Registry Id', 'Registered Office Number', 'Status', 'Created']
    dict1 = dict((el,"Not Found") for el in ls)

    js = None
    for i in card:
        m = i.text.split("\n")

        if m:
            for k in m:
                if "Business Number" in k:
                        dict1['Business Number'] = k.split(":")[1].strip()

                if "Registry ID" in k:
                        dict1['Registry Id'] = k.split(":")[1].strip()
            
                if "Registered Office Number" in k:
                        dict1['Registered Office Number'] = k.split(":")[1].strip()

                if "Status" in k:
                        dict1['Status'] = k.split(":")[1].strip()

                if "Created" in k:
                        dict1['Created'] = k.split(":")[1].strip()


    return dict1
