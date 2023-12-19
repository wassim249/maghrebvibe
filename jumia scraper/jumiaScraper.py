import selenium
from selenium.webdriver.common.by import By
from time import sleep
from selenium import webdriver
import pandas as pd
import os

class JumiaScraper:
    def __init__(self,reviews_num= 500) -> None:
        self.reviews_num = reviews_num
        self.url = 'https://www.jumia.ma'
        self.categories = [
           # 'telephone-tablette',
            #'electronique',
            #'ordinateurs-accessoires-informatique',
            'maison-cuisine-jardin',
        ]
        if not os.path.exists('reviews.csv'):
            self.reviews_csv = pd.DataFrame(columns=['review','rating'])
        else:
            self.reviews_csv = pd.read_csv('reviews.csv')
        self.scraped_reviews_num = 0
        
        
    def scrape(self):
        self.driver = webdriver.Chrome()
        for category in self.categories:
            self._scrape_category(category)
            
    def _close_newsletter(self):
        try:
            #button aria-label="newsletter_popup_close-cta"
            self.driver.find_element(By.CSS_SELECTOR, 'button[aria-label="newsletter_popup_close-cta"]').click()
        except selenium.common.exceptions.NoSuchElementException:
            pass
        
    def _scroll_to_bottom(self):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        
    def _scrape_category(self,category,page=1):
        print(f'scraping {category} page {page}')
        self.driver.get(f'{self.url}/{category}/?page={page}')
        sleep(2)
        self._close_newsletter()
        #self._scroll_to_bottom()
        sleep(2)
        
        # get all anchor that are in a article tag that has class name prd _fl c-prd
        anchors = self.driver.find_elements(By.CSS_SELECTOR, 'article.prd._fb.col.c-prd a')
        anchors_links = []
        for anchor in anchors:
            anchors_links.append(anchor.get_attribute('href'))

        for link in anchors_links:
            print(self.scraped_reviews_num , self.reviews_num)

            if self.scraped_reviews_num >= self.reviews_num:
                self.scraped_reviews_num = 0
                return
            self._scrape_product(link)
        
        self._scrape_category(category,page+1)

    
                                                  
            
    def _scrape_product(self,product_url):
        # open new tab with product url
        self.driver.get(product_url)
        
    
        sleep(2)
        
        try:
            #click on  button that has class -plxs _more
            showmore_url = self.driver.find_element(By.CSS_SELECTOR, 'a.-plxs._more')
            if showmore_url.get_attribute('href') == None:
                return
            showmore_url.click()
            
            
        except selenium.common.exceptions.NoSuchElementException:
            return
        
        
        # get reviews articles that has class -pvs -hr _bet
        reviews_ratings = [int(rating.text[0]) for rating in self.driver.find_elements(By.CSS_SELECTOR, 'article.-pvs.-hr._bet div.stars._m._al')]
        reviews_texts = [review.text for review in self.driver.find_elements(By.CSS_SELECTOR, 'article.-pvs.-hr._bet p.-pvs')]
        
        self.scraped_reviews_num += len(reviews_texts)
        
        self.reviews_csv = pd.concat([self.reviews_csv,pd.DataFrame({'review':reviews_texts,'rating':reviews_ratings})])
        self._save_reviews()
        
    def _save_reviews(self):
        self.reviews_csv.to_csv('reviews.csv',index=False)
        

        
        
        