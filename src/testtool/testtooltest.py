#
#
#
#
#
import unittest

import os
from datetime import datetime

import sqlitelib
import tests

class TestTest(unittest.TestCase):
    def setUp(self):
        self.test = tests.Test()

    def typeCheck(self, test):
        self.failUnless(isinstance(test.title, basestring))
        self.failUnless(isinstance(test.ctime, datetime))
        self.failUnless(isinstance(test.description, basestring))
        
    def testInitialize(self):
        # default init
        test = tests.Test()
        self.typeCheck(test)

        # title
        title = "test_title"
        test = tests.Test(title=title)
        self.typeCheck(test)
        self.failUnlessEqual(test.title, title)

        # ctime
        ctime = "2008-10-28 01:02:03"
        test = tests.Test(ctime=ctime)
        self.typeCheck(test)
        self.failUnlessEqual(test.ctime, datetime.strptime(ctime, "%Y-%m-%d %H:%M:%S"))

        # description
        description = "This is unittest"
        test = tests.Test(description=description)
        self.typeCheck(test)
        self.failUnlessEqual(test.description, description)
        
        # all
        title = "test_title"
        ctime = "2008-10-28 01:02:03"
        description = "This is unittest"
        test = tests.Test(title=title, ctime=ctime, description=description)
        self.typeCheck(test)
        self.failUnlessEqual(test.title, title)
        self.failUnlessEqual(test.ctime, datetime.strptime(ctime, "%Y-%m-%d %H:%M:%S"))
        self.failUnlessEqual(test.description, description)

    def testInitializeError(self):
        # title
        title = 123
        test = tests.Test(title=title)
        self.typeCheck(test)
        self.failUnlessEqual(test.title, str(title))

        # ctime
        ctime = datetime.now()
        test = tests.Test(ctime=ctime)
        self.typeCheck(test)
        self.failUnlessEqual(test.ctime, ctime)

        # description
        description = 123
        test = tests.Test(description=description)
        self.typeCheck(test)
        self.failUnlessEqual(test.description, str(description))

    def testRun(self):
        self.failUnless(self.test.run)
        
    def test__str__(self):
        self.failUnless(self.test.__str__)

class TestReport(unittest.TestCase):
    def setUp(self):
        self.report = tests.Report()

    def typeCheck(self, obj):
        self.failUnless(isinstance(obj.ctime, datetime))
        self.failUnless(isinstance(obj.result, basestring))
        self.failUnless(isinstance(obj.log, basestring))
        
    def testInitialize(self):
        # default init
        report = tests.Report()
        self.typeCheck(report)

        # result
        result = "OK"
        report = tests.Report(result=result)
        self.typeCheck(report)
        self.failUnlessEqual(report.result, result)

        # ctime
        ctime = "2008-10-28 01:02:03"
        report = tests.Report(ctime=ctime)
        self.typeCheck(report)
        self.failUnlessEqual(report.ctime, datetime.strptime(ctime, "%Y-%m-%d %H:%M:%S"))

        # description
        log = "This is unittest log"
        reprot = tests.Report(log=log)
        self.typeCheck(report)
        self.failUnlessEqual(report.log, log)
        
        # all
        result = "OK"
        ctime = "2008-10-28 01:02:03"
        log = "This is unittest log"
        report = tests.Report(result=result, ctime=ctime, log=log)
        self.typeCheck(report)
        self.failUnlessEqual(report.result, result)
        self.failUnlessEqual(report.ctime, datetime.strptime(ctime, "%Y-%m-%d %H:%M:%S"))
        self.failUnlessEqual(report.log, log)

    def testInitializeError(self):
        # title
        result = 123
        report = tests.Report(result=result)
        self.typeCheck(report)
        self.failUnlessEqual(report.result, str(result))

        # ctime
        ctime = datetime.now()
        report= tests.Test(ctime=ctime)
        self.typeCheck(report)
        self.failUnlessEqual(report.ctime, ctime)

        # description
        log = 123
        report = tests.Test(log=log)
        self.typeCheck(report)
        self.failUnlessEqual(report.log, str(log))

    def test__str__(self):
        self.failUnless(self.report.__str__)

class TestTestToolSql(unittest.TestCase):
    dbfile = "unittestdb"
    def setUp(self):
        self.testtool = sqlitelib.TestToolSql()
        self.testtool.dbfile = self.dbfile

    def tearDown(self):
        del self.testtool
        try:
            os.unlink(self.dbname)
        except OSError:
            pass

    def typeCheck(self, test):
        self.failUnless(isinstance(test.title, basestring))
        self.failUnless(isinstance(test.ctime, datetime))
        self.failUnless(isinstance(test.description, basestring))
        
    def testIfTest(self):
        for n1 in xrange(4):
            for n2 in xrange(10):
                c1 = n1 + 1
                c2 = n2 + 1
                test = tests.Test(title="test%.3d-%.3d" % (c1, c2))
                self.testtool.addTest(test, [c1, c2])
        for n1 in xrange(4):
            for n2 in xrange(10):
                c1 = n1 + 1
                c2 = n2 + 1
                test = self.testtool.getTest([c1, c2,])
                self.failUnlessEqual(test.title, "test%.3d-%.3d" % (c1, c2))
        
    def testIfReport(self):
        for n1 in xrange(4):
            for n2 in xrange(10):
                c1 = n1 + 1
                c2 = n2 + 1
                report = tests.Report(test_id=c1*100+c2)
                self.testtool.addReport(report)
        for n1 in xrange(4):
            for n2 in xrange(10):
                c1 = n1 + 1
                c2 = n2 + 1
                test = self.testtool.getTest([c1, c2,])
                self.failUnlessEqual(test.title, "test%.3d-%.3d" % (c1, c2))
        
def test():
    unittest.main()
    
if __name__ == "__main__":
    test()

#
# EOF
#
