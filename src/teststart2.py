#!/usr/bin/env python
#
#
#
#
from testtool import *

def test():
    testfile = "../xml/test01.xml"

    file("%s.%d" % (testfile, time.time()), "w").writelines(file(testfile).readlines())

    print "START PARSE"
    testdoc = dom.parse(testfile)
    reportdoc = dom.parseString('<?xml-stylesheet type="text/xsl" href="report_html.xsl"?><autotest></autotest>')

    print "END PARSE"

    testroot = testdoc.getElementsByTagName(u'autotest')[0]
    env = Env(testroot.getElementsByTagName(u'env')[0])

    try:
        reportroot = reportdoc.getElementsByTagName(u'autotest')[0]
    except IndexError:
        reportroot = reportdoc.createElement(u'autotest')
        reportdoc.documentElement.appendChild(reportroot)
    reports = reportdoc.createElement(u'reports')

    tests = Tests(env)
    tests.fromXml(testroot.getElementsByTagName(u'tests')[0])
    strtime_start = time.strftime("%Y-%m-%dT%H:%M:%S")
    tests.run()
    strtime_end = time.strftime("%Y-%m-%dT%H:%M:%S")
    reports = tests.toXmlElements(reportdoc)

    reports.setAttribute(u'start', strtime_start)
    reports.setAttribute(u'end', strtime_end)
    reportroot.appendChild(reports)

    output = file("../xml/report.xml", "w")
    try:
        output.write(reportdoc.toxml().encode('utf-8'))
    finally:
        output.close()

if __name__ == "__main__":
    test()

#
# EOF
#
