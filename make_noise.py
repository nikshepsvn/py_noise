#necessary imports for ScatterFly
import os, sys, time, urllib2, platform, json
from random import choice, randint
from selenium import webdriver
import bs4 as bs
from selenium.webdriver.common.action_chains import ActionChains


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

        return (firefox_options)

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

#get_input is a function gets information from the user
def get_input():
    #asking user for input on which sites users browse to improve ScatterFly's ability to contaminate the data
    print '''Please select which of these sites you visit most often (choose all that is applicable) (input S when you're finished):
    1. Reddit
    2. YouTube
    3. Tumblr
    4. Amazon
    5. Ebay'''

    #creating an AL link user input and functions
    sites_dict = {
        '0': 'randomsite()',
        '1': 'randomreddit()',
        '2': 'random_youtube()',
        '3': 'random_tumblr()',
        '4': 'random_amazon()',
        '5': 'random_ebay()'
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

#function to visit random webpages on the internet, currently using uroulette
def randomsite():
    # uroulette url sometimes changes -- implement a selenium viist site and scrape url fix
    site = "http://www.uroulette.com/visit/quprs"
    driver.get(site)
    time.sleep(randint(0,7))
    print "currently on site: " + driver.current_url

#function to randomly visit a subreddit and then browse some posts
def randomreddit():
    driver.get("https://reddit.com/r/random")
    url = driver.current_url+"top/.json?count=10"
    req = urllib2.Request(url, headers={ 'User-Agent': 'Mozilla/5.0' })
    posts = json.loads(urllib2.urlopen(req).read())
    leng = len(posts['data']['children'])
    for i in range(0,leng):
        driver.get("https://reddit.com"+posts['data']['children'][i]['data']['permalink'])
        print "currently on site: " + driver.current_url
        time.sleep(randint(0,5))
    print "currently on site: " + driver.current_url
    time.sleep(randint(0,4))

def random_youtube():
    iterations = randint(1,8)
    count = 0
    while(1):
        item = words[randint(0,len(words))]
        driver.get("https://www.youtube.com/results?search_query="+item)
        element = driver.find_element_by_class_name('yt-uix-tile-link')
        element.click()
        actions = ActionChains(driver)
        actions.send_keys('K')
        actions.perform()
        time.sleep(randint(15,50))
        print "currently on site: " + driver.current_url
        count = count +1
        if count == iterations:
            break;


def random_tumblr():
    iterations = randint(1,8)
    count = 0
    while(1):
        item = words[randint(0,len(words))]
        driver.get("https://www.tumblr.com/search/"+item)
        element = driver.find_element_by_class_name('indash_header_wrapper')
        element.click()
        time.sleep(randint(5,14))
        print "currently on site: " + driver.current_url
        count = count +1
        if count == iterations:
            break;

def random_amazon():
    iterations = randint(1,8)
    count = 0
    while(1):
        item = words[randint(0,len(words))]
        driver.get("https://www.amazon.com/s/ref=nb_sb_noss_2?url=search-alias%3Daps&field-keywords="+item)
        element = driver.find_element_by_class_name('s-access-detail-page')
        element.click()
        time.sleep(randint(2,7))
        print "currently on site: " + driver.current_url
        count = count +1
        if count == iterations:
            break;

#function to open up a random items on Ebay
#TODO remove dependency and make it go through similar items
def random_ebay():
    iterations = randint(1,8)
    count = 0
    while(1):
        item = words[randint(0,len(words))]
        driver.get("http://www.ebay.com/sch/"+item)
        element = driver.find_element_by_class_name('vip')
        element.click()
        time.sleep(randint(2,7))
        print "currently on site: " + driver.current_url
        count = count +1
        if count == iterations:
            break;


#function to initialize drivers, get input and start running code
def start_noise(linklist, sites_dict):
    # loop to start the functions and visits
    while(1):
        rnd_site = choice(linklist)
        eval(sites_dict[rnd_site])

#main method
if __name__ == "__main__":
    driver = setupDriver()
    linklist, sites_dict = get_input()
    print "ScatterFly is now going to start generating some random traffic."
    start_noise(linklist, sites_dict)
