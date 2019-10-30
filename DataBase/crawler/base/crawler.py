from selenium import webdriver
from JobFinder.DataBase.lib import utilities as utils
import re
import os
import platform
import time
from abc import ABC, abstractmethod

# TODO has to deal with the platforms


class Crawler(ABC):
    
    def __init__(self, driver_type = None, driver_path = None):
        system = self.set_system(platform.platform().lower())
        # let's do windows and linux first
        prefix = os.getcwd()

        if system == 'windows':
            self.chrome = prefix + utils.WINDOWS_CHROME_DRIVER
            self.phantomjs = prefix + utils.WINDOWS_PHANTOMJS_DRIVER
            self.firefox = prefix + utils.WINDOWS_FIREFOX_DRIVER

        if system == 'linux':
            self.chrome = prefix + utils.LINUX_CHROME_DRIVER
            self.phantomjs = prefix + utils.LINUX_PHANTOMJS_DRIVER
            self.firefox = prefix + utils.LINUX_FIREFOX_DRIVER

        if system == 'mac':
            self.chrome = prefix + utils.MAC_CHROME_DRIVER
            self.phantomjs = prefix + utils.MAC_PHANTOMJS_DRIVER
            self.firefox = prefix + utils.MAC_FIREFOX_DRIVER
        
        if driver_type is not None:
            # customed driver
            # type : Chrome, PhantomJS, FireFox
            
            driver_type = utils.DRIVER_TYPE.get(driver_type)
            
            if driver_type == 'Chrome':
                try:
                    self.browser = webdriver.Chrome(driver_path)
                except FileNotFoundError as e:
                    print(e)
                    print('Using default Chrome driver!')
                    self.browser = webdriver.Chrome(self.chrome)
            elif driver_type == 'PhantomJS':
                try:
                    self.browser = webdriver.PhantomJS(driver_path)
                except FileNotFoundError as e:
                    print(e)
                    print('Using default PhantomJS driver!')
                    self.browser = webdriver.PhantomJS(self.phantomjs)
            elif driver_type == 'Firefox':
                try:
                    self.browser = webdriver.Firefox(driver_path)
                except FileNotFoundError as e:
                    print(e)
                    print('Using default Firefox driver!')
                    self.browser = webdriver.Firefox(self.firefox)
            else:
                try:
                    self.browser = webdriver.Firefox(driver_path)
                except FileNotFoundError as e:
                    print(e)
                    print('Sorry we dont\'t have native support for the driver you asking for. Please check the path you are providing is valid')
                    exit(1)
        else:
            # driver type not provided, using phantomJS as the fastest webdriver
            self.browser = webdriver.PhantomJS(self.phantomjs)

    def set_system(self, sys_info):
        try:
            m = re.search('windows|linux|mac', sys_info)
            return m.group(0)
        except AttributeError as ae:
            print(ae)
            print('Sorry, We don\'t support your system right now')
            exit(1)

    @abstractmethod
    def get_job(self):
        pass

    def process_link(self, job_link):
        job = {'link': job_link}
        self.browser.get(job_link)
        time.sleep(2)
        job['title'] = self.find_title()
        job['responsibilities'] = self.find_responsibility()
        job['locations'] = self.find_locations()
        job['apply_link'] = self.find_apply_link()
        job['description'] = self.find_description()
        job['minimum'] = self.find_minimum()
        job['preferred'] = self.find_preferred()
        return job

    @abstractmethod
    def find_title(self):
        pass

    @abstractmethod
    def find_locations(self):
        pass

    @abstractmethod
    def find_apply_link(self):
        pass

    @abstractmethod
    def find_req(self):
        pass

    @abstractmethod
    def find_responsibility(self):
        pass

    @abstractmethod
    def find_minimum(self):
        pass

    @abstractmethod
    def find_preferred(self):
        pass

    @abstractmethod
    def parse_years_and_degrees(self):
        pass

    # save job
    def save(self, job):
        self.collection.insert_one(job)

    # must call this before call get_job_level
    @abstractmethod
    def parse_years_and_degrees(self,job):
        pass

    def parse_level(self, job):
        # first try to find something from title
        title = job['title']
        
        # see if there is all level key word in the title
        all_level = re.search('all.*level', title.lower())
        if all_level:
            return utils.LEVEL_LIST
        
        # look for one or more matched key word in level list
        levels = re.findall(utils.RE_PATTERNS['level'], title.lower())
        res = []
        for l in utils.LEVEL_LIST:
            for level in levels:
                if l in level:
                    res.append(l)
                    
        # we prefer key word match as the level              
        if len(res)>0:
            job['level'] = res
        
        try:
            # now find level throgh yeas, we need minimum exp 
            for i in range(0,len(utils.YEAR_LIST)-1):
                if job['year']['min'] >= utils.YEAR_LIST[i]:
                    res.append(utils.LEVEL_LIST[i])

            if job['year']['min'] == 0:
                res.append('grad')
        except KeyError as ae:
            print(ae, 'You must call get_job_years_and_degrees before this function')
            self.get_job_years_and_degrees(job)
            self.get_job_level(job)
        else:
            job['level'] = res
        
    
        
        
        
        