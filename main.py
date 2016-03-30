import os, time, re
import urlparse, random, getpass

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup


def getEmail():
    '''Simple function to get email input '''
    email_verrified = False
    while not email_verrified:
        email = raw_input('Linkedin Email: ') #Asking for user input

        #Checking email format
        if re.match(r"[^@]+@[^@]+\.[^@]+", email):
            email_verrified = True
            return email
        else:
            print "Email not valid. Please try again"

def getPassword():
    '''Simple function to get pasword input'''
    pw_verrified = False
    while not pw_verrified:

        password = getpass.getpass('Password:') #Asking for user input

        #Checking password format
        if len(password) >= 6:
            pw_verrified = True
            return password
        else:
            print "Password must have 6 or more characters"

def getPeopleLinks(page):
    '''Append a list with all user links in the page'''
    links = []
    for link in page.find_all('a'): #look for all <a ....> </a
        #Getting the href attribute
        url = link.get('href')
        if url: #making sure there is an href with the boolean
            if 'profile/view?id' in url: #locating the link to other profile
                links.append(url)
    return links

def getJobLinks(page):
    links = []
    for link in page.find_all('a'):#look for all <a ....> </a
        #Getting the href attribute
        url = link.get('href')
        if url: #making sure there is an href with the boolean
            if '/jobs' in url:
                links.append(url)
                print "jobs is in url:",url 
    return links

def getID(url):
    pURL = urlparse.urlparse(url)
    return urlparse.parse_qs(pURL.query)['id'][0]


def ViewBot(browser):
    visited = {}
    pList = []
    counter = 0

    while True:
        time.sleep(random.uniform(3.4, 9.5))
        page = BeautifulSoup(browser.page_source)
        people = getPeopleLinks(page)

        for person in people:
            ID = getID(person)
            if ID not in visited:
                pList.append(person)
                visited[ID] = 1
        
        if pList:
            person = pList.pop()
            browser.get(person)
            
            #Trying to access job
            '''
            jobi=[]
            for job in page.find_all('a'):
                url2=job.get('href')
                if url2: #making sure there is an href with the boolean
                    if 'company/' in url2: #locating the link to other profile
                        jobi.append(url2)
            '''
            counter += 1
        
        else:
            jobs = getJobLinks(page)
            if jobs:
                job = random.choice(jobs)
                root = "http://www.linkedin.com"
                roots = "https://www.linkedin.com"

                if root not in job or roots not in job:
                    job = "https://www.linkedin.com" + job
                browser.get(job)
            else:
                print("I'm lost in this sea of jobs!!!")
                print("I'm giving up....")
                break
        
        print("[+] " + browser.title + jobi[0] + " Visited!\n(" + str(counter)+"/" + str(len(pList)) + ") Visited/Queue")
        print person
        print ""

def Main():
    email = getEmail()
    password = getPassword()
    
    print 'Logging in with %s' % email
    browser = webdriver.Firefox()
    browser.get("https://www.linkedin.com/uas/login")

    emailElement = browser.find_element_by_id("session_key-login")
    emailElement.send_keys(email)
    passwordElement = browser.find_element_by_id("session_password-login")
    passwordElement.send_keys(password)
    passwordElement.submit()

    os.system('clear')
    print("[+] Success! You are now logged in with %s." % email)
    print("[+] The bot is starting!")
    '''
    time.sleep(random.uniform(3.4, 9.5))
    #Indicate the search you want to initiate crawling
    browser.get("https://www.linkedin.com/vsearch/p?keywords=developeur")
    '''
    ViewBot(browser)
    browser.close()


if __name__ == "__main__":
    Main()

