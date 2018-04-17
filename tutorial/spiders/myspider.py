
#-*- coding: utf-8 -*-
import scrapy
import hashlib

class MySpider(scrapy.Spider):
	name='myspider'
	pagemd5s=list()

	def start_requests(self):
		yield scrapy.Request('https://www.chunyuyisheng.com/pc/qalist/clinicno_4/', self.parse)
		yield scrapy.Request('https://www.chunyuyisheng.com/pc/qalist/clinicno_2/', self.parse)
		yield scrapy.Request('https://www.chunyuyisheng.com/pc/qalist/clinicno_1/', self.parse)



	def parse(self, response):
		
		# get md5 encode about response.body
		md5 = hashlib.md5()
		md5.update(response.body)
		bodymd5encode = md5.hexdigest()
		
		if bodymd5encode in self.pagemd5s:
			return
		else:
			self.pagemd5s.append(bodymd5encode)

		
				
		title = response.css('title::text').extract_first()
		for qaitem in response.css("div.hot-qa-item"):
			ask = ''
			answer = ''
			for result in qaitem.css('div.qa-item.qa-item-ask a::text').extract():
				ask += result.strip()
			for result in qaitem.css('div.qa-item.qa-item-answer::text').extract():
				answer += result.strip()

			yield{
				'ask':ask,
				'answer':answer,
				'title':title,
			}

		# get next page url
		next_page = response.css('div.pagebar a.next::attr(href)').extract_first()
		self.logger.info('next page href = %s', next_page)
		if next_page is not None:
			next_page = response.urljoin(next_page)
			yield scrapy.Request(next_page, callback=self.parse)
		
	
		
