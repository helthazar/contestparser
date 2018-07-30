import re
from bs4 import BeautifulSoup
from selenium import webdriver
import time

class CodejamParser:
    @staticmethod
    def check(contest):
        return re.match('.*codejam.*', contest)

    @staticmethod
    def getBrowser(contest):
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        driver = webdriver.Chrome(chrome_options=options)
        return driver

    @staticmethod
    def parseContestProblems(browser, contest):
        browser.get(contest)
        time.sleep(2)
        soup = BeautifulSoup(browser.page_source, 'html.parser')

        contestName = soup.findAll('div', 'challenge__title')
        contestName = contestName[0].findAll('h4')[0].get_text()
        contestName = contestName.replace(' ', '')

        problems = soup.findAll('div', 'collection no-margin')
        problems = problems[0].findAll('a')
        problemlinks = [p["href"] for p in problems]
        problems = [p.get_text().strip().replace(' ', '').replace(':', '') for p in problems]
        print problemlinks
        return (contestName, zip(problems, problemlinks))

    @staticmethod
    def parseProblem(browser, contest, problem, problemlink):
        return
        page = requests.get("%s/problem/%s" % (contest, problem)).text
        soup = BeautifulSoup(page, 'html.parser')

        for br in soup.find_all('br'):
            br.replace_with('\n')
        tests = soup.findAll('div', 'sample-test')
        inputs = tests[0].findAll('div', 'input')
        inputs = [t.pre.get_text() for t in inputs]
        outputs = tests[0].findAll('div', 'output')
        outputs = [t.pre.get_text() for t in outputs]
        return zip(inputs, outputs)