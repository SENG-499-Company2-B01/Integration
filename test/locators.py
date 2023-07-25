from selenium.webdriver.common.by import By

class LoginPageLocators(object):
    NETLINK_INPUT = (By.XPATH, '//input[1]')
    PASSWORD_INPUT = (By.XPATH, '//input[2]')
    SIGNIN_BUTTON = (By.XPATH, "//div[text()='SIGN IN']/parent::button")
    FORGOT_PASSWORD_LINK = (By.XPATH, "//div[contains(text(),'Forgot your')]")

class ProfLandingPageLocators(object):
    SCHED_PREF_NAVBAR = (By.XPATH, "//div[text()='SCHEDULING PREFERENCES']")
    SET_PREF_BUTTON = (By.XPATH, "//div[text()='SET YOUR PREFERENCES']")
    USER_MENU_BUTTON = (By.XPATH, "(//button)[1]")
    SIGN_OUT_BUTTON = (By.XPATH, "//button[text()='Sign out']")

class ProfPrefPageLocators(object):
    SEMESTER_FALL_RADIO = (By.XPATH, "//span[text()='Fall']")
    SEMESTER_WINTER_RADIO = (By.XPATH, "//span[text()='Winter']")
    SEMESTER_SUMMER_RADIO = (By.XPATH, "//span[text()='Summer']")
    ABLE_TO_TEACH_RADIO_YES = (By.XPATH, "//input[@value='Yes']")
    ABLE_TO_TEACH_RADIO_NO = (By.XPATH, "//input[@value='No']")
    ABLE_TO_TEACH_TEXTBOX = (By.ID, "preference_reason")
    PREF_TIME_START = (By.XPATH, "//input[@placeholder='Start Time']")
    PREF_TIME_END = (By.XPATH, "//input[@placeholder='End Time']")
    PREF_CLASS_SIZE = (By.ID, "preference_classSize")
    CLASS_FORMAT_ONCE = (By.XPATH, "//span[text()='Once/Week']/preceding-sibling::span/input")
    CLASS_FORMAT_MR = (By.XPATH, "//span[text()='M, R']/preceding-sibling::span/input")
    CLASS_FORMAT_TWF = (By.XPATH, "//span[text()='T, W, F']/preceding-sibling::span/input")
    CLASS_FORMAT_ONLINE = (By.XPATH, "//span[text()='Online']/preceding-sibling::span/input")
    PREF_CLEAR_BUTTON = (By.XPATH, "//span[text()='CLEAR']/parent::button")
    PREF_CANCEL_BUTTON = (By.XPATH, "//span[text()='CANCEL']/parent::button")
    PREF_SUBMIT_BUTTON = (By.XPATH, "//span[text()='SUBMIT']/parent::button")

class AdminLandingPageLocators(object):
    VIEW_SCHED_LINK = (By.XPATH, "//a[@href='/timetable']")
    CREATE_ACCT_LINK = (By.XPATH, "//a[@href='/CreateAccountPage']")
    VIEW_PREF_LINK = (By.XPATH, "//a[@href='/Preferences']")
    USER_MENU_BUTTON = (By.XPATH, "(//button)[1]")
    SIGN_OUT_BUTTON = (By.XPATH, "//button[text()='Sign out']")



class GenerateSchedulePageLocators(object):
    START_GEN_BUTTON = (By.XPATH, "//div[text()='GENERATE SCHEDULE']/parent::button")
    TERM_SELECT_DROPDOWN = (By.XPATH, "//*[text()='Select']/parent::div")
    TERM_SELECT_ITEM = lambda sem: (By.XPATH, f"//li[@value='{sem}']")
    SCHEDULE_CALENDAR = (By.CLASS_NAME, "rbc-calendar")

class CreateAccountPageLocators(object):
    EMAIL_FIELD = (By.ID, "createAccount_email")
    FIRSTNAME_FIELD = (By.ID, "createAccount_firstName")
    LASTNAME_FIELD = (By.ID, "createAccount_lastName")
    EXPERTISE_FIELD = (By.ID, "createAccount_fieldOfExpertise")
    EXPERIENCE_FIELD = (By.ID, "createAccount_yearsOfExperience")
    EDUCATION_FIELD = (By.ID, "createAccount_highestEducationObtained")
    PASSWORD_FIELD = (By.ID, "createAccount_password")
    CONFIRMEDPASSWORD_FIELD = (By.ID, "createAccount_confirmedPassword")
    CLEAR_BUTTON = (By.XPATH, "//span[text()='CLEAR']/parent::button")
    CANCEL_BUTTON = (By.XPATH, "//span[text()='CANCEL']/parent::button")
    CREATE_BUTTON = (By.XPATH, "//span[text()='CREATE']/parent::button")
