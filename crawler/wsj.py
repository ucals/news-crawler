# -*- coding: utf-8 -*-
import os
import requests
from time import sleep
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options


def scrape_url(url):
    """
    Return HTML content of the WSJ url, stripped of distractions
    :param url: WSJ url
    :return: HTML content (string)
    """
    # Initialize driver
    options = Options()
    options.set_headless(headless=True)
    driver = webdriver.Firefox(firefox_options=options)

    # Login
    driver.get(url)
    sleep(10)
    driver.find_elements_by_xpath("//*[contains(text(), 'Sign In')]")[0].click()
    driver.find_element_by_id("username").send_keys(os.environ['WSJ_USER'])
    driver.find_element_by_id("password").send_keys(os.environ['WSJ_PASS'])
    driver.find_elements_by_class_name("solid-button.basic-login-submit")[0].click()

    # Wait full article to load
    sleep(10)
    contents = driver.page_source
    soup = BeautifulSoup(contents, 'html.parser')
    article = soup.find('article')

    # Removing non-content
    for id_name in ['ad_and_popular', 'share-target']:
        val = article.find(id=id_name)
        if val is not None:
            val.decompose()

    for class_name in ['.comments-count-container', '.author.mobile-scrim', '.byline', '.category']:
        for val in article.select(class_name):
            if val is not None:
                val.decompose()

    # Format images
    for val in article.select('.image-container.responsive-media'):
        if val is not None:
            new_tag = soup.new_tag('img')
            new_tag.attrs['src'] = val.find('img').attrs['src']
            val.replace_with(new_tag)

    return article.prettify("latin-1") #.decode("utf-8")
