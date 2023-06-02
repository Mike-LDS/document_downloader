from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import shutil
import os
import time
import csv

families = []
students = []

with open('test_users (1).csv',newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        line = [row['\ufeffID'], row['First name']+' '+row['Last name']]
        families.append(line)

with open('test_users.csv',newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        line = [row['\ufeffID'], row['First name']+' '+row['Last name'], row['Client ID'], row['Client Name']]
        students.append(line)

path = os.getcwd()
parent = os.path.dirname(path)

# Accessing TutorCruncher

driver = webdriver.Chrome()
driver.get('https://secure.tutorcruncher.com/')
driver.find_element('id','id_username').send_keys('At@ldsociety.ca')
driver.find_element('id','id_password').send_keys('wz8vv_3Fb66QaNx')
driver.find_element('id','email-signin').click()

# Downloading Family Account Documents

for family in families:
    print(family)
    new_path = path +'/'+ family[0] +' '+ family[1]
    os.mkdir(new_path)

    driver.get('https://secure.tutorcruncher.com/docs/?role='+family[0])
    links = driver.find_elements('xpath','//table//tbody/tr/td/a')
    
    for index in range(0,len(links)):
        links = driver.find_elements('xpath','//table//tbody/tr/td/a')
        if (index%2) == 0:
            links[index].click()
            d_elem = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME,'doc-download-link')))
            file_name = driver.find_element(By.TAG_NAME,'h1').text
            if not('Notice of Assessment' in file_name or 'NOA ' in file_name):
                d_elem.click()
                d_link = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT,'Click here to download')))
                d_link.click()
            driver.back()
            time.sleep(2)

    
    files = os.listdir(parent+'/Downloads')
    for file in files:  
        shutil.move(parent+'/Downloads/'+file, new_path+'/'+file)

# Downloading Student Account Documents       

for student in students:
    print(student)
    new_path = path +'/'+ student[2] +' '+ student[3]+'/'+student[0] +' '+ student[1]
    os.mkdir(new_path)

    driver.get('https://secure.tutorcruncher.com/docs/?role='+student[0])
    links = driver.find_elements('xpath','//table//tbody/tr/td/a')
    
    for index in range(0,len(links)):
        links = driver.find_elements('xpath','//table//tbody/tr/td/a')
        if (index%2) == 0:
            links[index].click()
            d_elem = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME,'doc-download-link')))
            file_name = driver.find_element(By.TAG_NAME,'h1').text
            if not('Notice of Assessment' in file_name or 'NOA ' in file_name):
                d_elem.click()
                d_link = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT,'Click here to download')))
                d_link.click()
            driver.back()
            time.sleep(2)

    files = os.listdir(parent+'/Downloads')
    for file in files:  
        shutil.move(parent+'/Downloads/'+file, new_path+'/'+file)
    
driver.close()
