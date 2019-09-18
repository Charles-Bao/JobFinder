from JobFinder.crawler.base.crawler import Crawler
import re

class FacebookCrawler(Crawler):

    def __init__(self, driver_type=None, driver_path=None):
        super().__init__(driver_type, driver_path)

    def get_links(self,element):
        res = []
        for jl in element:
            res.append(jl.get_attribute('href'))
        return res

    def get_job(self, base_url):
        base_url = 'https://www.facebook.com/careers/jobs?page=1&results_per_page=100#search_result'
        self.browser.get(base_url)
        num_text = self.browser.find_element_by_xpath("//div[@class='_6ci_']").text
        job_num = int(re.search('\d+', num_text).group())

        for i in range(1, int(job_num / 100) + 1):
            url = 'https://www.facebook.com/careers/jobs?page=' + str(i) + '&results_per_page=100#search_result'
            try:
                self.browser.get(url)
                job_links = self.get_links(self.browser.find_elements_by_xpath("//div[@id='search_result']/a"))
                for job_link in job_links:

                    job = {'link': job_link}

                    self.browser.get(job_link)

                    job['title'] = self.find_title()
                    job['category'] = self.find_categories()
                    job['location'] = self.find_locations()
                    job['apply_link'] = self.find_apply_link()
                    job['description'] = self.find_description()
                    


    def find_title(self):
        return self.browser.find_element_by_xpath("//h4").text

    def find_categories(self):
        categories = self.browser.find_elements_by_xpath("//div[@class='_2ke1']/span")
        return [ c.text for c in categories]

    def find_locations(self):
        locations = self.browser.find_elements_by_xpath("//span[@class='_3-8r _7vwo']")
        return [location.text for location in locations]

    def find_apply_link(self):
        apply_link = self.browser.find_element_by_xpath("//a[@role='button' and @class='_42ft _1p05 _2t6c _5kni _3nu9 _3nua _3nub _6ad5']")
        return apply_link.get_attribute('href')

    def find_description(self):
        return self.browser.find_element_by_xpath("//div[@class = '_3m9 _1n-z _6hy- _6ad1']").text




    def get_job_years_and_degrees(self,job):
        years = {'min': 0, 'prefer': 0}
        degrees = {'min': '', 'prefer': ''}
        
        job['years'] = years
        job['degrees'] = degrees

    def save(self, job):
        pass
