#necessary imports for ScatterFly
from selenium.webdriver.common.action_chains import ActionChains
import os, sys, time, urllib2, platform, json
from random import choice, randint
from selenium import webdriver
import bs4 as bs


#declaring variable to store current directory path for future use
currentpath = os.getcwd()


#TODO, custom random link generator using noun list
#opening file that contains a list of nouns and assigning it to a list called words
with open(currentpath + '/data/nounlist.txt') as data:
    words = data.read().splitlines()


#function that returns a random word from the list
def get_random_word():
    return words[randint(0,len(words))]


#function to check and initialize drivers based on system
def start_drivers():
    platform = platform.system()
    print("Attempting to initialize drivers....")
    #if user is using RPi, make sure that the virtual display has been setup or else exit

    if 'raspberrypi' in platform.uname() or 'armv7l' == platform.machine():
        #if user is running on raspberrypi and hasnt set up xvfb properly print instruction on how to set up and exit code
        if not os.getenv('DISPLAY'):
            print("Please make sure that your virtual display is setup correctly and try again!")
            print("Make sure you have executed the following commands: ")
            print("1. xvfb :99 -ac &")
            print("2. export DISPLAY=:99")
            print("Now exiting Program...")
            sys.exit(1)

        #adding options to firefox driver
        from selenium.webdriver.firefox.options import Options
        firefox_options = Options()
        firefox_options.add_argument("--headless") #starting firefox in headless mode
        firefox_options.add_argument("--mute-audio") #starting firefox without audio
        firefox_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36")
        #initializing driver with options
        p = currentpath + '/drivers/geckodriver_arm7'
        return webdriver.Firefox(executable_path = p, firefox_options = firefox_options)
        print("Drivers for RaspberryPi has been initialized succesfully!")

    else: #enters here if device is not a RPi
        #creating a chrome options object that is later going to be attached with the driver!
        from selenium.webdriver.chrome.options import Options
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--mute-audio")
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36")
        #choosing and initializing driver based on OS
        if 'Linux' in (platform):
            return webdriver.Chrome(currentpath +'/drivers/chromedriver_linux',chrome_options = chrome_options)
            print("Drivers for Linux has been initialized succesfully!")
        elif 'Windows' in (platform):
            return webdriver.Chrome(currentpath +'/drivers/chromedriver.exe',chrome_options = chrome_options)
            print("Drivers for Windows has been initialized succesfully!")
        elif 'Darwin' in (platform):
            return webdriver.Chrome(currentpath +'/drivers/chromedriver_mac',chrome_options = chrome_options)
            print("Drivers for OSX has been initialized succesfully!")


def request_user_data():
    print("ScatterFly can use your previous data to make its ability to obfuscate and generate noise more accurate.")
    print("This requires you to give ScatterFly permission to access your previous browsing history.")
    print("Please keep in mind ScatterFly is extremely secure and will not comprimise this data in anyway or form since this data will never leave your machine.")
    permission = input("ScatterFly is requesting permission to acess user data, type 'Yes' to grant permissions or 'No' to deny permission.")

    if permission == "Yes" || permission == "yes" || permission ="y" || permission =="Y":
        print("ScatterFly will now analyze your data to make it's obfuscation more intelligent")
        activity_data = process_data()
        obfuscate(activity_data)
    else:
        print("ScatterFly has been denied permission to access data, ScatterFly will continue running.")
        obfuscate("empty")

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
    driver = init_drivers()
    linklist, sites_dict = get_input()
    print "ScatterFly is now going to start generating some random traffic."
    start_noise(linklist, sites_dict)
