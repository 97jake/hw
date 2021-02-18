# -*- coding: utf-8 -*-
"""
Created on Mon Feb 15 19:22:07 2021

@author: 97jak
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options


import time
import os
import re


"""Get my password from a text file so that no one else can see it"""
with open('password.txt') as file:
    myPassword = file.read()


def submit_assignment(file_name,assignment_number,class_number):
    """

    Parameters
    ----------
    file_name (str): Name of the hw file to be submitted 
    assignment_number (str) : Specific number of the hw
        example: '8.3' for Volume 1 or '13' for Volume 2
    class_number (str): '1' or '2' representing Volume 1 or 2

    Raises
    ------
    ValueError for incorrect class number

    Returns
    -------
    None.

    """
    
    """Create the file path to the appropriate homework folder"""
    if class_number == "1":
        assignment_to_submit = os.path.join(os.getcwd(),'Volume_1\{}'.format(file_name))
    elif class_number == "2":
        assignment_to_submit = os.path.join(os.getcwd(),'Volume_2\{}'.format(file_name))
    else:
        raise ValueError("Invalid Class Number")
    
    """Here I open a Chrome session. The experimental options allow me to keep the browser
    open """
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    driver = webdriver.Chrome("C:/Users/97jak/Downloads/chromedriver_win32/chromedriver.exe",options=chrome_options)
    
    driver.get('https://www.gradescope.com/')
    
    """Finds the login button and Logs into gradescope.com using my credentials"""
    login = driver.find_element_by_xpath('/html/body/div/main/div[2]/div/header/nav/div[2]/span[3]/button')
    login.click()
    
    email = driver.find_element_by_id('session_email')
    password = driver.find_element_by_id('session_password')
    
    email.send_keys('97jake@gmail.com')
    password.send_keys(myPassword)
    
    session_login = driver.find_element_by_xpath('//*[@id="login-modal"]/div/div[1]/form/div[4]/input')
    session_login.click()
    
    
    """Find and select the appropriate button corresponding to the correct class"""
    if class_number == 2:
        vol_2 = driver.find_element_by_xpath('//*[@id="account-show"]/div[1]/div[1]/a[1]')
        vol_2.click()
        
        assignment_name = "'Homework {}'".format(assignment_number)
        assignment = driver.find_element_by_xpath('//button[text()={}]'.format(assignment_name))
        assignment.click()
        
    else:
        vol_1 = driver.find_element_by_xpath('//*[@id="account-show"]/div[1]/div[1]/a[2]')
        vol_1.click()
        
        assignment_name = "'HW {}'".format(assignment_number)
        assignment = driver.find_element_by_xpath('//button[text()={}]'.format(assignment_name))
        assignment.click()
        
    
    """Find input element and sends the homework assignment to be submitted"""
    submit_pdf = driver.find_element_by_id('submit-variable-length-pdf')
    submit_pdf.click()
    
    select_pdf = driver.find_element_by_id('submission_pdf_attachment')
    select_pdf.send_keys(assignment_to_submit)
    
    """Submits homework assignment"""
    submit = driver.find_element_by_id('submit')
    submit.click()
    

"""This part of the code detects when either homework folder has 
changed and runs submit_assignment automatically"""
before1 = os.listdir("Volume_1")
before2 = os.listdir("Volume_2")


"""Here we have a regular expression pattern to get the assignment number from
the assignment name"""
get_numbers = re.compile("([0-9]{1,2})")

while True:
    time.sleep(10)
    after1 = os.listdir("Volume_1")
    after2 = os.listdir("Volume_2")
    
    added1 = [f for f in after1 if not f in before1]
    added2 = [f for f in after2 if not f in before2]
    
    if len(added1) != 0:
        file_name = added1[0]
        nums = get_numbers.findall(file_name)
        assignment_number = "{}.{}".format(nums[0],nums[1])
        submit_assignment(file_name,assignment_number,'1')
    
    if len(added2) != 0:
        file_name = added2[0]
        nums = get_numbers.findall(file_name)
        assignment_number = "{}.{}".format(nums[0],nums[1])
        submit_assignment(file_name,assignment_number,'2')
    
    before1 = after1
    before2 = after2
