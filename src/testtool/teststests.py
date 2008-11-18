#
#
#
#
#
import unittest

import tests

class TestTests(unittest.TestCase):
    def setUp(self):
        self.tests = tests.Tests()

    def testadd(self):
        self.tests.addTests(tests.Tests(title="tests01"))
        self.tests.addTests(tests.Tests(title="tests02"))
        self.tests.addTests(tests.Tests(title="tests03"))
        self.tests.addTest(tests.Test(title="test01"))
        self.tests.addTest(tests.Test(title="test02"))
        self.tests.addTest(tests.Test(title="test03"))
    
class TestTestTool(unittest.TestCase):
    def setUp(self):
        self.testtool = tests.TestTool()
    
    def testinterface(self):
        self.testtool.addClause(tests.Tests(title="Tests 001"))
        self.testtool.addClause(tests.Tests(title="Tests 002"))
        self.testtool.addClause(tests.Tests(title="Tests 003"))
        self.testtool.addClause(tests.Tests(title="Tests 004"))
        self.testtool.addClause(tests.Tests(title="Tests 005"))
        
        self.testtool.addClause(tests.Tests(title="Tests 001-001"), [1,])
        self.testtool.addClause(tests.Tests(title="Tests 001-002"), [1,])
        self.testtool.addClause(tests.Tests(title="Tests 001-003"), [1,])
        self.testtool.addClause(tests.Tests(title="Tests 001-004"), [1,])
        self.testtool.addClause(tests.Tests(title="Tests 001-005"), [1,])
        self.testtool.addClause(tests.Tests(title="Tests 001-006"), [1,])
        self.testtool.addClause(tests.Tests(title="Tests 002-001"), [2,])
        self.testtool.addClause(tests.Tests(title="Tests 002-002"), [2,])
        self.testtool.addClause(tests.Tests(title="Tests 003-001"), [3,])
        self.testtool.addClause(tests.Tests(title="Tests 003-002"), [3,])
        self.testtool.addClause(tests.Tests(title="Tests 003-003"), [3,])
        self.testtool.addClause(tests.Tests(title="Tests 004-001"), [4,])
        self.testtool.addClause(tests.Tests(title="Tests 004-002"), [4,])
        self.testtool.addClause(tests.Tests(title="Tests 004-003"), [4,])
        self.testtool.addClause(tests.Tests(title="Tests 004-004"), [4,])
        self.testtool.addClause(tests.Tests(title="Tests 005-001"), [5,])
        self.testtool.addClause(tests.Tests(title="Tests 005-002"), [5,])

        self.testtool.addTest(tests.Test(title="Test 001"), [1,1,])
        print self.testtool

        self.assert_(self.testtool.getClause([1,]).title == "Tests 001")
        self.assert_(self.testtool.getClause([2,]).title == "Tests 002")
        self.assert_(self.testtool.getClause([1,1,]).title == "Tests 001-001")
        self.assert_(self.testtool.getClause([1,2,]).title == "Tests 001-002")
        self.assert_(self.testtool.getTest([1,1,1,]).title == "Test 001")
        
        self.assertRaises(IndexError, 
            self.testtool.addClause, tests.Tests(title="Tests 001-003"), [1,100,])
        self.assertRaises(IndexError, 
            self.testtool.addClause, tests.Tests(title="Tests 002-003"), [200,3,])
        self.assertRaises(IndexError, 
            self.testtool.addClause, tests.Tests(title="Tests 002-003"), [1,9,1,])
        self.assertRaises(IndexError, 
            self.testtool.addClause, tests.Tests(title="Tests 002-003"), [2,9,])


def test():
    unittest.main()
    
if __name__ == "__main__":
    test()

#
# EOF
#
