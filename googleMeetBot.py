#!/usr/bin/env python
# coding: utf-8

# In[12]:


"""__author__ = "Jayson Ruzario"
__copyright__ = ""
__credits__ = ["Aditya Sheshadri", "Clyde Dcosta"]
__license__ = "GPL"
__version__ = "0.0.1"
__maintainer__ = "Jayson ruzario"
__email__ = "jayson.ruzario@21n78e.com"
__status__ = "Development"
"""


# In[13]:


#imports
import time
from selenium import webdriver


# In[31]:


#selenium bot
class meet_bot:
    def __init__(self,cookie_directory,gmeet_link):
        '''
        
        cookie_directory =  usually found in "C:\\Users\\%USERNAME%\\AppData\\Local\\Google\\Chrome\\User Data" 
        gmeet_link = link to google meet eg.'https://meet.google.com/abc-def-ghi'
        '''
        
        #----defining crucial links
        self.cookie_directory= cookie_directory
        self.meeting_link = gmeet_link
        
        #--defining xpath of multiple links--#
        # the intent of defining it this way is so that it can be changed from front-end if required in future..
        
        self.xpath_mic_button = "/html/body/div[1]/c-wiz/div/div/div[8]/div[3]/div/div/div[2]/div/div[1]/div[1]/div[1]/div/div[4]/div[1]/div"
        self.xpath_video_button = "/html/body/div[1]/c-wiz/div/div/div[8]/div[3]/div/div/div[2]/div/div[1]/div[1]/div[1]/div/div[4]/div[2]"
        self.xpath_join_now = "/html/body/div[1]/c-wiz/div/div/div[8]/div[3]/div/div/div[2]/div/div[1]/div[2]/div/div[2]/div/div[1]/div[1]/span/span"
        self.xpath_disconnect_button = "/html/body/div[1]/c-wiz/div[1]/div/div[8]/div[3]/div[9]/div[2]/div[2]/div"
        #optional
        self.xpath_check_time = "/html/body/div[1]/c-wiz/div[1]/div/div[8]/div[3]/div[6]/div[3]/div/div[2]/span"
        self.xpath_check_ppljoined = "/html/body/div[1]/c-wiz/div[1]/div/div[8]/div[3]/div[6]/div[3]/div/div[2]/div[1]/span/span/div/div/span[2]"
        #
        self.xpath_switch_account = '/html/body/div[1]/c-wiz/div/div/div[8]/div[3]/div/div/div[1]/div[2]/div/div/a'                        
        #----------
        
        
        options = webdriver.ChromeOptions()
        path_to_chrome_cookie="user-data-dir="+self.cookie_directory
        #path_to_chrome_cookie="user-data-dir=C:\\Users\\evilr\\AppData\\Local\\Google\\Chrome\\User Data"
        print(path_to_chrome_cookie)
        options.add_argument(path_to_chrome_cookie)
        try:
            self.bot = webdriver.Chrome('./webdriver/chromedriver.exe', options=options)
        except:
            print("[-] 1. Please close all your chrome browser before opening the program")
            print("[-] 2. Please update the chromedriver.exe in the webdriver folder according to your chrome version:https://chromedriver.chromium.org/downloads")
    
    def login(self,acc_email):
        bot=self.bot
        #join meeting
        bot.get(self.meeting_link)
        time.sleep(2)
        #switch account
        switch = bot.find_element_by_xpath(self.xpath_switch_account)
        switch.click()
        time.sleep(1)
        acc = bot.find_element_by_xpath("//*[contains(text(), '{}')]".format(acc_email)) 
        acc.click()
        time.sleep(1)
        #disable mic
        time.sleep(1)
        mic_btn = bot.find_element_by_xpath(self.xpath_mic_button)
        time.sleep(2)
        mic_btn.click()
        time.sleep(2)
        #disable video
        video_btn = bot.find_element_by_xpath(self.xpath_video_button)
        time.sleep(1)
        video_btn.click()
        time.sleep(2)
        #join meet
        join_now = bot.find_element_by_xpath(self.xpath_join_now)
        time.sleep(2)
        join_now.click()
        
    def logout(self):
        bot=self.bot
        time.sleep(2)
        #disconnect for good
        discnt_btn = bot.find_element_by_xpath(self.xpath_disconnect_button)
        time.sleep(2)
        discnt_btn.click()
        bot.close()
        
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

    # def switch_account(self,acc_email):


    #     # bot = self.bot
    #     # time.sleep(1)
    #     # #join meeting
    #     # bot.get(self.meeting_link)
    #     # time.sleep(2)
    #     # #switch account
    #     switch = bot.find_element_by_xpath(self.xpath_switch_account)
    #     switch.click()
        
    #     acc = bot.find_element_by_xpath("//*[contains(text(), '{}')]".format(acc_email)) 
    #     acc.click()


    #     time.sleep(50)

# In[35]:


if __name__ == "__main__":
    
    obj = meet_bot(cookie_directory= "C:\\Users\\evilr\\AppData\\Local\\Google\\Chrome\\User Data",gmeet_link='https://meet.google.com/')

    # obj.login()

    # obj.check_folks_joined()

    # time.sleep(5)
    # # obj.check_time()
    # obj.check_folks_joined()
    # time.sleep(5)
    # obj.logout()


# In[ ]:




