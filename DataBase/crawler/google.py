from JobFinder.DataBase.crawler.base.crawler import Crawler
from pymongo import MongoClient
from JobFinder.DataBase.lib.utilities import MONGO_STRING
import time


class GoogleCrawler(Crawler):
    def __init__(self, driver_type=None, driver_path=None):
        super().__init__(driver_type, driver_path)
        self.client = MongoClient(MONGO_STRING)
        self.collection = self.client.jobs.google
        if self.collection.drop():
            self.collection = self.client.jobs.google

    def get_links(self, li):
        return [l.get_attribute('href') for l in li]

    def get_job(self,):
        page = 0
        try:
            while True:
                page += 1
                base_url = 'https://careers.google.com/jobs/results/?page=' + str(page)
                self.browser.get(base_url)
                cur_links = self.get_links(self.browser.find_elements_by_xpath("//ol/li/a"))
                if len(cur_links) < 1:
                    break
                for job_link in cur_links:
                    job = self.process_link(job_link)
                    job['company'] = self.find_sub_company();
                    self.save(job);
        except Exception as e:
            print(e)
            pass
        finally:
            self.browser.quit()

    def find_title(self):
        return self.browser.find_element_by_xpath("//div[@class='gc-card__header gc-job-detail__header']/h1").text

    def find_sub_company(self):
        return ""

    def find_locations(self):
        loc_str = self.browser.find_elements_by_xpath("//p[@class='gc-job-detail__instruction-description']/b")
        if len(loc_str) < 1:
            loc = self.browser.find_element_by_xpath(
                "//div[@class='gc-card__header gc-job-detail__header']/ul/li[@itemprop='jobLocation']")
            return [loc.text]

        return loc_str[0].text.split(';')

    def find_apply_link(self):
        js = "var q=document.documentElement.scrollTop=200"
        self.browser.execute_script(js)
        time.sleep(1)
        apply_link = self.browser.find_element_by_xpath("//div[@class='gc-job-detail__section--apply-bottom-container']/a")
        return apply_link.get_attribute('href')

    def find_description(self):
        return '\n'.join([p.text for p in self.browser.find_elements_by_xpath("//div[@itemprop = 'description']/p")])

    def find_req(self):
        return self.browser.find_element_by_xpath("//div[@itemprop = 'qualifications']")

    def find_minimum(self):
        elements = self.find_req()
        minimum = elements.find_elements_by_xpath("./ul")[0].find_elements_by_xpath("./li")
        return [item.text for item in minimum]

    def find_preferred(self):
        elements = self.find_req()
        minimum = elements.find_elements_by_xpath("./ul")[1].find_elements_by_xpath("./li")
        return [item.text for item in minimum]

    def find_responsibility(self):
        return [item.text for item in self.browser.find_elements_by_xpath("//div[@itemprop='responsibilities']//li")]

    def parse_years_and_degrees(self):
        pass

    def parse_level(self, job):
        pass
