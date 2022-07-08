from faulthandler import disable
from tkinter import CENTER, LEFT, RIGHT
from webbrowser import BackgroundBrowser
import PySimpleGUI as sg
from matplotlib.pyplot import margins
from utils import *
from classes import *
import time

#All the stuff in the window

def createGUI():
    layout = [[sg.Text("Enter USF Email:", size = (13,1), justification=RIGHT, background_color="Black") , sg.InputText(justification = LEFT)],
            [sg.Text("Enter password:" , size = (13,1), justification=RIGHT, background_color="Black") , sg.InputText(justification = LEFT, password_char='*')],
            [sg.Text("Class CRN:", size = (13,1), justification=RIGHT, background_color="Black"), sg.InputText(justification=LEFT)],
            [sg.Text("Status:", size = (13,1), justification=RIGHT, background_color="Black"), sg.Multiline(size = (45,1), disabled = True, justification= LEFT , key = '-OUTPUT-', auto_refresh=True, no_scrollbar = True, 
            background_color='White')],
            [sg.Button("Submit", size = (13,1)), ]]

    #Creates the window and sets theme
    #sg.theme('DarkAmber')
    window = sg.Window("ClassChecker", layout, margins = (50,50), keep_on_top = True, location = (1000,400), grab_anywhere= False, background_color="Black")

    while True:
        event, values = window.read(timeout = 30)
        if event == sg.WIN_CLOSED:
            window.close()
            break
        elif event == "Submit":
            validCRN = False
            if values[2].isdigit() and len(values[2]) == 5:
                validCRN = True
                studentInfo = setCredentials(values[0], values[1], values[2])
                #studentInfo.printUserInfo()
                window["Submit"].update(disabled = True)
                window["-OUTPUT-"].update("Launching Firefox...")
                time.sleep(1)
                driver = webdriver.Firefox()
                time.sleep(1)
                openSite(driver,window)
                time.sleep(1)
                login(driver, studentInfo, window)
                Authenticator(driver, window)
                myUSFNavigation(driver, window)
                oasisNavigation(driver, window)
                registerClasses(driver, studentInfo, window)
            elif not validCRN:
                sg.popup("Class CRN not valid. CRN must be numeric and 5 digits.", title = "Invalid CRN", keep_on_top = True)
                #clear() #Clears Console
                #print("CRN entered not valid. Please input valid CRN. CRN must be 5 digits and all numeric.")
    #print(values)
    window.close()
    driver.quit()
