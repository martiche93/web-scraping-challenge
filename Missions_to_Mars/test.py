from splinter import Browser, browser
from bs4 import BeautifulSoup as bs
import time
from webdriver_manager.chrome import ChromeDriverManager

def scrape():
    # browser = init_browser()
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

# -------------------------------------------------
# Part One - Mars News Scraping
# -------------------------------------------------

    # mars = {}

    MarsNews_url = 'https://redplanetscience.com/'
    browser.visit(MarsNews_url)

    time.sleep(1)

    html = browser.html
    soup = bs(html, 'html.parser')

    news_titles = soup.find('div', class_='content_title').get_text()
    news_p = soup.find('div', class_='article_teaser_body').get_text()

    mars_data = {
        'news_titles': news_titles[0],
        'news_p': news_p[0]
    }

    print("Mars News: Scraping Complete!")

    browser.quit()

    return mars_data

# -------------------------------------------------
# Part Two - Featured Image Scraping
# -------------------------------------------------