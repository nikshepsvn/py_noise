#necessary imports for ScatterFly
import os, sys, time, urllib2, platform, json
from random import randint
from selenium import webdriver
import bs4 as bs
from selenium.webdriver.common.action_chains import ActionChains
import logging


#TODO, custom random link generator using noun list
#opening file that contains a list of nouns and assigning it to a list
with open(os.getcwd()+'/data/nounlist.txt') as f:
    words = f.read().splitlines()

#function to initialize drivers based on OS and platform
def setupDriver():
    un = platform.uname()
    op_system = platform.system()
    cwd = os.getcwd()
    # Set raspberry pi options
    if (un == 'raspberrypi') or (un == 'arm7l'):
        # Check for xvfb and instruct accordingly
        if not os.getenv('DISPAY'):
            print("Start a virtual display with this command:")
            print("Xvfb :99 -ac &")
            print("export DISPLAY=:99")
            sys.exit(1)

        # Define Firefox option arguments
        from selenium.webdriver.firefox.options import Options
        firefox_options = Options()
        firefox_options.add_argument("--headless")
        firefox_options.add_argument("--mute-audio")
        firefox_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 6.1) AppleWebKit/547.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36")

        return (webdriver.Firefox(executable_path=p, firefox_options=firefox_options))

    else:
        # Define Chrome option arguments
        from selenium.webdriver.chrome.options import Options
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--mute-audio")
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36")

        if ('Linux' in op_system):
            return webdriver.Chrome(cwd+'/drivers/chromedriver_linux', chrome_options=chrome_options)
        elif ('Windows' in op_system):
            return webdriver.Chrome(cwd+'/drivers/chromedriver.exe',chrome_options=chrome_options)
        elif ('Darwin' in op_system):
            return webdriver.Chrome(cwd+'/drivers/chromedriver_mac',chrome_options=chrome_options)

with open(os.getcwd()+'/data/nounlist.txt') as SEARCH_TERMS:
    words = SEARCH_TERMS.read().splitlines()

def getReddit(driver):
    driver.get("https://reddit.com/r/random")
    url = driver.current_url+"top/.json?count=10"
    req = urllib2.Request(url, headers= { 'User-Agent': 'Mozilla/5.0' })
    posts = json.loads(urllib2.urlopen(req).read())
    count = len(posts['data']['children']) - 1
    n = randint(3, count)

    driver.get("https://reddit.com"+posts['data']['children'][n]['data']['permalink'])

    driver.get("https://reddit.com")
    print "Currently viewing: " + driver.current_url
    time.sleep(randint(0,4))

def getYouTube(driver):
    item = words[randint(0,len(words))]

    driver.get("https://www.youtube.com/results?search_query=" + item)
    element = driver.find_element_by_class_name('yt-uix-tile-link')
    element.click()

    actions = ActionChains(driver)
    actions.send_keys('K')
    actions.perform()

    print "Currently viewing: " + driver.current_url
    time.sleep(randint(10,20))

def getTumblr(driver):
    item = words[randint(0,len(words))]
    driver.get("https://www.tumblr.com/search/" + item)
    element = driver.find_element_by_class_name('indash_header_wrapper')
    element.click()
    print "Currently viewing: " + driver.current_url
    time.sleep(randint(5,14))

def getAmazon(driver):
    item = words[randint(0,len(words))]
    driver.get("https://www.amazon.com/s/ref=nb_sb_noss_2?url=search-alias%3Daps&field-keywords=" + item)
    element = driver.find_element_by_class_name('s-access-image')
    element.click()
    print "Currently viewing: " + driver.current_url
    time.sleep(randint(2,7))

def getEbay(driver):
    item = words[randint(0,len(words))]
    driver.get("https://www.ebay.com/sch" + item)
    element = driver.find_element_by_class_name('hide-text')
    element.click()
    print "Currently viewing: " + driver.current_url
    time.sleep(randint(2,7))


# Application loop
if __name__ == "__main__":
    driver = setupDriver()
    print "ScatterFly is now going to start generating some random traffic."
    while (1):
        getReddit(driver)
        getAmazon(driver)
        getYouTube(driver)
        #getTumblr(driver)
        #getEbay(driver)
