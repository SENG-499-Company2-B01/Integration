from selenium.webdriver.common.by import By

class LoginPageLocators(object):
    NETLINK_INPUT = (By.XPATH, '//input[1]')
    PASSWORD_INPUT = (By.XPATH, '//input[2]')
    SIGNIN_BUTTON = (By.XPATH, "//div[text()='SIGN IN']/parent::button")
    FORGOT_PASSWORD_LINK = (By.XPATH, "//div[contains(text(),'Forgot your')]")

class ProfLandingPageLocators(object):
    SCHED_PREF_NAVBAR = (By.XPATH, "//div[text()='SCHEDULING PREFERENCES']")
    SET_PREF_BUTTON = (By.XPATH, "//div[text()='SET YOUR PREFERENCES']")

class ProfPrefPageLocators(object):
    SEMESTER_FALL_RADIO = (By.XPATH, "//*[@value='Fall']/parent::span")
    SEMESTER_WINTER_RADIO = (By.XPATH, "//*[@value='Winter']/parent::span")
    SEMESTER_SUMMER_RADIO = (By.XPATH, "//*[@value='Summer']/parent::span")
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
