#necessary imports for ScatterFly
from selenium.webdriver.common.action_chains import ActionChains
import os, sys, time, platform, json
from random import choice, randint, SystemRandom
from selenium import webdriver
import sqlite3 as sql
import bs4 as bs
try:
    import urllib.request as urllib2
except ImportError:
    import urllib2
import functools
print = functools.partial(print, flush=True)

#declaring variable to store current directory path for future use
currentpath = os.getcwd()

#declaring variable to store the system/os of the user
sysplatform = platform.system()

#TODO, custom random link generator using noun list
#opening file that contains a list of nouns and assigning it to a list called words
with open(currentpath + '/data/nounlist.txt') as data:
    words = data.read().splitlines()


#function that returns a random word from the list
def get_random_word():
    return words[random.SystemRandom().randint(0,len(words))]


#function to check and initialize drivers based on system
def start_drivers():
    print("\n\nAttempting to initialize drivers....")
    #if user is using RPi, make sure that the virtual display has been setup or else exit

    if 'raspberrypi' in platform.uname() or 'armv7l' == platform.machine():
        #if user is running on raspberrypi and hasnt set up xvfb properly print(instruction on how to set up and exit code
        if not os.getenv('DISPLAY'):
            print("\nPlease make sure that your virtual display is setup correctly and try again!")
            print("\nMake sure you have executed the following commands: ")
            print("\n1. xvfb :99 -ac &")
            print("\n2. export DISPLAY=:99")
            print("\nNow exiting Program...")
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
        print("\nDrivers for RaspberryPi has been initialized succesfully!")

    else:
        #enters here if device is not a RPi
        #creating a chrome options object that is later going to be attached with the driver!
        from selenium.webdriver.chrome.options import Options
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--mute-audio")
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36")
        #choosing and initializing driver based on OS

        if 'Linux' in (sysplatform):
            print("\nDrivers for Linux has been initialized succesfully!")
            return webdriver.Chrome(currentpath +'/drivers/chromedriver_linux',chrome_options = chrome_options)

        elif 'Windows' in (sysplatform):
            print("\nDrivers for Windows has been initialized succesfully!")
            return webdriver.Chrome(currentpath +'/drivers/chromedriver.exe',chrome_options = chrome_options)

        elif 'Darwin' in (sysplatform):
            print("\nDrivers for OSX has been initialized succesfully!")
            return webdriver.Chrome(currentpath +'/drivers/chromedriver_mac',chrome_options = chrome_options)


#function that asks user permission to access previous data
def request_user_data():
    print("\nScatterFly can use your previous data to make its ability to obfuscate and generate noise more accurate.")
    print("\nThis requires you to give ScatterFly permission to access your previous browsing history.")
    print("\nPlease keep in mind ScatterFly is extremely secure and will not comprimise this data in anyway or form since this data will never leave your machine.")
    permission = input("ScatterFly is requesting permission to acess user data, type 'Yes' to grant permissions or 'No' to deny permission.")

    if permission == "Yes" or permission == "yes" or permission == "y" or permission =="Y":
        print("\nScatterFly will now analyze your data to make it's obfuscation more intelligent")
        activity_data = obtain_data()
        process_data(activity_data)
        obfuscate(activity_data)
    else:
        print("\nScatterFly has been denied permission to access data, ScatterFly will continue running.")
        obfuscate("empty")

def get_browser():
        browser = input("Are you using Chrome or Firefox? -- Enter C for Chrome, F for Firefox. Press X to exit.")
        if browser == 'F':
            return("Firefox")
        elif browser == 'C':
            return("Chrome")
        elif browser == 'X':
            sys.exit(1)
            return("Exit")
        else:
            return("Invalid")

#function that obtains data from browser
def obtain_data():
    browser = get_browser()
    datapath = NULL
    if browser == "Chrome":
        winpath = '/AppData/Local/Google/Chrome/User Data/Default'
        linuxpath = '/.config/google-chrome/Default'
        macpath = '/Library/Application Support/Google/Chrome/Default'
        get_chrome_data()
    elif browser == "Firefox":
        winpath = '/AppData/Roaming/Mozilla/Firefox/Profiles'
        linuxpath = "/.mozilla/firefox/"
        macpath = '/Library/Application Support/Firefox/Profiles/'
        get_firefox_data()

    def get_chrome_data():
        if datapath is NULL:
            if 'raspberrypi' in platform.uname() or 'armv7l' == platform.machine():
                print("Please copy all the data from your browser user data folder and place it in the root directory of the file in the folder called data")
            if "Darwin" in sysplatform:
                datapath = os.path.expanduser('~')+macpath
            if "Linux" in sysplatform:
                datapath = os.path.expanduser('~')+linuxpath
            if "Windows" in sysplatform:
                datapath = os.path.expanduser('~')+winpath

        if datapath is not NULL:
            print("Data has been found!")
        else:
            datapath = input("There was an error finding the data, if you have installed"+browser+"in a non default directory please input the path to the directory or type 'X' to exit")
            if datapath == 'X':
                print("Exiting ScatterFly!")
                time.sleep(0.5)
                sys.exit(1)
            else:
                get_chrome_data()
            print("Attempting to find data...")

    print("Loading data for Processing..")
    files = os.listdir(datapath)
    history_db = os.path.join(data_path, '/History')
    c = sql.connect(history_db)
    cursor = c.cursor()
    select_statement = "SELECT urls.url, urls.visit_count FROM urls, visits WHERE urls.id = visits.url;"
    cursor.execute(select_statement)
    results = cursor.fetchall()
    print(results)





#get_input is a function gets information from the user
def get_input():
    #asking user for input on which sites users browse to improve ScatterFly's ability to contaminate the data
    print("Please select which of these sites you visit most often (choose all that is applicable and input 0 when finished):")
    print("1. Reddit")
    print("2. YouTube")
    print("3. Tumblr")
    print("4. Amazon")
    print("5. Ebay")


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
    while(True):
        x = input()
        if x == '0':
            print("You have succesfully entered " + (str(len(linklist)-1)) + " sites.")
            break;
        else:
            linklist.append(x)

    return linklist, sites_dict

#function to visit random webpages on the internet, currently using uroulette
def randomsite():
    # uroulette url sometimes changes -- implement a selenium viist site and scrape url fix
    site = "http://www.uroulette.com/visit/quprs"
    driver.get(site)
    time.sleep(randint(0,7))
    print("currently on site: " + driver.current_url)

#function to randomly visit a subreddit and then browse some posts
def randomreddit():
    driver.get("http://reddit.com/r/random")
    url = driver.current_url+"top/.json?count=10";
    req = urllib2.Request(url, headers={ 'User-Agent': 'Mozilla/5.0' })
    posts = json.loads(urllib2.urlopen(req).read())
    leng = len(posts['data']['children'])
    for i in range(0,leng):
        driver.get("http://reddit.com"+posts['data']['children'][i]['data']['permalink'])
        print("currently on site: " + driver.current_url)
        time.sleep(randint(0,5))
    print("currently on site: " + driver.current_url)
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
        print("currently on site: " + driver.current_url)
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
        print("currently on site: " + driver.current_url)
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
        print("currently on site: " + driver.current_url)
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
        print("currently on site: " + driver.current_url)
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
    driver = start_drivers()
    linklist, sites_dict = get_input()
    print("ScatterFly is now going to start generating some random traffic.")
    start_noise(linklist, sites_dict)
