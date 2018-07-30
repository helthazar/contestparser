import re
import requests
from bs4 import BeautifulSoup

class CodeforcesParser:
    @staticmethod
    def check(contest):
        return re.match('.*codeforces.*', contest)

    @staticmethod
    def getBrowser(contest):
        return None

    @staticmethod
    def parseContestProblems(browser, contest):
        page = requests.get(contest).text
        soup = BeautifulSoup(page, 'html.parser')

        contestName = soup.findAll('table', 'rtable')
        contestName = contestName[0].findAll('a')[0].get_text()
        contestName = contestName.replace('(', '').replace(')', '').replace(' ', '').replace('#', '').replace(',', '').replace('.', '')
        contestName = contestName.replace('Codeforces', '').replace('Educational', 'E').replace('Round', '').replace('Ratedfor', '').replace('and', '').replace('combined', '')

        problems = soup.findAll('table', 'problems')
        problems = problems[0].findAll('td', 'id')
        problems = [p.get_text().strip() for p in problems]
        return (contestName, zip(problems, problems))

    @staticmethod
    def parseProblem(browser, contest, problem, problemlink):
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
