
# Dependencies
from bs4 import BeautifulSoup
from splinter import Browser
import pandas as pd
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_db")


@app.route("/scrape")
def scrape():

    # # NASA MARS NEWS #

    executable_path = {'executable_path': "chromedriver.exe"}
    browser = Browser('chrome', **executable_path, headless=False)

    #URLS of pages to be scraped
    nasanews_url = 'https://mars.nasa.gov/news/'
    browser.visit(nasanews_url)
    browser.is_element_present_by_css('item_list', wait_time=10)


    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    tables = soup.find('ul', class_='item_list')

    article_list = []
    article_plist = []

    for article in tables:
        title = article.find('div', class_="content_title").text
        article_list.append(title)
        paragraph = article.find('div', class_="article_teaser_body").text
        article_plist.append(paragraph)
        
        print(article_list)
        print(article_plist)


    #pull the latest News Title and Paragraph Text
    news_title = article_list[0]
    news_p = article_plist[0]

    print(news_title)
    print(news_p)


    # # JPL MARS SPACE IMAGES #


    executable_path = {'executable_path': "chromedriver.exe"}
    browser = Browser('chrome', **executable_path, headless=False)


    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    browser.is_element_present_by_css('default floating_text_area ms-layer', wait_time=10)


    #grab full image file from site and save as featured_image_url
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    image = soup.find('div', class_='default floating_text_area ms-layer')
    featured_image = image.find('a')['data-fancybox-href']

    featured_image_url = 'https://www.jpl.nasa.gov/' + f'{featured_image}'

    print(featured_image_url)


    # # MARS WEATHER #

    executable_path = {'executable_path': "chromedriver.exe"}
    browser = Browser('chrome', **executable_path, headless=False)



    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    browser.is_element_present_by_css('css-901oao r-hkyrab r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim r-qvutc0', wait_time=10)


    #grab latest tweet from site and save as mars_weather
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    weather = soup.find('div', class_='css-901oao r-hkyrab r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim r-qvutc0')
    mars_weather = weather.find('span', class_='css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0').text

    print(mars_weather)


    # # Mars Facts #


    table_url = 'https://space-facts.com/mars/'

    mars_table = pd.read_html(table_url)

    mars_table


    df = mars_table[0]
    df.columns=["Description", "Value"]
    df.set_index("Description", inplace=True)
    df
    html_mars_table = df.to_html()
    html_mars_table


    # # Mars Hemispheres #

    executable_path = {'executable_path': "chromedriver.exe"}
    browser = Browser('chrome', **executable_path, headless=False)

    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    browser.is_element_present_by_css('collapsible results', wait_time=10)


    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    hemisphere = soup.find('div', class_='collapsible results')
    hem_categories = hemisphere.find_all('div')

    hem_list = []
    for hem in hem_categories:
        info = hem.find('a', class_= 'itemLink product-item').text
        
        hem_list.append(info)

    # remove any blanks
    while("" in hem_list) : 
        hem_list.remove("")
        
    hem_list


    #Cerberus Hemisphere Enhanced extract image
    Cerberus_url ='https://astrogeology.usgs.gov/search/map/Mars/Viking/cerberus_enhanced'

    browser.visit(Cerberus_url)
    browser.is_element_present_by_css('downloads', wait_time=10)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    hem_image = soup.find('div', class_='downloads')
    hem_Cerberus = hem_image.find('a')['href']

    hem_Cerberus

    #Schiaparelli Hemisphere Enhanced extract image
    Schiaparelli_url = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/schiaparelli_enhanced'

    browser.visit(Schiaparelli_url)
    browser.is_element_present_by_css('downloads', wait_time=10)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    hem_image = soup.find('div', class_='downloads')
    hem_Schiaparelli = hem_image.find('a')['href']

    hem_Schiaparelli


    #Syrtis Major Hemisphere Enhanced extract image
    Syrtis_url = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/syrtis_major_enhanced'

    browser.visit(Syrtis_url)
    browser.is_element_present_by_css('downloads', wait_time=10)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    hem_image = soup.find('div', class_='downloads')
    hem_Syrtis = hem_image.find('a')['href']

    hem_Syrtis


    #Valles Marineris Hemisphere Enhanced extract image
    Valles_url = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/valles_marineris_enhanced'

    browser.visit(Valles_url)
    browser.is_element_present_by_css('downloads', wait_time=10)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    hem_image = soup.find('div', class_='downloads')
    hem_Valles = hem_image.find('a')['href']

    hem_Valles


    #create url list
    hem_url_list = [hem_Cerberus,hem_Schiaparelli,hem_Syrtis,hem_Valles]
    hem_url_list


    #combine two lists into key value pair dictionary
    hemisphere_image_urls = [{'title': hem_list[0], 'img_url': hem_url_list[0]},{'title': hem_list[1], 'img_url': hem_url_list[1]},
                {'title': hem_list[2], 'img_url': hem_url_list[2]},{'title': hem_list[3], 'img_url': hem_url_list[3]}]
    hemisphere_image_urls


    # RETURN ONE DICTIONARY CONTAINING ALL ABOVE SCRAPED DATA
    python_dict_list = {'news_title': news_title, 'news_p': news_p,'featured_image_url': featured_image_url,'mars_weather': mars_weather,'html_mars_table': html_mars_table,'hemisphere_image_urls': hemisphere_image_urls}

    #update the Mongo database using update and upsert=True
    mongo.db.collection.update({}, python_dict_list, upsert=True)

    return redirect('/')


@app.route("/")
def home():

    #find one record of data from the mongo database
    mars_data = mongo.db.collection.find_one()

    return render_template('index.html', mars = mars_data)



if __name__ == "__main__":
    app.run(debug=True)
