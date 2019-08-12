import scrapy
from scrapy import Request

class Jobinja(scrapy.Spider):
    name = 'jobinja'
    allowed_domains = ['jobinja.ir']
    start_urls = ['https://jobinja.ir/collection/استخدام-برنامه-نویس']

    def parse(self, response):
        job_urls = response.css('.c-jobListView__item a::attr(href)').getall()
        for job_url in job_urls:
            yield Request(job_url, callback=self.parseOffer)
        
        next_page_sign = response.css('.paginator li a::text').getall()[-1]
        if next_page_sign == ' →':
            next_page = response.css('.paginator li a::attr(href)').getall()[-1]
            yield response.follow(next_page, callback=self.parse)

    def parseOffer(self, response):
        tag_headers = response.css('#singleJob > div > div:nth-child(1) > div.col-md-8.col-sm-12.js-fixedWidgetSide > section > ul:nth-child(7) > li >  h4::text').getall()
        skills_index = 0
        for index, header in enumerate(tag_headers):
            if header == 'مهارت‌های مورد نیاز':
                skills_index = index + 1
                break
        skills = response.css('#singleJob > div > div:nth-child(1) > div.col-md-8.col-sm-12.js-fixedWidgetSide > section > ul:nth-child(7) > li:nth-child(' + str(skills_index) + ') > div span::text').getall()
        dictOfSkills = { i : (skills[i] if len(skills) > i else None) for i in range(0, 15) }
        yield dictOfSkills
        
