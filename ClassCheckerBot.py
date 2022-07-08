from utils import *
from interface import *

#creates object called "studentInfo" from the userInfo Class
#Establishes user email, password, class CRN

#Potential to make multiple class entries at once, meaning students
#could theoretically schedule their whole semester in one attempt, or
#attempt to schedule more than one closed class in general.
#Would then need to differentiate what classes were successfully registered
#and what classes failed to do so

createGUI()

#studentInfo = setCredentials()

#print("Launching Firefox. One moment...")
#driver = webdriver.Firefox()
#openSite(driver)
#login(driver, studentInfo)
#Authenticator(driver)
#myUSFNavigation(driver)
#oasisNavigation(driver)
#registerClasses(driver, studentInfo)



#identifyErrorText(timesFailed, timesSuccessful)

#leave = False
#while not leave:
    #registrationSuccessful, timesFailed, timesSuccessful = loopedCheck(timesFailed, timesSuccessful)
    #Statistics.timesAttempted += 1 
    #print("Times Attempted:         ", Statistics.timesAttempted)
    #print("Times Failed:            ", Statistics.timesFailed)
    #print("Times Successful:        ", Statistics.timesSuccessful)
    #print("Registration Successful: ", Statistics.registrationSuccessful, "\n")
    
#NEXT STEP, SO STATISTICS AND DETECTION OF CLASS REGISTRATION