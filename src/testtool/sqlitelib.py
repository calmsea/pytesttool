#!/usr/bin/env python
#
#
#
#
from string import Template
from script import *
import re
import sqlite3
from tests import Test, TestToolBase

class TestToolSql(TestToolBase):
    def __init__(self):
        self.dbfile = "testtool.db"
        self.createtable()

    def openDb(self):
        return sqlite3.connect(self.dbfile)
    
    def createtable(self):
        con = self.openDb()
        con.executescript('''
-- Create Info Table
create table if not exists info (
  name text unique,
  value text
);
insert or ignore into info(name,value) values("title","");
insert or ignore into info(name,value) values("author","");
insert or ignore into info(name,value) values("ctime", datetime("now", "localtime"));
insert or ignore into info(name,value) values("mtime", datetime("now", "localtime"));

-- Create Clause Table
create table if not exists clause (
  clause1 integer not null,
  clause2 integer,
  clause3 integer,
  title text
);

-- Create Test Table
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

-- Create Report Table
create table if not exists report (
    idx integer primary key,
    testidx integer default NULL,
    ctime datetime default CURRENT_TIMESTAMP,
    result text default NULL,
    log text default NULL
);
''')
        con.commit()

    def addTest(self, test, clause):
        t_insert = Template('''
insert into test
    (clause1, clause2, clause3, title, description, procedure)
    values ($clause1, $clause2, $clause3, "$title", "$description", "$procedure"    )
''')
        if len(clause) < 3:
            clause.extend([0, 0, 0])
        clause1, clause2, clause3 = clause[0:3]
        title = test.title
        description = test.description
        procedure = test.procedure
        
        con = self.openDb()
        con.execute(t_insert.substitute(locals()))
        con.commit()

    def getTest(self, clause):
        t_select = Template('''
select clause1, clause2, clause3, title, description, procedure
    from test
    where clause1 = $clause1 and clause2 = $clause2 and clause3 = $clause3
    order by ctime desc, idx desc
    limit 0, 1
''')
        if len(clause) < 3:
            clause.extend([0, 0, 0])
        clause1, clause2, clause3 = clause[0:3]

        con = self.openDb()
        con.row_factory = sqlite3.Row
        row = con.execute(t_select.substitute(locals())).fetchone()
        return Test(title       = row["title"], 
                    description = row["description"], 
                    procedure   = row["procedure"])
        
    def addReport(self, report):
        t_insert = Template('''
insert into report
    (testidx, result, log)
    values ($test_idx, "$result", "$log")
''')
        test_idx = report.test_id
        result   = report.result
        log      = report.log
        
        con = self.openDb()
        print t_insert.substitute(locals())
        con.execute(t_insert.substitute(locals()))
        con.commit()

    def run(self, clause="all"):
        con = self.openDb()
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        if clause == "all":
            cur.execute('select distinct clause1, clause2, clause3 from test')
            for clause in cur:
                self.run(clause="-".join([str(clause[n]) for n in xrange(3)]))
        else:
            clause = map(int, clause.split("-"))
            cur.execute('''
select distinct * from test where clause1 = ? and clause2 = ? and clause3 =? order by ctime desc,idx desc
''', tuple(clause))
            ent = cur.fetchone()
            keys = ("title", "ctime", "description", "procedure", )
            d = dict([(key, ent[key]) for key in keys])
            print Test(**d)
            
    def show(self):
        con = self.openDb()
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        for tbl in ["info", "clause", "test", "reports", "report", "report"]:
            print "[%s]" % tbl
            cur.execute('select * from %s' % tbl)
            for row in cur:
                print row

    def showTest(self):
        con = self.openDb()
        con.row_factory = sqlite3.Row
        cur = con.cursor()
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
    order by ctime desc, idx desc limit 0, 1''' % (c1, c2, c3))
                    for row in cur:
                        print "[clause %.3d-%.3d-%.3d]" % (
                                        row["clause1"], row["clause2"], row["clause3"]),
                        print "Title = %s" % row["title"]
                        
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
        con.execute("drop table info")
        con.commit()
TestTool = TestToolSql

def test():
    tool = TestTool()
#    tool.clear()
    tool = TestTool()
    for n1 in xrange(4):
        for n2 in xrange(10):
            c1 = n1 + 1
            c2 = n2 + 1
            test = Test(title="test%.3d-%.3d" % (c1, c2), clause="%d-%d" % (c1, c2))
            tool.addTest(test, [c1,c2])
    tool.show()
    tool.showTest()
    tool.run()

if __name__ == "__main__":
    test()


#
# EOF
#
