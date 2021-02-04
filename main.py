from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.firefox.options import Options
import time, re, sys

import env #password file

class Skating():
    def __init__(self, env):
        self.driver = webdriver.Firefox()
        self.env = env

    #login to the eFun platform
    def setup(self):
        self.driver.get("https://efun.toronto.ca/TorontoFun/Start/Start.asp")
        self.retryTime = 1
        self.startTime = time.time()

    def login(self):
        try:
            self.driver.find_element_by_xpath("//a[@title='Click here to log in.']").click()
            client = self.driver.find_element_by_id("ClientBarcode")
            client.send_keys(self.env.clientNumber)
            password = self.driver.find_element_by_id("AccountPIN")
            password.send_keys(self.env.familyNumber)
            self.driver.find_element_by_id("Enter").click()
        except Exception as e:
            print("Retrying login", e)
            time.sleep(self.retryTime)
            self.login()

    #go to the reserve skate page
    def skatePage(self):
        try:
            self.driver.find_element_by_xpath("//a[@title='Reservations for Skate']").click()
        except Exception as e:
            print("Retrying skatePage", e)
            time.sleep(self.retryTime)
            self.skatePage()


    # select the park for reservation
    def selectPark(self):
        try:
            self.park = Select(self.driver.find_element_by_name('ComplexId'))
            self.park.select_by_visible_text(self.env.park)
            self.driver.find_element_by_xpath("//a[@title='Show Courses']").click()
            time.sleep(self.retryTime)
        except Exception as e:
            print("Retrying selectPark", e)
            time.sleep(self.retryTime)
            self.selectPark()

    # search for 1 week out from the day
    def lastPage(self):
        try:
            self.driver.find_element_by_xpath("//a[@title='Click here to jump to the last page.']").click()
            time.sleep(self.retryTime)
        except Exception as e:
            print("Retrying lastPage", e)
            time.sleep(self.retryTime)
            self.lastPage()

    # move up 1 page
    def prevPage(self):
        try:
            self.driver.find_element_by_xpath("//a[@title='Click here to jump to the previous page.']").click()
            time.sleep(self.retryTime)
        except Exception as e:
            print("Retrying prevPage", e)
            time.sleep(self.retryTime)
            self.prevPage()

    # find the correct time (logic to cycle through page and find correct button to press)
    def selectTime(self):
        try:
            data = self.driver.find_elements_by_xpath("//tr[@id='activity-course-row']")
            for element in data:
                if self.env.time in element.text:
                    print(element.text)
                    html = element.get_attribute('innerHTML')
                    match = re.findall(r'href=[\'"]?([^\'" >]+)', html)
                    url = [s for s in match if "MyBasket" in s]
                    self.driver.find_element_by_xpath("//a[@href='"+url[0].replace("&amp;", "&")+"']").click()
                    time.sleep(self.retryTime)
                    return

            self.prevPage()
            self.selectTime()
        except Exception as e:
            print("Retrying selectTime", e)
            time.sleep(self.retryTime)
            self.selectTime()

    # register all members of the family
    def registerAll(self):
        print("registering")
        select = self.userSelect()
        names = [name.text for name in select.options[1:]]

        for i in range(len(names)):
            print(names[i])
            if i != 0:
                select = self.userSelect()

            select.select_by_visible_text(names[i])
            if i+1 is not len(names):
                self.addNewClient()

            time.sleep(self.retryTime)

        self.checkout()

    # checkout button
    def checkout(self):
        try:
            self.driver.find_element_by_xpath("//input[@title='Click here to go to the checkout and pay for the items in your shopping cart.']").click()
        except Exception as e:
             print("Retrying checkout", e)
             time.sleep(self.retryTime)
             self.checkout()

    # click add new client button
    def addNewClient(self):
        try:
            self.driver.find_element_by_xpath("//input[@title='Select to add another client to cart.']").click()
        except Exception as e:
             print("Retrying addNewClient", e)
             time.sleep(self.retryTime)
             self.addNewClient()

    # returning user select instance
    def userSelect(self):
        try:
            select = Select(self.driver.find_element_by_name('ClientID'))
            return select
        except Exception as e:
            print("Retrying userSelect", e)
            time.sleep(self.retryTime)
            self.userSelect()

    # submit registration
    def submit(self):
        try:
            self.driver.find_element_by_xpath("//input[@title='Click here to complete transaction and proceed to transaction confirmation page.']").click()
        except Exception as e:
            print("Retrying submit", e)
            time.sleep(self.retryTime)
            self.submit()

    # complete waiver agreement
    def waiverAgreement(self):
        try:
            self.driver.find_element_by_xpath("//input[@title='Click to agree with the Release of Liability, Waiver of Claims, Assumption of Risks and Indemnity Agreement']").click()
        except Exception as e:
            print("Retrying waiverAgreement", e)
            time.sleep(self.retryTime)
            self.waiverAgreement()

    # combines submit and waiver
    def complete(self):
        self.submit()
        self.waiverAgreement()

    # close browser window
    def close(self):
        print("Time elapsed (s):", time.time()-self.startTime)
        time.sleep(5*self.retryTime)
        self.driver.close()

class Headless(Skating):
    def __init__(self, env):
        options = webdriver.firefox.options.Options()
        options.add_argument('-headless')
        self.driver = webdriver.Firefox(executable_path='geckodriver', options=options)
        self.env = env

class Chrome(Skating):
    def __init__(self, env):
        self.driver = webdriver.Chrome()
        self.env = env

class HeadlessChrome(Skating):
    def __init__(self, env):
        options = webdriver.chrome.options.Options()
        options.add_argument('--headless')
        self.driver = webdriver.Chrome(options=options)
        self.env = env

if __name__ == '__main__':
    headless = any('--headless' == arg for arg in sys.argv)
    chrome = any('--chrome' == arg for arg in sys.argv)

    if headless and chrome:
        reserve = HeadlessChrome(env)
    elif not headless and chrome:
        reserve = Chrome(env)
    elif headless and not chrome:
        reserve = Headless(env)
    else:
        reserve = Skating(env)

    reserve.setup()
    reserve.login()
    reserve.skatePage()
    reserve.selectPark()
    reserve.lastPage()
    reserve.selectTime()
    reserve.registerAll()
    reserve.complete()
    reserve.close()
