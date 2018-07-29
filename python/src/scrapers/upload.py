from google.cloud import storage
from scrapy.crawler import CrawlerProcess
from scrapers.spiders.amlit import AmlitSpider

BUCKET_NAME = 'sentence-92ceb.appspot.com'
FILENAME = 'web/American Literature.json'

process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
    'FEED_FORMAT': 'json',
    'FEED_URI': 'data.json'
})

process.crawl(AmlitSpider)
process.start()

blob = storage.Client().bucket(BUCKET_NAME).blob(FILENAME)
blob.upload_from_filename('data.json')
