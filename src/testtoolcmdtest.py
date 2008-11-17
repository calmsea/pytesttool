#
#
#
#
#
import unittest

import testtoolcmd

class TestTestToolCmd(unittest.TestCase):
    def setUp(self):
        self.cmd = testtoolcmd.TestToolCmd()
        self.cmd.preloop()
        
    def tearDown(self):
        self.cmd.postloop()

    def testadd(self):
        self.cmd.onecmd("show")
        self.cmd.onecmd("add clause title clause1")
        self.cmd.onecmd("add clause title clause2")
        self.cmd.onecmd("add clause title clause3")
        self.cmd.onecmd("add clause title clause4")
        self.cmd.onecmd("add clause title clause5")
        
        self.cmd.onecmd("add test title test0")
        self.cmd.onecmd("add test clause 1 title test1")
        self.cmd.onecmd("add test clause 1 title test2")
        self.cmd.onecmd("add test clause 2 title test3")
        self.cmd.onecmd("add test clause 2 title test4")
        self.cmd.onecmd("add test clause 3 title test5")
        self.cmd.onecmd("show")
        
def test():
    unittest.main()
    
if __name__ == "__main__":
    test()

#
# EOF
#
