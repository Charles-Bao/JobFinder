from pymongo import MongoClient
from JobFinder.DataBase.lib.utilities import MONGO_STRING
from JobFinder.DataBase.crawler.base.crawler import Crawler
import re


class AppleCrawler(Crawler):
    def __init__(self, driver_type=None, driver_path=None):
        super().__init__(driver_type, driver_path)
        self.client = MongoClient(MONGO_STRING)
        self.collection = self.client.jobs.apple
        if self.collection.drop():
            self.collection = self.client.jobs.apple

    def get_links(self,element):
        res = []
        for ele in element:
            res.append(ele.find_element_by_xpath("./tr/td/a").get_attribute('href'))
        return res

    def get_job(self):
        base_url = 'https://jobs.apple.com/en-us/search?search='
        self.browser.get(base_url)
        pages = int(self.browser.find_element_by_xpath("//form[@id='frmPagination']/span[@data-reactid=2840]").text)
        try:
            for i in range(1, pages+1):
                url = 'https://jobs.apple.com/en-us/search?page='+str(i)
                self.browser.get(url)
                job_links = self.get_links(self.browser.find_elements_by_xpath("//div[@id='search_result']/a"))
                for job_link in job_links:
                    job = self.process_link(job_link)
                    job['role_id'] = self.find_id()
                    job['post_date'] = self.find_date()
                    job['weekly-hour'] = self.find_hours()
                    job['team'] = self.find_team()
        except Exception as e:
            print(e)
            pass
        finally:
            self.browser.quit()

    def find_title(self):
        try:
            return self.browser.find_element_by_xpath("//h1[@class='jd__header--title']").text
        except Exception as e:
            print(e)
            print("can't find title in" + self.browser.current_url)
        finally:
            pass

    def find_id(self):
        return self.browser.find_element_by_xpath("//strong[@id='jobNumber']").text

    def find_team(self):
        return self.browser.find_element_by_xpath("//div[@id='job-team-name']").text

    def find_description(self):
        return self.browser.find_element_by_xpath("//div[@id='jd-job-summary']//span").text



    job['location'] = self.find_locations()
    job['apply_link'] = self.find_apply_link()
    job['minimum'] = self.find_minimum()
    job['preferred'] = self.find_preferred()

    def find_date(self):
        return self.browser.find_element_by_xpath("//time[@id='jobPostDate']").get_attribute('datetime')

    def find_hours(self):
        return int(self.browser.find_element_by_xpath("//strong[@id='jobWeeklyHours']").text)
