import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager


def scrape():

# -------------------------------------------------
# Part One - Mars News Scraping
# -------------------------------------------------

    # Set up Splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # Visit redplanetscience.com
    news_url = 'https://redplanetscience.com/'
    browser.visit(news_url)

    # Scrape page into Soup
    news_html = browser.html
    news_soup = bs(news_html, 'html.parser')

    # Get the news titles
    title = news_soup.find_all("div", class_="content_title")
    title = title[0].text

    # Get the news paragraphs
    paragraph = news_soup.find_all("div", class_="article_teaser_body")
    paragraph = paragraph[0].text

    print(title)
    print("----------------------------------------")
    print(paragraph)

    # Close the browser after scraping
    browser.quit()

# -------------------------------------------------
# Part Two - Featured Image Scraping
# -------------------------------------------------

    # Set up Splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # Visit spaceimages-mars.com
    featured_url = 'https://spaceimages-mars.com'
    browser.visit(featured_url)

    # Scrape page into Soup
    featured_html = browser.html
    featured_soup = bs(featured_html, 'html.parser')

    # Find image url and assign to a variable
    images = featured_soup.find_all("img", class_="header image fade-in")
    for image in images:
        featured_image_url = (image["src"])

    featured_image_url = "https://spaceimages-mars.com/" + featured_image_url
    print(featured_image_url)

    # Close the browser after scraping
    browser.quit()

# # # -------------------------------------------------
# # # Part Three - Mars Facts Scraping
# # # -------------------------------------------------

    # Visit galaxyfacts-mars.com
    facts_url = 'https://galaxyfacts-mars.com'

    # Read tables from html
    tables = pd.read_html(facts_url)

    # Convert table to df
    table_df = pd.DataFrame(tables[1])
    table_df.columns = ["Description", "Value"]
    table_df

    # Convert df to html table string
    html_table = table_df.to_html()
    html_table


# # # -------------------------------------------------
# # # Part Five - Mars Hemisphere Scraping
# # # -------------------------------------------------

    # Set up Splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # Visit marshemispheres.com
    images_url = 'https://marshemispheres.com/'
    browser.visit(images_url)

    # Set up list for hemispheres and entries
    hemispheres = ["Cerberus", "Schiaparelli", "Syrtis Major", "Valles Mariners"]
    hemisphere_entries = []

    for hemi in hemispheres:

        # Click hemisphere link
        browser.links.find_by_partial_text(hemi + "Hemisphere Enhanced").click()

    # Scrape page into Soup
    images_html = browser.html
    images_soup = bs(images_html, 'html.parser')

    # Find all the image links
    li = images_soup.find_all("lli")
    a = li[0].find("a")
    image_url = images_url+a["href"]

    # Add urls to dictionary
    hemisphere_entries.append({"title": hemi + " Hemisphere Enhanced", "img_url": image_url})

    # Click the 'back' button
    browser.links.find_by_partial_text("Back").clilck()

    # Close the browser after scraping
    browser.quit()

    # View scraped hemisphere entries
    hemisphere_entries

    hemisphere_image_urls = hemisphere_entries
    hemisphere_image_urls

    mars_dictionary = {
        "article_title": title,
        "article_paragraph": paragraph,
        "featured_image_url": featured_image_url,
        "html_table": html_table,
        "cerberus_title": hemisphere_image_urls[0]["title"],
        "cerberus_image": hemisphere_image_urls[0]["img_url"],
        "schiaparelli_title": hemisphere_image_urls[1]["title"],
        "schiaparelli_image": hemisphere_image_urls[1]["img_url"],
        "syrtis_major_title": hemisphere_image_urls[2]["title"],
        "syrtis_major_image": hemisphere_image_urls[2]["img_url"],
        "valles_marineris_title": hemisphere_image_urls[3]["title"],
        "valles_marineris_image": hemisphere_image_urls[3]["img_url"]
    }

    return(mars_dictionary)
