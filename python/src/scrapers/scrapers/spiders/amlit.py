import os
from scrapers.items import WebItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class AmlitSpider(CrawlSpider):
    name = 'amlit'
    allowed_domains = ['americanliterature.com']
    start_urls = ['https://americanliterature.com']

    rules = (
        Rule(LinkExtractor(allow=('.*/short-stories-for-children', )), follow=True),
        Rule(LinkExtractor(allow=('.*/short-story/.*', '.*/childrens-stories/.*')), callback='parse_story')
    )

    def parse_story(self, response):
        self.logger.info(response.request.url)
        item = WebItem()
        url = response.request.url
        title = os.path.split(url)[-1].replace('-', ' ').title()

        item['url'] = url
        item['title'] = title
        item['lines'] = response.xpath('//p/text()').extract()
        return item

