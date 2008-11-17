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
        self.cmd.onecmd("add test title test1")
        self.cmd.onecmd("add test title test2")
        self.cmd.onecmd("add test title test3")
        self.cmd.onecmd("add test title test4")
        self.cmd.onecmd("add test title test5")
        self.cmd.onecmd("show")
        
def test():
    unittest.main()
    
if __name__ == "__main__":
    test()

#
# EOF
#
