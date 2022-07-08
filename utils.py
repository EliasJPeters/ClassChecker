from unicodedata import numeric
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import os
import keyboard
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.command import Command
from selenium.common.exceptions import NoSuchElementException,ElementNotInteractableException
from selenium.webdriver.support.ui import Select
from classes import *

#Getting the User's credentials
def setCredentials(userEmail, userPassword, userCRN):
    #userEmail = input("Enter USF Email: ")
    #userPassword = input("Enter USF Password (Your password is not stored! There's no security risk!): ")

    validCRN = False
    #while not validCRN:
        #userCRN = input("Enter the desired class's CRN: ")
        #Making sure CRN is all numeric and has 5 digits
        #if userCRN.isdigit() and len(userCRN) == 5:
         #   validCRN = True
        #else:
         #   clear() #Clears Console
          #  print("CRN entered not valid. Please input valid CRN. CRN must be 5 digits and all numeric.")
    #Creating student object from class structure
    studentInfo = userInfo(userEmail, userPassword, userCRN)
    return studentInfo
        
def openSite(driver, window):
    windowHandle = driver.current_window_handle
    driver.switch_to.window(windowHandle)
    #driver.minimize_window()
    driver.set_window_size(1500, 950)
    driver.set_window_position(10, 10, windowHandle='current')
    website = "https://my.usf.edu/myusf/home_myusf/index"
    driver.get(website)
    window.refresh()
    time.sleep(2.5)

def login(driver, studentInfo,window):
    emailArea = driver.find_element_by_id("i0116")
    window["-OUTPUT-"].update("Entering Email...")
    window.refresh()
    # print("Entering Email...")
    emailArea.send_keys(studentInfo.userEmail)
    time.sleep(1)
    #Clicking enter
    enterKey = driver.find_element_by_id("idSIButton9")
    enterKey.send_keys(Keys.RETURN)
    time.sleep(2)
    window["-OUTPUT-"].update("Entering Password...")
    window.refresh()
    #print("Entering Password...")
    passwordArea = driver.find_element_by_id('i0118')
    passwordArea.send_keys(studentInfo.userPassword)
    time.sleep(1)
    enterButton = driver.find_element_by_id("idSIButton9")
    enterButton.send_keys(Keys.RETURN)

def Authenticator(driver, window):
    #https://login.microsoftonline.com/741bf7de-e2e5-46df-8d67-82607df9deaa/login
    time.sleep(2)
    stillOnPage = True
    window["-OUTPUT-"].update("Please complete Microsoft Authenticator")
    window.refresh()
    while stillOnPage:
        #time.sleep(3)
        if (driver.current_url != "https://my.usf.edu/myusf/home_myusf/index"):
            #print("Please use the window to input your Microsoft Authenticator Code.")
            #time.sleep(2)
            pass
        elif (driver.current_url == "https://my.usf.edu/myusf/home_myusf/index"):
            #print("On MyUSF home page")
            window["-OUTPUT-"].update("Authenticator complete...")
            window.refresh()
            stillOnPage = False
        else:
            print("Unknown Page.")
    

def myUSFNavigation(driver,window):
    correctPage = False
    time.sleep(2)
    while not correctPage:
        if (driver.current_url == "https://my.usf.edu/myusf/home_myusf/index"):
            correctPage = True
            window["-OUTPUT-"].update("At MyUSF homepage...")
            window.refresh()
        else:
            pass
            #print("Please navigate to the MyUSF Homepage. Url: https://my.usf.edu/myusf/home_myusf/index")
    #clear()
    window["-OUTPUT-"].update("Clicking My Resources...")
    window.refresh()
    #print("Clicking My Resources...")
    myResources = driver.find_element_by_id("kgoui_page_navigation_header_section_my_resources_menu_trigger")
    myResources.click()
    time.sleep(1)
    window["-OUTPUT-"].update("Clicking Oasis...")
    window.refresh()
    #print("Clicking Oasis...")
    oasis = driver.find_element_by_xpath("/html/body/header/div[7]/div/div/ul/li[10]/a")
    oasis.click()

def oasisNavigation(driver, window):
    time.sleep(5)
    p = driver.current_window_handle
    parent = driver.window_handles[0]
    chld = driver.window_handles[1]
    driver.switch_to.window(chld)
    window["-OUTPUT-"].update("Clicking Student...")
    window.refresh()
    #print("Clicking Student...")
    studentLink = driver.find_element_by_partial_link_text("udent")
    studentLink.click()
    time.sleep(1)
    window["-OUTPUT-"].update("Clicking Registration...")
    window.refresh()
    #print("Clicking Registration...")
    registrationLink = driver.find_element_by_link_text("Registration")
    registrationLink.click()
    time.sleep(2)
    #Clicking on register for classes
    window["-OUTPUT-"].update("Clicking Register, Add, Or Drop Classes...")
    window.refresh()
    #print('Clicking Register, Add or Drop Classes...')
    registerforClass = driver.find_element_by_link_text("Register, Add or Drop Classes")
    registerforClass.click()
    # Submit button for registration term
    driver.find_element_by_xpath("/html/body/div[3]/form/input").click()

def registerClasses(driver,studentInfo, window):
    time.sleep(2)
    #Scroll to bottom of page
    window["-OUTPUT-"].update("Scrolling Down...")
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)
    #Inputting CRN
    window["-OUTPUT-"].update("Entering CRN...")
    try:
        driver.find_element_by_id("crn_id1").click()
        driver.find_element_by_id("crn_id1").send_keys(studentInfo.userCRN)
        #ENABLE THIS FOR BUILD
        #driver.find_element_by_id("crn_id1").send_keys(Keys.RETURN)
    except NoSuchElementException:
        window["-OUTPUT-"].update("Place to input course number not found...")
        print("Input Course Number Not Found")

def identifyErrorText(driver, timesFailed, timesSuccessful):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    try:
        errorPresent = driver.find_element_by_class_name("errortext")
        print("Class Not Registered. Still Closed.\n")
        successful = False
        timesFailed += 1
    except NoSuchElementException:
        print("Error not detected, class registered?")
        successful = True
        timesSuccessful += 1
    return successful, timesFailed, timesSuccessful

def loopedCheck(driver, timesFailed, timesSuccessful):
    time.sleep(1)
    driver.back()
    time.sleep(300)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)
    clear()
    try:
        driver.find_element_by_id("crn_id1").send_keys(Keys.RETURN)
        print("Attempting...")
    except NoSuchElementException:
        print("Cant Find Button On loop")
    time.sleep(2)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(.5)
    registrationSuccessful, timesFailed, timesSuccessful = identifyErrorText(timesFailed, timesSuccessful)
    return registrationSuccessful, timesFailed, timesSuccessful

def refresh(driver):
    time.sleep(1)
    driver.refresh()

def clear(): os.system('cls')
