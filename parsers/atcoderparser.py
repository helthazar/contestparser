import re
from robobrowser import RoboBrowser
from bs4 import BeautifulSoup
from auth.auth import Auth

class AtcoderParser:
    @staticmethod
    def check(contest):
        return re.match('.*atcoder.*', contest)

    @staticmethod
    def getBrowser(contest):
        browser = RoboBrowser(parser="html.parser")
        browser.open('https://beta.atcoder.jp/login')

        form = browser.get_forms()[0]
        form['username'] = Auth.atcoder()['login']
        form['password'] = Auth.atcoder()['password']
        browser.submit_form(form)
        return browser

    @staticmethod
    def parseContestProblems(browser, contest):
        browser.open('%s/assignments' % contest)
        soup = browser.parsed

        contestName = contest.split('//')[1].split('.')[0]

        problems = soup.findAll('table', '')
        problems = problems[0].findAll('td', 'center')
        problemlinks = [p.findAll('a')[0]["href"] for p in problems]
        problems = [p.get_text().strip()[0] for p in problems]
        return (contestName, zip(problems, problemlinks))

    @staticmethod
    def parseProblem(browser, contest, problem, problemlink):
        browser.open('%s%s' % (contest, problemlink))
        soup = browser.parsed

        for br in soup.find_all('br'):
            br.replace_with('\n')
        # tests = soup.findAll('div', {'id': 'task-statement'})
        # tests = tests[0].findAll('span', 'lang-en')
        # tests = tests[0].findAll('pre')
        tests = soup.findAll('pre')
        tests = [t.get_text().strip() + '\n' for t in tests if len(t.findAll(['var'])) == 0]
        return zip(tests[0::2], tests[1::2])
