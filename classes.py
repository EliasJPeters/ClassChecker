class Statistics:
    #Initially declaring the variables to be their default values
    timesAttempted = 0
    timesOpen = 0
    timesFailed = 0
    timesSuccessful = 0
    registrationSuccessful = False

    #Used when creating the object that is using the Statistics Class Structure
    def __init__(self, attempted, open, failed, successful, isSuccess) -> None:
        self.timesAttempted = attempted 
        self.timesOpen = open
        self.timesFailed = failed
        self.timesSuccessful = successful
        self.registrationSuccessful = isSuccess

class userInfo:
    #Assigns the variables that accompany the object created with the userInfo class structure
    def __init__(self, email, password, CRN, operationMode, courseNumber) -> None:
        self.userEmail = email
        self.userPassword = password
        self.userCRN = CRN
        self.userOperationMode = operationMode
        self.userCourseNumber = courseNumber

    def printUserInfo(self):
        print("UserEmail:    ", self.userEmail)
        print("UserPassword: ", self.userPassword)
        print("UserCRN:      ", self.userCRN)
