import re
from robobrowser import RoboBrowser
from bs4 import BeautifulSoup
from auth.auth import Auth

class OpencupParser:
    @staticmethod
    def check(contest):
        return re.match('.*contest.yandex.*opencup.*', contest)

    @staticmethod
    def getBrowser(contest):
        browser = RoboBrowser(parser="html.parser", user_agent='Mozilla/5.0')
        browser.open(contest)
        soup = browser.parsed

        link = soup.findAll('a', 'link link_access_login')
        browser.open('https://official.contest.yandex.ru%s' % link[0]['href'])

        form = browser.get_forms()[0]
        form['login'] = Auth.opencup()['login']
        form['password'] = Auth.opencup()['password']
        browser.submit_form(form)
        return browser

    @staticmethod
    def parseContestProblems(browser, contest):
        browser.open('%s/problems' % contest)
        soup = browser.parsed

        contestName = soup.findAll('div', 'contest-head__item contest-head__item_role_title')[0].get_text()
        contestName = contestName.replace(' ', '').replace('GrandPrixof', 'GP').replace('GrandPrix', 'GP')

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
