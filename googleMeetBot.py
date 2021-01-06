#!/usr/bin/env python
# coding: utf-8

"""__author__ = "Jayson Ruzario"
__copyright__ = ""
__credits__ = ["Aditya Sheshadri", "Clyde Dcosta"]
__license__ = "open-source"
__version__ = "0.0.1"
__maintainer__ = "Jayson ruzario"
__email__ = "jayson.ruzario@21n78e.com"
__status__ = "Development"
"""

#imports
import time
from selenium import webdriver


#selenium bot
class meet_bot:
    def __init__(self,gmeet_link):

        #----defining crucial links
        self.cookie_directory= "./cookies"
        self.meeting_link = gmeet_link

        #--defining xpath of multiple links--#
        # the intent of defining it this way is so that it can be changed from front-end if required in future..
        self.xpath_mic_button = "/html/body/div[1]/c-wiz/div/div/div[8]/div[3]/div/div/div[2]/div/div[1]/div[1]/div[1]/div[1]/div[3]/div[1]/div/div/div/span"
        self.xpath_video_button = "/html/body/div[1]/c-wiz/div/div/div[8]/div[3]/div/div/div[2]/div/div[1]/div[1]/div[1]/div[1]/div[3]/div[2]/div/div/span/span"
        # self.xpath_join_now = "/html/body/div[1]/c-wiz/div/div/div[8]/div[3]/div/div/div[2]/div/div[1]/div[2]/div/div[2]/div/div[1]/div[1]/span/span"
        self.xpath_disconnect_button = "/html/body/div[1]/c-wiz/div[1]/div/div[8]/div[3]/div[10]/div[2]/div[2]/div/span"
        #optional
        self.xpath_check_time = "/html/body/div[1]/c-wiz/div[1]/div/div[8]/div[3]/div[6]/div[3]/div/div[2]/span"
        self.xpath_check_ppljoined = "/html/body/div[1]/c-wiz/div[1]/div/div[8]/div[3]/div[6]/div[3]/div/div[2]/div[1]/span/span/div/div/span[2]"
        #
        # self.xpath_switch_account = '/html/body/div[1]/c-wiz/div/div/div[8]/div[3]/div/div/div[1]/div[2]/div/div/a'                        
        #----------
        
        
        options = webdriver.ChromeOptions()
        path_to_chrome_cookie="user-data-dir="+self.cookie_directory
        #path_to_chrome_cookie="user-data-dir=C:\\Users\\evilr\\AppData\\Local\\Google\\Chrome\\User Data"
        print(path_to_chrome_cookie)
        options.add_argument(path_to_chrome_cookie)
        options.add_argument('log-level=3')
        # options.add_argument('--no-sandbox')
        try:
            self.bot = webdriver.Chrome('./webdriver/chromedriver.exe', options=options)
        except:
            print("[-] 2. Please update the chromedriver.exe in the webdriver folder according to your chrome version:https://chromedriver.chromium.org/downloads")
    
    def cookiecreator(self):
        bot=self.bot
        bot.get('https://accounts.google.com/signin')
        try:
            if bot.find_element_by_xpath("/html/body/div[2]/header/div[2]/div[3]"): # checks if logged in 
                print("cookie is available ")
                bot.quit()
        except Exception as e:
            print(e)
            print('element not found')
            print("sleeping")
            time.sleep(30)
            self.cookiecreator()

            
        

    def login(self):
        bot=self.bot
        #join meeting
        bot.get(self.meeting_link)
        print("redirecting to meeting")
        time.sleep(2)
        #switch account
        # switch = bot.find_element_by_xpath(self.xpath_switch_account)
        # switch.click()
        # time.sleep(1)
        # acc = bot.find_element_by_xpath("//*[contains(text(), '{}')]".format(acc_email)) 
        # acc.click()
        # time.sleep(1)
        #disable mic
        time.sleep(3)
        mic_btn = bot.find_element_by_xpath(self.xpath_mic_button)
        time.sleep(2)
        mic_btn.click()
        time.sleep(2)
        print("mic disabled")
        #disable video
        video_btn = bot.find_element_by_xpath(self.xpath_video_button)
        time.sleep(1)
        video_btn.click()
        time.sleep(2)
        print("video disabled")
        #join meet
        join_now = bot.find_element_by_xpath("//*[contains(text(), '{}')]".format("Join now")) 
        time.sleep(2)
        join_now.click()
        print("meeting joined")

    def logout(self):
        bot=self.bot
        time.sleep(2)
        #disconnect for good
        try:
            discnt_btn = bot.find_element_by_xpath(self.xpath_disconnect_button)
            time.sleep(2)
            discnt_btn.click()
            print("disconnected")
        except:
            pass

        bot.quit()
        print("quit")

    def check_time(self):
        bot=self.bot
        time.sleep(1)
        #check Time
        Time_on_meet = bot.find_element_by_xpath(self.xpath_check_time)
        print(Time_on_meet.text)
        
    def check_folks_joined(self):
        bot=self.bot
        time.sleep(1)
        #check ppl joined
        ppl_joined = bot.find_element_by_xpath(self.xpath_check_ppljoined)
        # print(ppl_joined.text)
        return ppl_joined.text


if __name__ == "__main__":
    
    obj = meet_bot(gmeet_link="https://meet.google.com/hur-xvwt-yut")

    obj.login()
    time.sleep(1)
    print("folks joined :")
    print(obj.check_folks_joined())

    time.sleep(1)
    obj.check_time()
    # obj.check_folks_joined()
    time.sleep(5)
    obj.logout()






