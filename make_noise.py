#necassary imports for PyNoise
import os, sys
import json
import urllib2
import platform
import time
from random import choice, randint
from selenium import webdriver

#TODO, custom random link generator using noun list
with open(os.getcwd()+'/data/nounlist.txt') as f:
    words = f.read().splitlines()

def init_drivers():
    #initializing drivers
    print("Starting drivers ... ")

    # checking if user is attempting to run pynoise on a RPi, and if so, initializing different drivers.
    if 'raspberrypi' in platform.uname() or 'armv7l' == platform.machine():
        if not os.getenv('DISPLAY'):
            print("make sure to start a virtual display:")
            print("Xvfb :99 -ac &")
            print("export DISPLAY=:99")
            sys.exit(1)

        #adding user agent and headless argument to browser
        from selenium.webdriver.firefox.options import Options
        firefox_options = Options()
        firefox_options.add_argument("--headless")
        firefox_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36")

        #initializing driver
        p = os.getcwd() + '/drivers/geckodriver_arm7'
        return webdriver.Firefox(executable_path=p, firefox_options=firefox_options)

    else:
        #adding user agent and headless argument to browser
        from selenium.webdriver.chrome.options import Options
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36")

        #choosing chrome driver based on OS and initializing it for further use
        if 'Linux' in (platform.system()):
            return webdriver.Chrome(os.getcwd()+'/drivers/chromedriver_linux',chrome_options=chrome_options)
        elif 'Windows' in (platform.system()):
            return webdriver.Chrome(os.getcwd()+'/drivers/chromedriver.exe',chrome_options=chrome_options)
        elif 'Darwin' in (platform.system()):
            return webdriver.Chrome(os.getcwd()+'/drivers/chromedriver_mac',chrome_options=chrome_options)


def get_input():
    #asking user for input on which sites users browse to improve pynoise's ability to contaminate the data
    print '''Please select which of these sites you visit most often (choose all that is applicable) (input S when you're finished):
    1. Reddit
    2. Facebook
    3. YouTube
    4. Tumblr
    5. Amazon
    6. Ebay'''

    #creating an AL link user input and fucntions
    sites_dict = {
        '0': 'randomsite()',
        '1': 'randomreddit()',
        '2': 'random_fb()',
        '3': 'random_youtube()',
        '4': 'random_tumblr()',
        '5': 'random_amazon()',
        '6': 'random_ebay()'
    }

    #loop to input the data
    # start with randomsite as default
    linklist = ['0']
    while(1):
        x = raw_input()
        if (x != "S"):
            linklist.append(x)
        else:
            print "You have succesfully entered " + (str(len(linklist)-1)) + " sites."
            break;

    return linklist, sites_dict

#function to visit random webpages on the internet
def randomsite():
    # uroulette url sometimes changes -- implement a selenium viist site and scrape url fix
    site = "http://www.uroulette.com/visit/onvpu"
    driver.get(site)
    time.sleep(randint(0,7))
    print "currently on site: " + driver.current_url

#function to randomly visit a subreddit and then browse through it
def randomreddit():
    driver.get("http://reddit.com/r/random")
    url = driver.current_url+"top/.json?count=10"
    req = urllib2.Request(url, headers={ 'User-Agent': 'Mozilla/5.0' })
    posts = json.loads(urllib2.urlopen(req).read())
    leng = len(posts['data']['children'])
    for i in range(0,leng):
        driver.get("http://reddit.com"+posts['data']['children'][i]['data']['permalink'])
        print "currently on site: " + driver.current_url
        time.sleep(randint(0,5))
    print "currently on site: " + driver.current_url
    time.sleep(randint(0,4))

def random_fb():
    print("Facebook not implemented yet ... ")

def random_youtube():
    site = "http://ytroulette.com/"
    driver.get(site)
    #Time turned off to minimize the amount of data and bandwidth of videos
    #time.sleep(randint(0,2))
    print "currently on site: " + driver.current_url

def random_tumblr():
    print("Tumblr not implemented yet ... ")

def random_amazon():
    #Currently only generates random searches
    rndword = words[randint(0,4553)]
    site = "https://www.amazon.com/s/ref=nb_sb_noss_2?url=search-alias%3Daps&field-keywords=" + rndword
    driver.get(site)
    time.sleep(randint(0,5))
    print "currently on site: " + driver.current_url

def random_ebay():
    iterations = randint(1,8)
    count = 0
    while(1):
        driver.get("http://kice.me/randomebay/")
        element = driver.find_element_by_tag_name('a')
        element.click();
        time.sleep(randint(0,7))
        print "currently on site: " + driver.current_url
        count += 1
        if count == iterations:
            break;



def start_noise(linklist, sites_dict):
    # loop to start the functions and visits
    while(1):
        rnd_site = choice(linklist)
        eval(sites_dict[rnd_site])

if __name__ == "__main__":
    driver = init_drivers()
    linklist, sites_dict = get_input()
    print "ScatterFly is now going to start generating some random traffic."
    start_noise(linklist, sites_dict)
