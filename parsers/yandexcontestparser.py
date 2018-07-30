import re
from robobrowser import RoboBrowser
from bs4 import BeautifulSoup
from auth.auth import Auth

class YandexContestParser:
    @staticmethod
    def check(contest):
        return re.match('.*contest.yandex.*', contest)

    @staticmethod
    def getBrowser(contest):
        browser = RoboBrowser(parser="html.parser")
        browser.open(contest)
        soup = browser.parsed

        form = browser.get_forms()[0]
        form['login'] = Auth.yandexcontest()['login']
        form['passwd'] = Auth.yandexcontest()['password']
        browser.submit_form(form)
        return browser

    @staticmethod
    def parseContestProblems(browser, contest):
        browser.open('%s/problems' % contest)
        soup = browser.parsed

        contestName = soup.findAll('div', 'contest-head__item contest-head__item_role_title')[0].get_text()
        contestName = contestName.replace(' ', '').replace('Round', 'R').replace('Qualification', 'Q').replace(',', '')

        problems = soup.findAll('ul', 'tabs-menu_role_problems')
        problems = problems[0].findAll('a')
        problems = [p.get_text().strip()[0] for p in problems]
        return (contestName, zip(problems, problems))

    @staticmethod
    def parseProblem(browser, contest, problem, problemlink):
        browser.open('%s/problems/%s' % (contest, problem))
        soup = browser.parsed

        for br in soup.find_all('br'):
            br.replace_with('\n')
        tests = soup.findAll('table', 'sample-tests')
        tests = [[x.get_text() for x in t.findAll('pre')] for t in tests]
        return tests