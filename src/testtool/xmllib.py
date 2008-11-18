#!/usr/bin/env python
#
#
#
#
from tests import *
from script import *
from xml.dom import minidom
import re
from cStringIO import StringIO

# TestTool
def TestTool_loadXml(self, xmlfile):
    doc = minidom.parse(xmlfile)

    self.env = Env()
    self.env.fromXml(doc.getElementsByTagName(u'env')[0])
    root = doc.getElementsByTagName(u'autotest')[0]
    self.title = root.getElementsByTagName(u'title')[0].firstChild.data
    author = root.getElementsByTagName(u'author')[0]
    self.author = author.getElementsByTagName(u'name')[0].firstChild.data
    self.mtime = root.getElementsByTagName(u'pubDate')[0].firstChild.data

    self.tests = Tests(self.env)
    self.tests.fromXml(root.getElementsByTagName(u'tests')[0])
TestTool.loadXml = TestTool_loadXml

def TestTool_saveXml(self, xmlfile):
    doc = minidom.parseString('<?xml-stylesheet type="text/xsl" href="report_html.xsl"?><autotest></autotest>')

    root = doc.getElementsByTagName(u'autotest')[0]
    reports = self.tests.toXml(doc)
    reports.setAttribute(u'start', time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime(self.starttime)))
    reports.setAttribute(u'end', time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime(self.endtime)))
    root.appendChild(reports)

    output = file(xmlfile, "w")
    try:
        output.write(doc.toxml().encode('utf-8'))
    finally:
        output.close()
TestTool.saveXml = TestTool_saveXml

# Report
def Report_toXml(self, doc):
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
Report.toXml = Report_toXml

# Script
def Script_fromXml(self, root):
    self.host = root.getAttribute(u'host')
    self.protocol = root.getAttribute(u'protocol')
    self.source = root.firstChild.data
    self.account = root.getAttribute(u'account')
    if not self.account:
        self.user = root.getAttribute(u'user')
        self.passwd = root.getAttribute(u'passwd')
    self.loop = root.getAttribute(u'loop')
    if not self.protocol or self.protocol == "local":
        self.__class__ = LocalScript
    elif self.protocol == "telnet":
        self.__class__ = TelnetScript
    elif self.protocol == "ftp":
        self.__class__ = FtpScript
    else:
        print "%s!!" % self.protocol
Script.fromXml = Script_fromXml

# Test
def Test_fromXml(self, root):
    self.id = root.getAttribute(u'id')
    self.title = root.getElementsByTagName(u'title')[0].firstChild.data
    self.description = root.getElementsByTagName(u'description')[0].firstChild.data
    self.pubDate = root.getElementsByTagName(u'pubDate')[0].firstChild.data
    for node in root.getElementsByTagName(u'procedure')[0].childNodes:
        try:
            scripts = []
            for nodescript in node.getElementsByTagName(u'script'):
                script = Script(self.env)
                script.fromXml(nodescript)
                scripts.append(script)
            self.procedure[node.tagName] = scripts
        except AttributeError, err:
            continue
Test.fromXml = Test_fromXml

def Test_toXml(self, doc):
    return self.report.toXml(doc)
Test.toXml = Test_toXml

# Tests
def Tests_fromXml(self, root):
    self.clause = root.getAttribute(u'clause')
    for node in root.childNodes:
        try:
            tag = node.tagName
        except:
            continue
        if tag == u'title':
            self.title = node.firstChild().data
        elif tag == u'test':
            test = Test(self.env)
            test.fromXml(node)
            self.test_list.append(test)
        elif tag == u'tests':
            tests = Tests(self.env)
            tests.fromXml(node)
            self.test_list.append(tests)
Tests.fromXml = Tests_fromXml

def Tests_toXml(self, doc):
    reports = doc.createElement(u'reports')
    for test in self.test_list:
        reports.appendChild(test.toXml(doc))
    for tests in self.tests_list:
        reports.appendChild(tests.toXml(doc))
    return reports
Tests.toXml = Tests_toXml

# EnvParam
def EnvParam_fromXml(self, element):
    self.name = element.getAttribute(u'name')
EnvParam.fromXml = EnvParam_fromXml

# Account
def Account_fromXml(self, element):
    super(Account, self).fromXml(element)
    self.host = element.getAttribute(u'host')
    self.user = element.getAttribute(u'user')
    self.passwd = element.getAttribute(u'passwd')
Account.fromXml = Account_fromXml

# Host
def Host_fromXml(self, element):
    super(Host, self).fromXml(element)
    self.addr = element.getAttribute(u'addr')
Host.fromXml = Host_fromXml

# Env
def Env_fromXml(self, root):
    for element in root.getElementsByTagName(u'account'):
        account = Account(element)
        self.accounts[account.name] = account
    for element in root.getElementsByTagName(u'host'):
        host = Host(element)
        self.hosts[host.name] = host
Env.fromXml = Env_fromXml

#
# EOF
#
