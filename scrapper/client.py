# -*- coding: utf-8 -*-

# @Author: Stormix - Anas Mazouni
# @Date:   2020-06-18
# @Email:  anas.mazouni@stormix.co
# @Project: Sourcerer.io scrapper
# @Website: https://stormix.co

# Import Some Python Modules
import inspect
import sys
import os
import time
from sys import platform
import re
from datetime import datetime
import shutil
from bs4 import BeautifulSoup

# Import self.browser modules
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotVisibleException
from selenium.webdriver.common.keys import Keys


class Sourcerer:
    delay = 2
    baseUrl = "https://sourcerer.io"
    browser = None
    name = None
    data = {}
    selectors = {
        'name': '#summary-section > div > div.profile-narrowed > div > div.section-header > div.caption > div > div.main > h1',
        'username': '#summary-section > div > div.profile-narrowed > div > div.section-header > div.caption > div > div.nick > h2',
        'commits': '#summary-section > div > div.profile-narrowed > div > div.stats > div.plates-but-avatar > div:nth-child(1) > div.stat-number',
        'loc': '#summary-section > div > div.profile-narrowed > div > div.stats > div.plates-but-avatar > div:nth-child(3) > div.stat-number',
        'overview_technologies': '#awesome-chart-section > div > div > div > div.layout > div.chart > div.legend-area > div > div',
        # 'chart': '#awesome-chart-section > div > div > div > div.layout > div.chart > div.chart-area > div > div > div.tooltips',
        'updated_at': '#awesome-chart-section > div > div > div > div.layout > div.section-header > div.repos > div.widget.reposummary > div:nth-child(2)',
        'technologies': '#tech-section > div > div > div > div.layout > div.techs',
    }

    def __init__(self, username="stormiix"):
        self.url = f"{self.baseUrl}/{username}"

    def goTo(self, link):
        self.browser.get(link)
        time.sleep(self.delay)

    def launchBrowser(self, headless=False):
        # Initiate the self.browser webdriver
        currentfolder = os.path.dirname(os.path.abspath(inspect.stack()[0][1]))
        options = webdriver.ChromeOptions()
        options.add_experimental_option("prefs", {
            "download.default_directory": currentfolder,
            'profile.default_content_setting_values.automatic_downloads': 2,
        })
        # open Browser in maximized mode
        options.add_argument("start-maximized")
        options.add_argument("disable-infobars")  # disabling infobars
        options.add_argument("--disable-extensions")  # disabling extensions
        options.add_argument("--disable-gpu")  # applicable to windows os only
        # overcome limited resource problems
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--no-sandbox")  # Bypass OS security model
        if(headless):
            options.add_argument('headless')
            options.add_argument('window-size=1280,800')
            options.add_argument('disable-gpu')
            options.add_argument('allow-insecure-localhost')
        self.browser = webdriver.Chrome(options=options)
        self.browser.get(self.url)
        print("Browser Initiated !")
        print("Loading .. " + self.url, end=' ')
        time.sleep(self.delay)
        print('[DONE]')

    def fillInfo(self):
        self.launchBrowser()
        for k, v in self.selectors.items():
            if 'chart' in k:
                self.data[k] = {
                    'updated_at': datetime.strptime(self.getElementsText(self.selectors['updated_at']).split(': ')[1], '%Y/%m/%d — %H:%M:%S'),
                    'dataset': self.getChartData(v)
                }
            elif '_at' in k:
                self.data[k] = datetime.strptime(self.getElementsText(
                    v).split(': ')[1], '%Y/%m/%d — %H:%M:%S')
            elif k == 'technologies':
                self.data[k] = self.parseTechnologies(v)
            else:
                self.data[k] = self.getElementsText(v)

    def parseTechnologies(self, selector):
        try:
            # Show all techs
            btn = self.browser.find_element_by_css_selector(
                '#tech-section > div > div > div > div.layout > div.show-more')
            self.browser.execute_script("arguments[0].click();", btn)
            # Parse all
            parent = self.browser.find_element_by_css_selector(selector)
            cards = parent.find_elements_by_css_selector('.tech-card')
            technologies = []
            for card in cards:
                soup = BeautifulSoup(card.get_attribute(
                    'innerHTML'), 'html.parser')
                title = soup.find(
                    "div", {"class": "caption"}).get_text().strip()
                commits = int(
                    soup.find("div", {"class": "commits"}).get_text().strip().split(' commits')[0])
                libraries = []
                libCards = soup.findAll("div", {"class": "lib-card"})
                for lib in libCards:
                    libraries.append({
                        'name': lib.findChild("div", {"class": "header"}).get_text().strip(),
                        'type': lib.findChild("div", {"class": "tag"}).get_text().strip(),
                        'loc': int(lib.findChild("div", {"class": "locs"}).get_text().strip().split(" LOC")[0])
                    })
                technologies.append({
                    'title': title,
                    'commits': commits,
                    'libraries': libraries
                })
        except NoSuchElementException as e:
            print("Failed to getText(): NoSuchElement")
        except ElementNotVisibleException as e:
            print("Failed to getText(): ElementNotVisible")

    def getElementsText(self, selector):
        try:
            elements = self.browser.find_elements_by_css_selector(selector)
            if len(elements) == 1:
                return elements[0].text
            else:
                return [elt.text for elt in elements]
        except NoSuchElementException as e:
            print("Failed to getText(): NoSuchElement")
        except ElementNotVisibleException as e:
            print("Failed to getText(): ElementNotVisible")

    def getChartData(self, selector):
        try:
            parent = self.browser.find_element_by_css_selector(selector)
            children = parent.find_elements_by_xpath('div')
            datapoints = []
            for child in children:
                soup = BeautifulSoup(child.get_attribute(
                    'innerHTML'), 'html.parser')
                languages = [elt.findChildren("div") for elt in soup.findAll(
                    "div", {"class": "tech-part"})]
                point = {
                    'date': [datetime.strptime(date, '%Y/%m/%d') for date in soup.find("div", {"class": "interval"}).get_text().split(" - ")],
                    'data': []
                }
                for language in languages:
                    point['data'].append({
                        'language': language[0].get_text(),
                        'commits': int(language[1].get_text().split(": ")[1]),
                        'locs': int(language[2].get_text().split(": ")[1])
                    })
                datapoints.append(point)
            return datapoints
        except NoSuchElementException as e:
            print("Failed to getText(): NoSuchElement")
        except ElementNotVisibleException as e:
            print("Failed to getText(): ElementNotVisible")

    def getInfo(self):
        return self.browser.find_element_by_css_selector(self.selectors['profile']['name'])


if __name__ == "__main__":
    test = Sourcerer()
    test.launchBrowser(headless=True)
    test.fillInfo()
