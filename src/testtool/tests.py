#!/usr/bin/env python
#
#
#
#
from datetime import datetime
from cStringIO import StringIO

class TestToolError(StandardError):
    pass

class TestToolBase(object):
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
TestTool = TestToolBase

class Report(object):
    RESULT_PASS = 0
    RESULT_FAIL = 1
    RESULT_NONE = 2
    resultstring_table = {
        RESULT_PASS : "PASS",
        RESULT_FAIL : "FAIL",
        RESULT_NONE : "NONE",
    }

    def __init__(self, **kwds):
        super(Report, self).__init__(**kwds)
        
        ctime = kwds.get("ctime", datetime.now())
        if isinstance(ctime, basestring):
            ctime = datetime.strptime(ctime, "%Y-%m-%d %H:%M:%S")

        self.test_id = kwds.get("test_id", None)
        self.tester  = kwds.get("tester", "unknown")
        self.result  = kwds.get("result", Report.RESULT_NONE)
        self.log     = kwds.get("log", "")
        self.ctime   = ctime
        
    def resultstring(self):
        return Report.resultstring_table[self.result]

    def __str__(self):
        test_id = self.test_id
        tester = self.tester
        result = self.result
        logs = self.logs
        ctime = self.ctime.strftime("%Y-%m-%d %H:%M:%S")
        return """
Test ID     : %(test_id)s
Tester      : $(tester)s
Result      : $(result)s
Create Time : $(ctime)s
Log         :
$(logs)s""" % locals()

class Test(object):
    def __init__(self, **kwds):
        super(Test, self).__init__(**kwds)

        ctime = kwds.get("ctime", datetime.now())
        if isinstance(ctime, basestring):
            ctime = datetime.strptime(ctime, "%Y-%m-%d %H:%M:%S")
        mtime = kwds.get("mtime", datetime.now())
        if isinstance(mtime, basestring):
            mtime = datetime.strptime(mtime, "%Y-%m-%d %H:%M:%S")

        self.title = str(kwds.get("title", ""))
        self.description = str(kwds.get("description", ""))
        self.procedure = {}
        self.ctime = ctime
        self.mtime = mtime

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
        title = self.title
        ctime = self.ctime.strftime("%Y-%m-%d %H:%M:%S")
        mtime = self.mtime.strftime("%Y-%m-%d %H:%M:%S")
        description = self.description
        return """
Title       : %(title)s
Create Time : %(ctime)s
Modify Time : %(mtime)s
Description : %(description)s""" % locals()
        
if __name__ == "__main__":
    from teststests import *
    test()

#
# EOF
#
