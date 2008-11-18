#!/usr/bin/env python
#
#
#
#
import time
from cStringIO import StringIO

class TestToolError(StandardError):
    pass

class TestTool(object):
    def __init__(self):
        self.tests = Tests()
        self.env = Env()
    def run(self):
        self.tests.run()

    #
    # add Clause
    #
    def addClause(self, item, clause=[]):
        self.tests.addTests(item, clause)
    def setClause(self, item, clause=[]):
        self.tests.setTests(item, clause)
    def getClause(self, clause):
        return self.tests.getTests(clause)
    
    #
    # add Test
    #
    def addTest(self, item, clause=[]):
        self.tests.addTest(item, clause)
    def setTest(self, item, clause=[]):
        self.tests.setTest(item, clause)
    def getTest(self, clause):
        return self.tests.getTest(clause)
    
    #
    # add Env
    #
    def addEnv(self, type, **kwds):
        self.env.addParam(type, **kwds)
    def setEnv(self, type, **kwds):
        self.env.setParam(type, **kwds)
        
    def __str__(self):
        sout = StringIO()
        sout.write("TestTool ENV>>>\n%s" % self.env)
        sout.write("TestTool Tests>>>\n%s" % self.tests)
        return sout.getvalue()

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

class TestNode(object):
    def __init__(self, **kwds):
        self.title = kwds.get("title", "")
        self.ctime = time.time()
        self.mtime = time.time()
    def __str__(self):
        return """Title : %s
Create Time : %s
Modify Time : %s""" % (self.title,
                       time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.ctime)),
                       time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.mtime)),)

class Test(TestNode):
    def __init__(self, **kwds):
        super(Test, self).__init__(**kwds)
        self.description = kwds.get("description", "")
        self.procedure = {}
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
    def __str__(self):
        sout = StringIO()
        sout.write("%s\n" % super(Test, self).__str__())
        sout.write("Description : %s" % self.description)
        return sout.getvalue()

class Tests(TestNode):
    def __init__(self, **kwds):
        super(Tests, self).__init__(**kwds)

        self._tests_list = []
        self._test_list = []

    def run(self):
        reports = []
        for test in self.test_list:
            reports.append(test.run())
        for tests in self.tests_list:
            reports.append(tests.run())
        return reports

    def addTests(self, tests=None, clause=[]):
        self.getTests(clause)._tests_list.append(tests)
    def setTests(self, clause=[]):
        self.getTests(clause)
        if len(clause) > 0:
            return self.tests(clause[0]).setTests(tests, clause[1:])
        
    def getTests(self, clause=[]):
        if len(clause) > 0:
            return self.tests(clause[0]).getTests(clause[1:])
        else:
            return self
    def getTest(self, clause=[]):
        if len(clause) > 1:
            return self.tests(clause[0]).getTest(clause[1:])
        else:
            return self.test(clause[0])
    def addTest(self, test=None, clause=[]):
        if len(clause) > 0:
            self.tests(clause[0]).addTest(test, clause[1:])
        else:
            self._test_list.append(test)
    
    def tests(self, clause):
        return self._tests_list[clause-1]
    def test(self, clause):
        return self._test_list[clause-1]
    
    def __str__(self):
        sout = StringIO()
        sout.write("Tests : %s\n" % self.title)
        sout.write("%s\n" % super(Tests, self).__str__())
        for test in self._test_list:
            for line in str(test).splitlines():
                sout.write("\t%s\n" % line)
        for tests in self._tests_list:
            for line in str(tests).splitlines():
                sout.write("\t%s\n" % line)
        return sout.getvalue()

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
    def __init__(self):
        self._param = {
                       "account" : {},
                       "hosts" : {},
                       }
    def getHost(self, name):
        return self._param["host"][name]
    def getAccount(self, name):
        return self._param["account"][name]
    def __str__(self):
        sout = StringIO()
        for type, params in self._param.items():
            sout.write("[%s]\n" % type)
            for name, val in params:
                sout.write("%s : %s", (name, val))
        return sout.getvalue()
        
if __name__ == "__main__":
    from teststests import *
    test()

#
# EOF
#
