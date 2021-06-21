from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import time
import requests
from webdriver_manager.chrome import ChromeDriverManager


def init_browser():
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=True)


def scrape():
    browser = init_browser()

# -------------------------------------------------
# Part One - Mars News Scraping
# -------------------------------------------------

    MarsNews_url = "https://redplanetscience.com/"
    print("Scraping Mars News...")

    browser.visit(MarsNews_url)
    time.sleep(1)

    html = browser.html
    soup = bs(html, 'html.parser')

    last_div = soup.find('div', class_='list_text')
    news_titles = last_div.find('div', class_='content_title').text
    news_p = last_div.find('div', class_='article_teaser_body').text

    print("Mars News: Scraping Complete!")

# -------------------------------------------------
# Part Two - Featured Image Scraping
# -------------------------------------------------

    JPL_url = 'https://spaceimages-mars.com'
    print('Scraping JPL Featured Space Image...')

    browser.visit(JPL_url)
    time.sleep(1)

    html = browser.html
    soup = bs(html, 'html.parser')

    carousel = soup.find('div', class_='carousel_container')
    featuredimage_title = carousel.find('a')['data-title']

    browser.find_by_id('full_image').click()
    time.sleep(1)

    if browser.is_element_visible_by_css('div.fancybox-title') == False:
        base_url = 'https://www.jpl.nasa.gov/'
        image_url = carousel.find('a')['data-fancybox=href']
        featuredimage_url = base_url + image_url

    else:
        base_url = 'https:'

        browser.links.find_by_partial_text('more info').click()
        time.sleep(1)

        img_detail_html = browser.html
        imagesoup = bs(img_detail_html, 'html.parser')
        download_div = imagesoup.find_all('div', class_='download_tiff')[1]
        fullsize_img = download_div.find('a')['href']

        featuredimage_url = base_url + fullsize_img

    print("JPL Featured Space Image: Scraping Complete!")

# -------------------------------------------------
# Part Three - Mars Facts Scraping
# -------------------------------------------------

    MarsFacts_url = 'https://galaxyfacts-mars.com'
    print('Scraping Mars Facts...')

    browser.visit(MarsFacts_url)
    time.sleep(1)

    html = browser.html
    table = pd.read_html(html)

    mars_df = table[0]
    mars_df.columns = ['Description', 'Value']

    html_table = mars_df.to_html(index=False, header=False, border=0,
                                 classes='table table-sm table-striped font-weight-light')
    print('Mars Facts: Scraping Complete!')

# -------------------------------------------------
# Part Four - Mars Hemisphere Images Scraping
# -------------------------------------------------

    Hemisphere_url = 'https://marshemispheres.com/index.html'
    print('Scraping Mars Hemisphere Images...')

    browser.visit(Hemisphere_url)
    time.sleep(1)

    html = browser.html
    soup = bs(html, 'html.parser')

    divs = soup.find_all('div', class_='item')

    hemis_photo_urls = []

    for div in divs:
        hemis_link = browser.find_by_css('a.product-item h3')
        hemis_link[div].click()
        time.sleep(1)

        img_detail_html = browser.html
        imagesoup = bs(img_detail_html, 'html.parser')

        base_url = 'https://marshemispheres.com/'

        hem_url = imagesoup.find('img', class_='wide-image')['src']

        img_url = base_url + hem_url

        img_title = browser.find_by_css('.title').text

        hemis_photo_urls.append({'title': img_title, 'img_url': img_url})

        browser.back()

    browser.quit()
    print("Mars Hemisphere Images: Scraping Complete!")

# -------------------------------------------------
# Create a dictionary to store values
# -------------------------------------------------

    scraped_data = {
        "news_titles": news_titles,
        "news_p": news_p,
        "featuredimage_title": featuredimage_title,
        "mars_facts_table": html_table,
        "hemisphere_images": hemis_photo_urls
    }

    return scraped_data
