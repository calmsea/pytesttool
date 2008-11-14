#!/usr/bin/env python
#
#
#
#
import sys

import time
import pexpect
import re
import signal
from pexpect import ExceptionPexpect
from cStringIO import StringIO
import xml.dom.minidom as dom
from pprint import pprint

class Report(object):
    RESULT_PASS = 0
    RESULT_FAIL = 1
    RESULT_NONE = 2
    resultstring_table = {
        RESULT_PASS : "PASS",
        RESULT_FAIL : "FAIL",
        RESULT_NONE : "NONE",
    }

    def __init__(self):
        self.id = ""
        self.date = None
        self.tester = "unknown"
        self.result = Report.RESULT_NONE
        self.logs = {}
    def resultstring(self):
        return Report.resultstring_table[self.result]

class Test(object):
    def __init__(self, env):
        self.id = ""
        self.title = ""
        self.description = ""
        self.pubDate = ""
        self.procedure = {}
        self.env = env
    def run(self):
        report = Report()
        report.id = self.id
        print "Running Test(%s)" % self.id
        for key, scripts in self.procedure.items():
            logs = []
            for script in scripts:
                logs.append(script.run())
            report.logs[key] = "\n".join(logs)
        self.report = report
        return report

class Tests(object):
    def __init__(self, env):
        self.tests_list = []
        self.test_list = []
        self.id = None
        self.reports = []
        self.env = env
    def run(self):
        reports = []
        for test in self.test_list:
            reports.append(test.run())
        for tests in self.tests_list:
            reports.append(tests.run())
        return reports

class EnvParam(object):
    def __init__(self, element=None, **kwds):
        self.name = kwds.get("name", None)
        if element:
            self.fromXml(element)

class Account(EnvParam):
    def __init__(self, element=None, **kwds):
        super(Account, self).__init__(**kwds)
        self.host = kwds.get("host", None)
        self.user = kwds.get("user", None)
        self.passwd = kwds.get("passwd", None)
        if element:
            self.fromXml(element)

class Host(EnvParam):
    def __init__(self, element=None, **kwds):
        super(Host, self).__init__(**kwds)
        self.addr = kwds.get("addr", None)
        if element:
            self.fromXml(element)

class Env(object):
    def __init__(self, root=None):
        self.accounts = {}
        self.hosts = {}
        if root:
            self.fromXml(root)
    def getHost(self, name):
        return self.hosts[name]
    def getAccount(self, name):
        return self.accounts[name]

#
# EOF
#
