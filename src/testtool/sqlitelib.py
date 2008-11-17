#!/usr/bin/env python
#
#
#
#
from tests import *
from script import *
import re
import sqlite3

def dbopen(dbfile="db"):
    return sqlite3.connect(dbfile)

def TestTool_saveSql(self, dbfile):
    print self.__dict__
    finished = False
    con = dbopen(dbfile)
    try:
        createtable(con)
        con.commit()
        cur = con.cursor()
        # info
        for item in (("title", self.title),
                     ("mtime", self.mtime),
                     ("author", self.author),
                     ):
            cur.execute('update info set value="%s" where name = "%s"' % (item[1], item[0]) )
        con.commit()
        self.tests.commitSql(con)
        finished = True
        dump(con)
#    except:
#        print "Exception!!"
#        if not finished:
#            con.rollback()
    finally:
        con.close()
TestTool.saveSql = TestTool_saveSql

# Report
def Report_commitSql(self, con):
    try:
        cur = con.cursor()
        cur.execute('''
insert into report(test_id, reports_id, ctime, result, log) valuses(?,?,?,?,?)
)''', (self.test_id, self.report_id, timenow(), self.result, self.log,))
    except:
        con.rollback()
    else:
        con.commit()
Report.commitSql = Report_commitSql

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
    return self.report.toXml(doc)
Test.toXml = Test_toXml

# Tests
def Tests_commitSql(self, con):
    try:
        cur = con.cursor()
        cur.execute('insert into clause')
    except:
        con.rollback()
    else:
        con.commit()

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

def dump(con):
    cur = con.cursor()
    for tbl in ["info", "clause1", "clause2", "clause3", "test", "reports", "report", "report"]:
        print "[%s]" % tbl
        cur.execute('select * from %s' % tbl)
        for row in cur:
            print row

def createtable(con):
    con.executescript('''
create table if not exists info (
  name text unique,
  value text
);
insert or ignore into info(name,value) values("title","");
insert or ignore into info(name,value) values("author","");
insert or ignore into info(name,value) values("mtime","");
create table if not exists clause (
  clause1 integer not null,
  clause2 integer,
  clause3 integer,
  title text
);
create table if not exists test (
  idx integer primary key,
  clause1 integer,
  clause2 integer,
  clause3 integer,
  title text,
  description text,
  ctime datetime,
  procedure text
);
create table if not exists reports (
  idx integer primary key,
  starttime datetime,
  endtime datetime
);
create table if not exists report (
  idx integer primary key,
  test_id integer,
  reports_id integer,
  ctime datetime
  result integer,
  log text
);
''')

def test():
    import xmllib

    tool = TestTool()
    tool.loadXml("../../xml/test.xml")
    tool.saveSql("dbtest")

if __name__ == "__main__":
    test()


#
# EOF
#
