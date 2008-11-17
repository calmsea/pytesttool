#!/usr/bin/env python
#
#
#
#
from string import Template
from script import *
import re
import sqlite3

class TestToolSql(object):
    def __init__(self):
        self.dbfile = "testtool.db"
        self.createtable()

    def openDb(self):
        return sqlite3.connect(self.dbfile)
    
    def createtable(self):
        con = self.openDb()
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
  clause1 integer default 0,
  clause2 integer default 0,
  clause3 integer default 0,
  title text default NULL,
  description text default NULL,
  ctime datetime default CURRENT_TIMESTAMP,
  procedure text default NULL
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
        con.commit()

    def addTest(self, **kwds):
        t_insert = Template('''
insert into test
    (clause1, clause2, clause3, title, procedure)
    values ($clause1, $clause2, $clause3, $title, $procedure)
''')
        clause = map(int, kwds.get("clause", "1").split("-"))
        if len(clause) < 3:
            clause.extend([0, 0, 0])
        clause1, clause2, clause3 = clause[0:3]
        if kwds.has_key("title"):
            title = "\"%s\"" % kwds.get("title")
        else:
            title = "NULL"
        procedure = kwds.get("procedure", "NULL")
        con = self.openDb()
        cur = con.cursor()
        print t_insert.substitute(locals())
        cur.execute(t_insert.substitute(locals()))
        con.commit()

    def show(self):
        cur = self.openDb().cursor()
        for tbl in ["info", "clause", "test", "reports", "report", "report"]:
            print "[%s]" % tbl
            cur.execute('select * from %s' % tbl)
            for row in cur:
                print row

    def showTest(self):
        cur = self.openDb().cursor()
        cur.execute('select distinct clause1 from test')
        for c1 in map(lambda x: x[0], cur):
            cur.execute('select distinct clause2 from test where clause1 = %d' % c1)
            for c2 in map(lambda x: x[0], cur):
                cur.execute('select distinct clause3 from test where clause1 = %d and clause2 = %d' % (c1, c2))
                for c3 in map(lambda x: x[0], cur):
                    cur.execute('''
select clause1, clause2, clause3, title from test t1 
    where clause1 = %d
        and clause2 = %d
        and clause3 = %d
    order by ctime desc, idx desc limit 1''' % (c1, c2, c3))
                    for row in cur:
                        print "[clause %.3d-%.3d-%.3d]" % (row[0], row[1], row[2]),
                        print "Title = %s" % row[3]
                        
#        cur.execute('''
#select * from test t1 
#    where not exists (
#        select 1 from test t2 where 
#            t1.clause1 = t2.clause1
#            and t1.clause2 = t2.clause2
#            and t1.clause3 = t2.clause3
#            and (
#                t1.ctime < t2.ctime
#                or (t1.ctime = t2.ctime and t1.idx < t2.idx)
#            )
#        );
#''')
#        for row in cur:
#            print row
            
    def clear(self):
        con = self.openDb()
        con.execute("drop table test")
        con.commit()

def test():
    tool = TestToolSql()
#    tool.clear()
    tool = TestToolSql()
#    for n1 in xrange(4):
#        for n2 in xrange(10):
#            c1 = n1 + 1
#            c2 = n2 + 1
#            tool.addTest(title="test%.3d-%.3d" % (c1, c2), clause="%d-%d" % (c1, c2))
    tool.show()
    tool.showTest()

if __name__ == "__main__":
    test()


#
# EOF
#
