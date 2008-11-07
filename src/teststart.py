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
    def toXmlElements(self, doc):
        report = doc.createElement("report")
        # id
        report.setAttribute(u'ref', "%s" % self.id)
        # date
        date = doc.createElement(u"date")
        date.appendChild(doc.createTextNode(time.strftime("%Y-%m-%dT%H:%M:%S")))
        report.appendChild(date)
        # tester
        tester = doc.createElement(u"tester")
        name = doc.createElement(u"name")
        name.appendChild(doc.createTextNode(self.tester))
        tester.appendChild(name)
        report.appendChild(tester)
        # result
        result = doc.createElement(u"result")
        result.setAttribute(u"value", str(self.result))
        result.appendChild(doc.createTextNode(self.resultstring()))
        report.appendChild(result)
        # log
        log = doc.createElement(u"log")
        for key, val in self.logs.items():
            ent = doc.createElement(unicode(key))
            ent.appendChild(doc.createTextNode(val))
            log.appendChild(ent)
        report.appendChild(log)

        return report
    def resultstring(self):
        return Report.resultstring_table[self.result]

class Script(object):
    def __init__(self):
        self.host = ""
        self.protocol = ""
        self.source = ""
        self.account = ""
        self.user = ""
        self.passwd = ""
    def parse(self, root):
        self.host = root.getAttribute(u'host')
        self.protocol = root.getAttribute(u'protocol')
        self.source = root.firstChild.data
        self.account = root.getAttribute(u'account')
        if not self.account:
            self.user = root.getAttribute(u'user')
            self.passwd = root.getAttribute(u'passwd')
        self.loop = root.getAttribute(u'loop')
    def processing(self, pe, line, prompt):
        print prompt.pattern, line
        mo = re.search(r"^(?P<line>.*)\[\[(?P<commands>.*)\]\]$", line)
        if mo:
            commands = mo.group("commands")
            commands = commands.split(";")
            if line[0] == "#":
                return
            line = mo.group("line")
            (pe.logfile, temp) = (None, pe.logfile)
            pe.sendline(line)
            pe.logfile = temp
            for cmd in commands:
                mo = re.search(r"(?P<func>\w+)\(\s*\"(?P<param>.*)\"\s*\)", cmd)
                func = str(mo.group("func"))
                param = str(mo.group("param"))
                print "func:%s, param:%s" % (func, param)
                if func == "expect":
                    pe.expect(re.escape(param))
                elif func == "sendline":
                    (pe.logfile, temp) = (None, pe.logfile)
                    pe.sendline(param)
                    pe.logfile = temp
                elif func == "sleep":
                    time.sleep(int(param))
                else:
                    print "unknown command!!"
            pe.expect(prompt)
        else:
            (pe.logfile, temp) = (None, pe.logfile)
            pe.sendline(line)
            pe.logfile = temp
            pe.expect(prompt)
        return
    def run(self):
        if not self.loop:
            return self._run()
        else:
            sio = StringIO()
            cmd, val = self.loop.split(":")
            if cmd == "count":
                for n in xrange(int(val)):
                    sio.write(self._run())
            elif cmd == "while":
                sec = int(val)
                start_time = time.time()
                while True:
                    sio.write(self._run())
                    if (start_time + sec) < time.time():
                        break
            return sio.getvalue()
    def _run(self):
        timeout = 4000
        sio = StringIO()
        if self.host == 'local':
            prompt = re.compile(r"^[^#]+[#$] ", re.MULTILINE)
            print "START >> LOCAL (%s)" % (self.host)
            cmd = "sh"
            try:
                sh = pexpect.spawn(cmd, timeout=timeout)
                sh.logfile = sio
                sh.logfile_write = None
                for line in self.source.splitlines():
                    self.processing(sh, line, prompt)
                if sh.isalive():
                    (sh.logfile, temp) = (None, sh.logfile)
                    sh.sendline("exit")
                    sh.logfile = temp
                    sh.read()
                    sh.close()
            except ExceptionPexpect, err:
                sio.write("# %s\n" % cmd)
                sio.write("%s\n" % err)
        else:
            host = env.getAddr(self.host)
            if self.account:
                account = env.getAccount(self.account)
                user = account.user
                passwd = account.passwd
            else:
                user = self.user
                passwd = self.passwd
            if self.protocol == u'telnet':
                prompt = re.compile(r"^[^#]+[#$] ", re.MULTILINE)
                cmd = 'telnet %s' % host
                print "START >> TELNET %s:%s@%s (%s)" % (user, passwd, host, cmd)
                try:
                    tn = pexpect.spawn(cmd, timeout=timeout)
                    tn.logfile = sio
                    tn.expect('login: ')
                    (tn.logfile, temp) = (None, tn.logfile)
                    tn.sendline(user)
                    tn.logfile = temp
                    index = tn.expect(['Password: ', prompt])
                    if index == 0:
                        (tn.logfile, temp) = (None, tn.logfile)
                        tn.sendline(passwd)
                        tn.logfile = temp
                        tn.expect(prompt)
                    for line in self.source.splitlines():
                        self.processing(tn, line, prompt)
                    if tn.isalive():
                        (tn.logfile, temp) = (None, tn.logfile)
                        tn.sendline("exit")
                        tn.logfile = temp
                        tn.read()
                        tn.close()
                except ExceptionPexpect, err:
                    sio.write("%s# %s\n" % (host, cmd))
                    sio.write("%s\n" % err)

            elif self.protocol == u'ftp':
                prompt = re.compile(r"^[^>]+> ", re.MULTILINE)
                cmd = 'ftp %s' % host
                print "START >> FTP %s:%s@%s (%s)" % (user, passwd, host, cmd)
                try:
                    ftp = pexpect.spawn(cmd, timeout=timeout)
                    ftp.logfile = sio
                    ftp.expect(": ")
                    (ftp.logfile, temp) = (None, ftp.logfile)
                    ftp.sendline(user)
                    ftp.logfile = temp
                    index = ftp.expect(["Password:", prompt])
                    if index == 0:
                        (ftp.logfile, temp) = (None, ftp.logfile)
                        ftp.sendline(passwd)
                        ftp.logfile = temp
                        ftp.expect(prompt)
                    for line in self.source.splitlines():
                        self.processing(ftp, line, prompt)
                    if ftp.isalive():
                        (ftp.logfile, temp) = (None, ftp.logfile)
                        ftp.sendline("bye")
                        ftp.logfile = temp
                        ftp.read()
                        ftp.close()
                except ExceptionPexpect, err:
                    sio.write("%s> %s\n" % (host, cmd))
                    sio.write("%s\n" % err)
        return sio.getvalue()

class Test(object):
    def __init__(self):
        self.id = ""
        self.title = ""
        self.description = ""
        self.pubDate = ""
        self.procedure = {}
    def parse(self, root):
        self.id = root.getAttribute(u'id')
        print root.__dict__
        self.title = root.getElementsByTagName(u'title')[0].firstChild.data
        self.description = root.getElementsByTagName(u'description')[0].firstChild.data
        self.pubDate = root.getElementsByTagName(u'pubDate')[0].firstChild.data
        for node in root.getElementsByTagName(u'procedure')[0].childNodes:
            try:
                scripts = []
                for nodescript in node.getElementsByTagName(u'script'):
                    script = Script()
                    script.parse(nodescript)
                    scripts.append(script)
                self.procedure[node.tagName] = scripts
            except AttributeError, err:
                continue
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
    def toXmlElements(self, doc):
        return self.report.toXmlElements(doc)

class Tests(object):
    def __init__(self):
        self.tests_list = []
        self.test_list = []
        self.id = None
        self.reports = []
    def parse(self, root):
        self.id = root.getAttribute(u'id')
        for node in root.childNodes:
            try:
                tag = node.tagName
            except:
                continue
            if tag == u'test':
                test = Test()
                test.parse(node)
                self.test_list.append(test)
            elif tag == u'tests':
                tests = Tests()
                tests.parse(node)
                self.test_list.append(tests)
    def run(self):
        reports = []
        for test in self.test_list:
            reports.append(test.run())
        for tests in self.tests_list:
            reports.append(tests.run())
        return reports
    def toXmlElements(self, doc):
        reports = doc.createElement(u'reports')
        for test in self.test_list:
            reports.appendChild(test.toXmlElements(doc))
        for tests in self.tests_list:
            reports.appendChild(tests.toXmlElements(doc))
        return reports

class EnvParam(object):
    def __init__(self, element=None, **kwds):
        self.name = kwds.get("name", None)
        if element:
            self.parse(element)
    def parse(self, element):
        self.name = element.getAttribute(u'name')

class Account(EnvParam):
    def __init__(self, element=None, **kwds):
        super(Account, self).__init__(**kwds)
        self.host = kwds.get("host", None)
        self.user = kwds.get("user", None)
        self.passwd = kwds.get("passwd", None)
        if element:
            self.parse(element)
    def parse(self, element):
        super(Account, self).parse(element)
        self.host = element.getAttribute(u'host')
        self.user = element.getAttribute(u'user')
        self.passwd = element.getAttribute(u'passwd')

class Host(EnvParam):
    def __init__(self, element=None, **kwds):
        super(Host, self).__init__(**kwds)
        self.addr = kwds.get("addr", None)
        if element:
            self.parse(element)
    def parse(self, element):
        super(Host, self).parse(element)
        self.addr = element.getAttribute(u'addr')

class Env(object):
    def __init__(self, root=None):
        self.accounts = {}
        self.hosts = {}
        if root:
            self.parse(root)
    def parse(self, root):
        for element in root.getElementsByTagName(u'account'):
            account = Account(element)
            self.accounts[account.name] = account
        for element in root.getElementsByTagName(u'host'):
            host = Host(element)
            self.hosts[host.name] = host
    def getAddr(self, name):
        return self.hosts[name].addr
    def getAccount(self, name):
        return self.accounts[name]

def test():
    testfile = "../xml/test.xml"

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

    tests = Tests()
    tests.parse(testroot.getElementsByTagName(u'tests')[0])
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

if __file__ == "__main__":
    test()

#
# EOF
#
