#!/usr/bin/env python
#
#
#
#
from tests import *
from script import *
import re
from cStringIO import StringIO

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
    print root.__dict__
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
    return self.report.toXmlElements(doc)
Test.toXml = Test_toXml

# Tests
def Tests_fromXml(self, root):
    self.id = root.getAttribute(u'id')
    for node in root.childNodes:
        try:
            tag = node.tagName
        except:
            continue
        if tag == u'test':
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
        reports.appendChild(test.toXmlElements(doc))
    for tests in self.tests_list:
        reports.appendChild(tests.toXmlElements(doc))
    return reports
Tests.toXml = Test_toXml

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
