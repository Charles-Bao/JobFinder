import JobFinder.crawler.facebook as fb
import JobFinder.crawler.google as gg
import unittest as ut

fb_crawler = fb.FacebookCrawler(driver_type='Chrome', driver_path='C:/Users/ybao2/Desktop/JobFinder/JobFinder/lib/chromedriver.exe')
google_crawler = gg.GoogleCrawler(driver_type='Chrome', driver_path='C:/Users/ybao2/Desktop/JobFinder/JobFinder/lib/chromedriver.exe')


fb_crawler.get_job()
google_crawler.get_job()