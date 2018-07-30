import re
from bs4 import BeautifulSoup
from selenium import webdriver
import time

class CSAcademyParser:
    @staticmethod
    def check(contest):
        return re.match('.*csacademy.*', contest)

    @staticmethod
    def getBrowser(contest):
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        driver = webdriver.Chrome(chrome_options=options)
        return driver

    @staticmethod
    def parseContestProblems(browser, contest):
        browser.get(contest)
        time.sleep(1)
        soup = BeautifulSoup(browser.page_source, 'html.parser')
        
        contestName = contest.split('/')[-1]

        problems = [a for a in soup.findAll('a') if a['href'] == ('/contest/%s/tasks/' % contest.split('/')[-1])]
        problems = [a['href'].split('/')[-2] for a in problems[0].findAll('a')]
        return (contestName, zip(problems, problems))

    @staticmethod
    def parseProblem(browser, contest, problem, problemlink):
        browser.get('%s/task/%s' % (contest, problemlink))
        time.sleep(1)
        soup = BeautifulSoup(browser.page_source, 'html.parser')

        for br in soup.find_all('br'):
            br.replace_with('\n')
        tests = [t.get_text().strip() + '\n' for t in soup.findAll('pre')]
        return zip(tests[0::2], tests[1::2])