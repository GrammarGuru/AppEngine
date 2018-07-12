import os
os.chdir('../..')
from src.news.scrapers.scraper import Scraper

article = Scraper('https://www.timeforkids.com/k1/meet-lady-liberty/')
lines = article.get_text()
for line in lines:
    print line