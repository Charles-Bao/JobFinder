import JobFinder.DataBase.crawler.facebook as fb
import JobFinder.DataBase.crawler.google as gg
#fb_crawler = fb.FacebookCrawler(driver_type='Chrome', driver_path='C:/Users/ybao2/Desktop/JobFinder/JobFinder/DataBase/lib/chromedriver.exe')
google_crawler = gg.GoogleCrawler(driver_type='Chrome', driver_path='C:/Users/ybao2/Desktop/JobFinder/JobFinder/DataBase/lib/chromedriver.exe')


#fb_crawler.get_job()
google_crawler.get_job()