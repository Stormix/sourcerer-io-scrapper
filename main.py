from scrapper.client import Sourcerer

test = Sourcerer()
test.launchBrowser(headless=True)
test.fillInfo()