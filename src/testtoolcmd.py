from cmd import Cmd
import readline
from testtool import TestTool, Test

class TestToolCmd(Cmd):
    def __init__(self):
        self.prompt = "TestTool> "
        Cmd.__init__(self)

    def preloop(self):
        self.testtool = TestTool()
    def postloop(self):
        pass

#    def do_add(self, str):
#        type, arg, line = self.parseline(str)
#        try:
#            func = getattr(self, "add_" + type)
#        except AttributeError:
#            return self.default(line)
#        return func(arg)
#    def add_test(self, str):
#        print "add Test!!"
#        items = str.split()
#        param = dict(zip(items[0::2], items[1::2]))
#        print param
#        test = Test(**param)
#        if param.has_key("clause"):
#            clause = param.get("clause").split("-")
#        else:
#            clause = []
#        self.testtool.addTest(test, clause)
#    def add_clause(self, str):
#        print "add Clause!!"
    def do_show(self, str):
        if not str:
            self.show()
        else:
            type, arg, line = self.parseline(str)
            try:
                func = getattr(self, "_" + type)
            except AttributeError:
                return self.default(line)
            return func(arg)
    def show(self):
        print self.testtool
    def do_exit(self, str):
        print "exit!!"
        return True

if __name__ == "__main__":
    cli = TestToolCmd()
    cli.cmdloop()
   
#
# EOF
#
