#!/usr/bin/env python

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from parsel import Selector
from collections import defaultdict
import json
import time

def get_linkedin_info(business_name):
    main = []
    info_final=[]
    dict1 = defaultdict()
    js = None
    driver = webdriver.Chrome('chromedriver')
    driver.get('https://www.linkedin.com')
    username = driver.find_element_by_id('session_key')
    username.send_keys('spasha@sfu.ca')
    passw = driver.find_element_by_id('session_password')
    passw.send_keys('Sameer123')
    log_in_button = driver.find_element_by_class_name('sign-in-form__submit-button')
    log_in_button.click()
    driver1 = webdriver.Chrome('chromedriver')
    driver1.get("https://www.google.com")
    search_query = driver1.find_element_by_name('q')
    search_query.send_keys('site:linkedin.com/company/ AND '+business_name)
    search_query.send_keys(Keys.RETURN)
    if search_query:
        url1 = driver1.find_elements_by_tag_name('a')
        if url1:
            linkedin_urls = [url.get_attribute('href') for url in url1]
            if linkedin_urls:
                for i in linkedin_urls:
                    if i and "https://ca.linkedin.com" in i:
                        main.append(i)
                        if main:

                            driver.get(main[0]+"/about/")
                            time.sleep(0.5)
                            sel = Selector(text=driver.page_source) 
                            website = sel.xpath('//*[starts-with(@class, "org-page-details__definition-text t-14 t-black--light t-normal")]/a/@href').extract_first()
                            info1 = sel.xpath('//*[starts-with(@class, "org-page-details__definition-term t-14 t-black t-bold")]/text()').extract()
                            info = sel.xpath('//*[starts-with(@class, "org-page-details__definition-text t-14 t-black--light t-normal")]/text()').extract()
                            employee_details = sel.xpath('//*[starts-with(@class, "org-page-details__employees-on-linkedin-count t-14 t-black--light mb5")]/text()').extract_first()

                            for i in info:
                                if i.strip():
                                    info_final.append(i)

                            info_final=[]
                            for i in info:
                                if i.strip():
                                    info_final.append(i.strip())
                            label=[]
                            for i in info1:
                                if i.strip():
                                    label.append(i.strip())
                                    
                            dict1 = defaultdict()
                            s= 0
                            if info_final:
                                if "Industry" in label:
                                    dict1['industry'] = info_final[0].strip()
                                    s += 1
                                else:
                                    dict1['industry'] = ""
                                if "Headquarters" in label:
                                    dict1['Headquarters'] = info_final[1].strip()
                                    s += 1
                                else:
                                    dict1['Headquarters']=""
                                    
                                if "Type" in label:
                                    dict1['Type'] = info_final[2].strip()
                                    s += 1
                                else:
                                    dict1['Type'] = ""
                                if "Founded" in label:
                                    dict1['Founded'] = info_final[3].strip()
                                    s += 1
                                else:
                                    dict1['Founded'] = ""
                            if employee_details:    
                                dict1['Company size'] = employee_details.strip()
                                s += 1
                            else:
                                dict1['Company size'] = ""
                            dict1['Score'] = s
                                                            
                            
    driver.quit()
    driver1.quit()
    #return dict
    return dict1



