#!/usr/bin/env python
#
#
#
#
from testtool import TestTool

xmldir = "../xml"
testfile = "%s/test.xml" % xmldir
reportfile = "%s/report.xml" % xmldir

tool = TestTool()
tool.loadXml(testfile)
try:
    tool.run()
except:
    tool.saveXml(reportfile)
    raise

#
# EOF
#
