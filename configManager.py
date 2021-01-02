from backports import configparser
from datetime import datetime

class ConfigManager:
    """
    config functionality is handled here 
    """
    def __init__(self):
        self.config = configparser.ConfigParser()
        
        self.config.read('config.ini')
    def resetConfig(self):
        self.config['UserConfig'] = {'CookieDirectory': 'Enter Chrome Cookie directory..','GoogleMeetLink': 'Enter Meeting link here',}
        with open('config.ini', 'w') as configfile:
            self.config.write(configfile)

    def setUserconfig(self,arg):
        self.config['UserConfig'] = arg
        with open('config.ini', 'w') as configfile:
            self.config.write(configfile)

    def setDeltaTime(self):
        self.config["timings"] = {'meetingDuration':str(self.deltaMeetingTime()),'timeTilMeet':str(self.deltaTime()[1])}
        print("debug : meeting duration  is {} and meeting would start in {} seconds".format(self.deltaMeetingTime(),self.deltaTime()[1]))
        with open('config.ini', 'w') as configfile:
            self.config.write(configfile)
    #=----------------------

    def startime(self):
        #meeting time
        str_time = self.config["UserConfig"]['starttime'].split(':')
        str_time=[int(x) for x in str_time]
        
        #meeting date
        str_date = self.config["UserConfig"]['date'].split('-')
        str_date=[int(x) for x in str_date]
        
        #create a datetime object 
        return (datetime(str_date[0], str_date[1], str_date[2], str_time[0], str_time[1], str_time[2]))

    def stoptime(self):
        #meeting time
        str_time = self.config["UserConfig"]['endtime'].split(':')
        str_time=[int(x) for x in str_time]
        
        #meeting date
        str_date = self.config["UserConfig"]['date'].split('-')
        str_date=[int(x) for x in str_date]
        
        #create a datetime object 
        return (datetime(str_date[0], str_date[1], str_date[2], str_time[0], str_time[1], str_time[2]))

    def deltaTime(self):
        a=self.startime()
        b=datetime.now()

        c=a-b
        _day,_hours,_mins = self.days_hours_minutes(c)



        return( str(_day)+" days " + str(_hours)+' hours & '+str(_mins)+ ' minutes Remaining',int(c.total_seconds())  )

    def deltaMeetingTime(self):
        a=self.startime()
        b=self.stoptime()

        c=b-a
        # print(c)
        return int(c.total_seconds())

    def days_hours_minutes(self,td):
        return td.days, td.seconds//3600, (td.seconds//60)%60