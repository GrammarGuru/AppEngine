from .scraper import Scraper


class USAToday(Scraper):
    def get_article(self):
        article = self.soup.find('article')
        main = article.find('div', {'role': 'main'})
        if main is None:
            return article
        return main

    @staticmethod
    def get_paragraphs(soup):
        return soup.findAll('p', {'class': 'p-text'})
