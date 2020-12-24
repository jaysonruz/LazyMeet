from backports import configparser



class ConfigManager:
    """
    config functionality is handled here 
    """
    def __init__(self):
        self.config = configparser.ConfigParser()
    
    def resetConfig(self):
        self.config['UserConfig'] = {'CookieDirectory': 'Enter Chrome Cookie directory..','GoogleMeetLink': 'Enter Meeting link here',}
        with open('config.ini', 'w+') as configfile:
            self.config.write(configfile)

    def setUserconfig(self,arg):
        self.config['UserConfig'] = arg
        with open('config.ini', 'w+') as configfile:
            self.config.write(configfile)