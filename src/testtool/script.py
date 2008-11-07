#!/usr/bin/env python
#
#
#
#
import time
import pexpect
import re
from pexpect import ExceptionPexpect
from cStringIO import StringIO

class Script(object):
    def __init__(self, env):
        self.host = ""
        self.protocol = ""
        self.source = ""
        self.account = ""
        self.loop = ""
        self.timeout = 4000
        self.sout = StringIO()
        self.env = env
    def processing(self, pe, line):
        print "prompt> %s" % line
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
            pe.expect(self.prompt)
        else:
            (pe.logfile, temp) = (None, pe.logfile)
            pe.sendline(line)
            pe.logfile = temp
            pe.expect(self.prompt)
        return
    def run(self):
        if not self.loop:
            self._run()
        else:
            cmd, val = self.loop.split(":")
            if cmd == "count":
                cnt = int(val)
                for n in xrange(cnt):
                    self._run()
            elif cmd == "while":
                sec = int(val)
                start_time = time.time()
                while True:
                    self._run()
                    if (start_time + sec) < time.time():
                        break
        return self.sout.getvalue()

    def _run(self):
        self.run_initialize()
        self.run_main()
        self.run_finalize()

    def run_initialize(self):
        pass
    def run_finalize(self):
        pass

class LocalScript(Script):
    prompt = re.compile(r"^[^#]+[#$] ", re.MULTILINE)
    def run_main(self):
        print "START >> LOCAL (%s)" % (self.host)
        cmd = "sh"
        try:
            sh = pexpect.spawn(cmd, timeout=self.timeout, logfile = self.sout)
            for line in self.source.splitlines():
                self.processing(sh, line)
            if sh.isalive():
                (sh.logfile, temp) = (None, sh.logfile)
                sh.sendline("exit")
                sh.logfile = temp
                sh.read()
                sh.close()
        except ExceptionPexpect, err:
            self.sout.write("# %s\n" % cmd)
            self.sout.write("%s\n" % err)

class TelnetScript(Script):
    prompt = re.compile(r"^[^#]+[#$] ", re.MULTILINE)

    def run_main(self):
        host = self.env.getHost(self.host).addr
        if self.account:
            account = self.env.getAccount(self.account)
            user = account.user
            passwd = account.passwd
        else:
            user = self.user
            passwd = self.passwd

        cmd = 'telnet %s' % host
        print "START >> TELNET %s:%s@%s (%s)" % (user, passwd, host, cmd)
        try:
            tn = pexpect.spawn(cmd, timeout=self.timeout, logfile=self.sout)
            tn.expect('login: ')
            (tn.logfile, temp) = (None, tn.logfile)
            tn.sendline(user)
            tn.logfile = temp
            index = tn.expect(['Password: ', self.prompt])
            if index == 0:
                (tn.logfile, temp) = (None, tn.logfile)
                tn.sendline(passwd)
                tn.logfile = temp
                tn.expect(self.prompt)
            for line in self.source.splitlines():
                self.processing(tn, line)
            if tn.isalive():
                (tn.logfile, temp) = (None, tn.logfile)
                tn.sendline("exit")
                tn.logfile = temp
                tn.read()
                tn.close()
        except ExceptionPexpect, err:
            self.sout.write("%s# %s\n" % (host, cmd))
            self.sout.write("%s\n" % err)

class FtpScript(Script):
    prompt = re.compile(r"^[^>]+> ", re.MULTILINE)
    def run_main(self):
        host = self.env.getHost(self.host).addr
        if self.account:
            account = self.env.getAccount(self.account)
            user = account.user
            passwd = account.passwd
        else:
            user = self.user
            passwd = self.passwd

        cmd = 'ftp %s' % host
        print "START >> FTP %s:%s@%s (%s)" % (user, passwd, host, cmd)
        try:
            ftp = pexpect.spawn(cmd, timeout=self.timeout, logfile=self.sout)
            ftp.expect(": ")
            (ftp.logfile, temp) = (None, ftp.logfile)
            ftp.sendline(user)
            ftp.logfile = temp
            index = ftp.expect(["Password:", self.prompt])
            if index == 0:
                (ftp.logfile, temp) = (None, ftp.logfile)
                ftp.sendline(passwd)
                ftp.logfile = temp
                ftp.expect(self.prompt)
            for line in self.source.splitlines():
                self.processing(ftp, line)
            if ftp.isalive():
                (ftp.logfile, temp) = (None, ftp.logfile)
                ftp.sendline("bye")
                ftp.logfile = temp
                ftp.read()
                ftp.close()
        except ExceptionPexpect, err:
            self.sout.write("%s> %s\n" % (host, cmd))
            self.sout.write("%s\n" % err)

#
# EOF
#
