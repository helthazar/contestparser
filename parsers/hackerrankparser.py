import re
from selenium import webdriver
from bs4 import BeautifulSoup
from auth.auth import Auth
import time

class HackerrankParser:
    @staticmethod
    def check(contest):
        return re.match('.*hackerrank.*', contest)

    @staticmethod
    def getBrowser(contest):
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        driver = webdriver.Chrome(chrome_options=options)

        driver.get(contest)
        driver.find_element_by_class_name('login').click()
        login = driver.find_element_by_xpath("//input[@placeholder='Your username or email']")
        login.send_keys(Auth.hackerrank()['login'])
        password = driver.find_element_by_xpath("//input[@placeholder='Your password']")
        password.send_keys(Auth.hackerrank()['password'])
        driver.find_element_by_xpath("//button[@data-analytics='LoginPassword']").click()
        return driver

    @staticmethod
    def parseContestProblems(browser, contest):
        browser.get('%s/challenges' % contest)
        time.sleep(1)
        soup = BeautifulSoup(browser.page_source, 'html.parser')
        
        contestName = contest.split('/')[-1]

        problems = soup.findAll('h4', 'challengecard-title')
        problems = [p.findAll('a')[0]['data-attr1'] for p in problems]
        return (contestName, zip(problems, problems))

    @staticmethod
    def parseProblem(browser, contest, problem, problemlink):
        browser.get('%s/challenges/%s' % (contest, problemlink))
        time.sleep(1)
        soup = BeautifulSoup(browser.page_source, 'html.parser')

        for br in soup.find_all('br'):
            br.replace_with('\n')
        inputs = soup.findAll('div', 'challenge_sample_input')
        inputs = [t.findAll('pre')[0].get_text().strip() + "\n" for t in inputs]
        outputs = soup.findAll('div', 'challenge_sample_output')
        outputs = [t.findAll('pre')[0].get_text().strip() + "\n" for t in outputs]
        return zip(inputs, outputs)