from JobFinder.DataBase.crawler.base.crawler import Crawler
from pymongo import MongoClient
from JobFinder.DataBase.lib.utilities import MONGO_STRING
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

import time


class GoogleCrawler(Crawler):
    def __init__(self, driver_type=None, driver_path=None):
        super().__init__(driver_type, driver_path)
        self.client = MongoClient(MONGO_STRING)
        self.collection = self.client.jobs.google
        if self.collection.drop():
            self.collection = self.client.jobs.google

    def get_links(self, li):
        return list(set([l.get_attribute('href') for l in li]))

    def get_job(self):
        page = 0
        try:
            while True:
                page += 1
                base_url = 'https://careers.google.com/jobs/results/?page=' + str(page)
                self.browser.get(base_url)
                time.sleep(2)
                cur_links = self.get_links(self.browser.find_elements_by_xpath("//ol/li/a"))
                if len(cur_links) < 1:
                    break
                for job_link in cur_links:
                    job = self.process_link(job_link)
                    job['company'] = self.find_sub_company()
                    self.save(job)

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
        try:
            loc_str = self.browser.find_elements_by_xpath("//p[@class='gc-job-detail__instruction-description']/b")
            if len(loc_str) < 1:
                loc = self.browser.find_element_by_xpath("//div[@class='gc-card__header gc-job-detail__header']/ul/li[@itemprop='jobLocation']")
                return [loc.text]
            return loc_str[0].text.split(';')
        except Exception as e:
            print("find_locations error")
            print(e, self.browser.current_url)
        finally:
            pass

    def find_apply_link(self):
        try:
            apply_link = WebDriverWait(self.browser, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[@class='gc-card__meta gc-job-detail__meta']/a"))
            )
            return apply_link.get_attribute('href')
        except Exception as e:
            print("find_apply_link error")
            print(e, self.browser.current_url)
            return ""
        finally:
            pass

    def find_description(self):
        try:
            desc = WebDriverWait(self.browser, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, "//div[@itemprop = 'description']/p"))
            )
            return '\n'.join([p.text for p in desc])
        except Exception as e:
            print("find_description error")
            print(e, self.browser.current_url)
            return ""
        finally:
            pass

    def find_req(self):
        try:
            req = WebDriverWait(self.browser, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[@itemprop = 'qualifications']"))
            )
            return req
        except Exception as e:
            print("find_req error")
            print(e, self.browser.current_url)
            return ""
        finally:
            pass

    def find_minimum(self):
        try:
            elements = self.find_req()
            minimum = elements.find_elements_by_xpath("./ul")[0].find_elements_by_xpath("./li")
            return [item.text for item in minimum]
        except Exception as e:
            print("find_minimum error")
            print(e, self.browser.current_url)
        finally:
            pass

    def find_preferred(self):
        try:
            elements = self.find_req()
            minimum = elements.find_elements_by_xpath("./ul")[1].find_elements_by_xpath("./li")
            return [item.text for item in minimum]
        except Exception as e:
            print("find_preferred error")
            print(e, self.browser.current_url)
        finally:
            pass

    def find_responsibility(self):
        return [item.text for item in self.browser.find_elements_by_xpath("//div[@itemprop='responsibilities']//li")]

    def parse_years_and_degrees(self):
        pass

    def parse_level(self, job):
        pass
