import feedparser as fp


class Feed(object):
    def __init__(self, url):
        self.feed = fp.parse(url)

    def get_articles(self, size=12):
        return [(entry['title'], entry['link']) for entry in self.feed.entries[:size]]
