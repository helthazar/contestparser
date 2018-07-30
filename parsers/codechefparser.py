import re
from urllib2 import urlopen
from bs4 import BeautifulSoup

class CodechefParser:
    @staticmethod
    def check(contest):
        return re.match('.*codechef.*', contest)

    @staticmethod
    def getBrowser(contest):
        return None

    @staticmethod
    def parseContestProblems(browser, contest):
        page = urlopen(contest).read()
        soup = BeautifulSoup(page, 'html.parser')
        
        contestName = contest.split('/')[-1]

        problems = soup.findAll('table', 'dataTable')
        problems = problems[0].findAll('td', align=None)
        problems = [p for p in problems if len(p.findAll('div')) == 0]
        problems = [p.get_text().strip() for p in problems]
        return (contestName, zip(problems, problems))

    @staticmethod
    def parseProblem(browser, contest, problem, problemlink):
        page = urlopen("%s/problems/%s" % (contest, problem)).read()
        soup = BeautifulSoup(page, 'html.parser')

        for br in soup.find_all('br'):
            br.replace_with('\n')
        tests = soup.findAll('pre')
        tests = [p.next_sibling for p in tests[0].findAll('b')]
        tests = ['\n'.join([x for x in p.split('\n') if len(x) != 0]) for p in tests]
        inputs = tests[0] + '\n'
        outputs = tests[1] + '\n'
        return zip([inputs], [outputs])