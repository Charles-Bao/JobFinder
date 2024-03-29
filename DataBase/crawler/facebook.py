from pymongo import MongoClient
from JobFinder.DataBase.lib.utilities import MONGO_STRING
from JobFinder.DataBase.crawler.base.crawler import Crawler
import re


class FacebookCrawler(Crawler):
    def __init__(self, driver_type=None, driver_path=None):
        super().__init__(driver_type, driver_path)
        self.client = MongoClient(MONGO_STRING)
        self.collection = self.client.jobs.facebook
        if self.collection.drop():
            self.collection = self.client.jobs.facebook

    def get_links(self,element):
        res = []
        for jl in element:
            res.append(jl.get_attribute('href'))
        return res

    def get_job(self):
        base_url = 'https://www.facebook.com/careers/jobs?page=1&results_per_page=100#search_result'
        self.browser.get(base_url)
        num_text = self.browser.find_element_by_xpath("//div[@class='_6ci_']").text
        job_num = int(re.search('\d+', num_text).group())
        try:
            for i in range(1, int(job_num / 100) + 1):
                url = 'https://www.facebook.com/careers/jobs?page=' + str(i) + '&results_per_page=100#search_result'
                self.browser.get(url)
                job_links = self.get_links(self.browser.find_elements_by_xpath("//div[@id='search_result']/a"))
                for job_link in job_links:
                    job = self.process_link(job_link)
                    job['categories'] = self.find_categories();
                    self.save(job)
        except Exception as e:
            print(e)
            pass
        finally:
            self.browser.quit()

    def find_title(self):
        try:
            return self.browser.find_element_by_xpath("//h4").text
        except Exception as e:
            print(e)
            print("can't find title in"+self.browser.current_url)
        finally:
            pass

    def find_categories(self):
        try:
            categories = self.browser.find_elements_by_xpath("//div[@class='_2ke1']/span")
            return [ c.text for c in categories]
        except Exception as e:
            print(e)
            print("can't find categories in"+self.browser.current_url)
        finally:
            pass

    def find_locations(self):
        locations = self.browser.find_elements_by_xpath("//span[@class='_3-8r _7vwo']")
        return [location.text for location in locations]

    def find_apply_link(self):
        apply_link = self.browser.find_element_by_xpath("//a[@role='button' and @class='_42ft _1p05 _2t6c _5kni _3nu9 _3nua _3nub _6ad5']")
        return apply_link.get_attribute('href')

    def find_description(self):
        return self.browser.find_element_by_xpath("//div[contains(@class,'_1n-z _6hy- _6ad1')]").text

    def find_req(self):
        return self.browser.find_elements_by_xpath("//div[@class = '_3-8q']")

    def find_responsibility(self):
        elements = self.find_req()
        return [item.text for item in elements[0].find_elements_by_xpath(".//div[@class = '_1zh- _6ad3']") ]

    def find_minimum(self):
        elements = self.find_req()
        return [item.text for item in elements[1].find_elements_by_xpath(".//div[@class = '_1zh- _6ad3']")]

    def find_preferred(self):
        elements = self.find_req()
        if len(elements) <= 2:
            return []
        return [item.text for item in elements[2].find_elements_by_xpath(".//div[@class = '_1zh- _6ad3']")]

    def parse_years_and_degrees(self, job):
        # req: dict, key: min/preferred, value: list of tuple
        # tuple :(year, degree, both)

        # that's so fucking complicate, let's just do years
        # like the data structure below
        years = {'min': 0, 'prefer': 0}
        degrees = {'min': '', 'prefer': ''}

        for item in job['minimum']:
            lst = item.split(' ')

        job['years'] = years
        job['degrees'] = degrees


