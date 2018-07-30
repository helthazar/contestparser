#!/usr/bin/env python
from sys import argv
from subprocess import call
from parsers.codeforcesparser import CodeforcesParser
from parsers.codechefparser import CodechefParser
from parsers.opencupparser import OpencupParser
from parsers.yandexcontestparser import YandexContestParser
from parsers.atcoderparser import AtcoderParser
from parsers.hackerrankparser import HackerrankParser
from parsers.csacademyparser import CSAcademyParser
from parsers.codejamparser import CodejamParser

TEMPLATEPATH = '/PATH/templates/template.cpp'

RED = '\033[31m'
GREEN = '\033[32m'
BOLD = '\033[1m'
NORM = '\033[0m'

def printColor(message, color):
    print BOLD + color + message + NORM

def parseContest(contest):
    if CodeforcesParser.check(contest):
        contestName = contest.split('/')[-1]
        printColor('Codeforces contest %s: %s' % (contestName, contest), GREEN)
        parser = CodeforcesParser

    elif CodechefParser.check(contest):
        contestName = contest.split('/')[-1]
        printColor('Codechef contest %s: %s' % (contestName, contest), GREEN)
        parser = CodechefParser

    elif OpencupParser.check(contest):
        contest = contest.replace('/enter/', '').replace('/enter', '')
        contestName = contest.split('/')[-1]
        printColor('Opencup contest %s: %s' % (contestName, contest), GREEN)
        parser = OpencupParser

    elif YandexContestParser.check(contest):
        contest = contest.replace('/enter/', '').replace('/enter', '')
        contestName = contest.split('/')[-1]
        printColor('Yandex contest %s: %s' % (contestName, contest), GREEN)
        parser = YandexContestParser

    elif AtcoderParser.check(contest):
        contestName = contest.split('/')[-1]
        printColor('Atcoder contest %s: %s' % (contestName, contest), GREEN)
        parser = AtcoderParser

    elif HackerrankParser.check(contest):
        contest = contest.replace('/challenges/', '').replace('/challenges', '')
        contestName = contest.split('/')[-1]
        printColor('Hackerrank contest %s: %s' % (contestName, contest), GREEN)
        parser = HackerrankParser

    elif CSAcademyParser.check(contest):
        contestName = contest.split('/')[-1]
        printColor('CSAcademy contest %s: %s' % (contestName, contest), GREEN)
        parser = CSAcademyParser

    elif CodejamParser.check(contest):
        contestName = contest.split('/')[-2]
        printColor('Codejam contest %s: %s' % (contestName, contest), GREEN)
        parser = CodejamParser

    else:
        printColor('Error no parser: %s' % contest, RED)
        return

    browser = parser.getBrowser(contest)
    (contestName, problems) = parser.parseContestProblems(browser, contest)
    printColor('%s Problems: %s' % (len(problems), ', '.join([problem for (problem, problemlink) in problems])), GREEN)

    for (problem, problemlink) in problems:
        samples = parser.parseProblem(browser, contest, problem, problemlink)
        printColor('Problem %s: %s samples' % (problem, len(samples)), GREEN)

        folder = '%s/tests/%s' % (contestName, problem)
        call(['mkdir', '-p', folder])
        call(['cp', '-n', TEMPLATEPATH, '%s/%s.cpp' % (contestName, problem)])

        for i, (samplein, sampleout) in enumerate(samples):
            infile = open('%s/%s.in' % (folder, i + 1), 'w')
            infile.write(samplein)
            outfile = open('%s/%s.ans' % (folder, i + 1), 'w')
            outfile.write(sampleout)

    if isinstance(parser, HackerrankParser) or isinstance(parser, CSAcademyParser):
        browser.quit()

def main():
    if len(argv) != 2:
        printColor('Error usage: ./parse.py http://contest', RED)
        return

    contest = argv[1]
    parseContest(contest)

if __name__ == '__main__':
    main()
