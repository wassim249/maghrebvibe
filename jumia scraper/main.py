from jumiaScraper import JumiaScraper
from filter_darija import filter_darija_sentences

def main():
    scraper = JumiaScraper()
    scraper.scrape()
    filter_darija_sentences('reviews.csv')
    
if __name__ == '__main__':
    main()