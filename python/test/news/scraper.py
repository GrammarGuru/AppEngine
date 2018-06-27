import os
os.chdir('../..')
from src.news.scrapers.usatoday import USAToday

article = USAToday('https://www.usatoday.com/story/sports/nba/2018/06/23/lebron-james-free-agent-chris-paul-kawhi-leonard-paul-george/728017002/')
lines = article.get_text()
for line in lines:
    print line, '\n'