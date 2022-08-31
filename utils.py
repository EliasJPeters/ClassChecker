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
def setCredentials(userEmail, userPassword, userCRN, operationMode, userCourseNumber):
    #Creating student object from class structure
    studentInfo = userInfo(userEmail, userPassword, userCRN, operationMode, userCourseNumber)
    return studentInfo
        
def openSite(driver, window):
    windowHandle = driver.current_window_handle
    driver.switch_to.window(windowHandle)
    #driver.minimize_window()
    driver.set_window_size(1500, 850)
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
    #Clicked Oasis
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
    # Submit button for term
    driver.find_element_by_xpath("/html/body/div[3]/form/input").click()

def oasisNavigationForClassStatus(driver, window):
    time.sleep(5)
    p = driver.current_window_handle
    parent = driver.window_handles[0]
    chld = driver.window_handles[1]
    driver.switch_to.window(chld)
    window["-OUTPUT-"].update("Clicking Student...")
    studentLink = driver.find_element_by_partial_link_text("udent")
    studentLink.click()
    time.sleep(1)
    window["-OUTPUT-"].update("Clicking Registration...")
    registrationLink = driver.find_element_by_link_text("Registration")
    registrationLink.click()
    time.sleep(2)
    #Clicking on register for classes
    window["-OUTPUT-"].update("Clicking Class Schedule Search...")
    classScheduleSearch = driver.find_element_by_link_text("Class Schedule Search")
    classScheduleSearch.click()
    time.sleep(1)
    #fall2022 option
    window["-OUTPUT-"].update("Selecting Fall2022 Term")
    select = Select(driver.find_element_by_name('p_term'))
    select.select_by_value('202208')
    # Submit button for semester term
    driver.find_element_by_xpath("/html/body/div[3]/form/input[2]").click()

def inputCourseNumber(driver, window, studentInfo):
    driver.find_element_by_id("crse_id").click()
    driver.find_element_by_id("crse_id").send_keys(studentInfo.userCourseNumber)
    time.sleep(1)
    #Scroll to bottom of page
    window["-OUTPUT-"].update("Scrolling Down...")
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)
    #Clicking limit to open sections only
    window["-OUTPUT-"].update("Expanding Search to All Sections...")
    driver.find_element_by_id("open_only").click()
    time.sleep(1)
    #Clicking the submit button
    window["-OUTPUT-"].update("Clicking Section Search...")
    driver.find_element_by_name("SUB_BTN").click()
    time.sleep(2)
    try:
        driver.find_element_by_partial_link_text(studentInfo.userCRN).click()
        if NoSuchElementException:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            window["-OUTPUT-"].update("Scrolling down to find CRN...")
            time.sleep(1)
            driver.find_element_by_partial_link_text(studentInfo.userCRN).click()
            if NoSuchElementException:
                #window["-OUTPUT-"].update("Did not find a CRN to click.")
                pass
        time.sleep(2)
        #driver.find_element_by_partial_link_text(studentInfo.userCRN).click()
    except:
        pass
        window["-OUTPUT-"].update("Error: Did not search for CRN to click.")
    
        
def readingSeatData(driver, window):
    totalSeatCapacity = (driver.find_element_by_xpath("/html/body/div[3]/table[1]/tbody/tr[2]/td/table/tbody/tr[2]/td[1]").text)
    availableSeatsNormal = (driver.find_element_by_xpath("/html/body/div[3]/table[1]/tbody/tr[2]/td/table/tbody/tr[2]/td[3]").text)
    print("Total Seats:" ,totalSeatCapacity)
    print("Available Seats: ", availableSeatsNormal)
    time.sleep(1)
    window["-OUTPUT-"].update("Total Seats: " + totalSeatCapacity + "\n" + "Available Seats: " + availableSeatsNormal)
    if (availableSeatsNormal == 0):
        refresh(driver)
        #Working on refresh of the info reading
    

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
        #Still not working because of hold on registration
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
