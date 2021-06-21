from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
import pandas as pd
import time
from webdriver_manager.chrome import ChromeDriverManager


def init_browser():
    executable_path = {'executable_path': 'chromedrive.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    return Browser


def scrape():
    browser = init_browser()

    mars_data = {}

# Part One
    url = 'https://redplanetscience.com/'
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')

    tresults = soup.find('div', class_='content_title')

    news_titles = []
    for result in tresults:
        if (result.a):
            if (result.a.text):
                news_titles.append(result)

    finalnewstitles = []
    for x in range(6):
        var = news_titles[x].text
        newvar = var.strip('\n\n')
        finalnewstitles.append(newvar)

    presults = soup.find('div', class_='article_teaser_body')

    news_p = []
    for x in range(6):
        var = presults[x].text
        newvar = var.strip('\n\n')
        news_p.append(newvar)

    mars_data['news_titles'] = finalnewstitles
    mars_data['news_p'] = news_p

# Part Two
    url = 'https://spaceimages-mars.com'
    browser.visit(url)
    browser.links.find_by_partial_text('FULL IMAGE').click()
    html = browser.html
    soup = bs(html, 'html.parser')

    img_url = soup.find('img', class_="fancybox-image").get("src")
    featured_image_url = url + img_url
    featured_image_url

# Part Three
    url = "https://galaxyfacts-mars.com"
    df_facts = pd.read_html(url)
    df_facts[1]

    mars_df = df_facts[1]
    mars_df.columns = ['Description', 'Values']
    mars_df.set_index = ['Description']

    html_table = mars_df.to_html()
    mars_df.to_html('mars_table.html')

# Part Four
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    url = "https://marshemispheres.com/index.html"
    browser.visit(url)

    nextpage_urls = []
    imgtitles = []
    base_url = 'https://marshemispheres.com/'

    html = browser.html
    soup = bs(html, "html.parser")
    divs = soup.find_all('div', class_='description')

    counter = 0
    for div in divs:
        link = div.find('a')
        href = link['href']
        img_title = div.a.find('h3')
        imgtitles.append(img_title)
        next_page = base_url + href
        nextpage_urls.append(next_page)
        counter = counter+1
        if (counter == 4):
            break

    images = []
    for nextpage_url in nextpage_urls:
        url = nextpage_url
        browser.visit(url)
        html = browser.html
        soup = bs(html, 'html.parser')
        link2 = soup.find('img', class_='wide-image')
        forfinal = link2['src']
        full_img = base_url + forfinal
        images.append(full_img)
        nextpage_urls = []

    hemis_photo_urls = []
    cerberus = {'title': imgtitles[0], 'img_url': images[0]}
    schiaparelli = {'title': imgtitles[1], 'img_url': images[1]}
    syrtis = {'title': imgtitles[2], 'img_url': images[2]}
    valles = {'title': imgtitles[3], 'img_url': images[3]}
    hemis_photo_urls = [cerberus, schiaparelli, syrtis, valles]

    return mars_data


if __name__ == "__main__":
    scrape()
