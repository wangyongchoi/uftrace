#!/usr/bin/env python

from runtest import TestBase
import subprocess as sp

TDIR='xxx'

class TestCase(TestBase):
    def __init__(self):
        TestBase.__init__(self, 'sleep', """
{"traceEvents":[
{"ts":56466448731,"ph":"B","pid":32537,"name":"main"},
{"ts":56466448731,"ph":"B","pid":32537,"name":"foo"},
{"ts":56466448742,"ph":"B","pid":32537,"name":"bar"},
{"ts":56466448743,"ph":"B","pid":32537,"name":"usleep"},
{"ts":56466450823,"ph":"E","pid":32537,"name":"usleep"},
{"ts":56466450827,"ph":"E","pid":32537,"name":"bar"},
{"ts":56466450834,"ph":"E","pid":32537,"name":"foo"},
{"ts":56466450835,"ph":"E","pid":32537,"name":"main"}
], "metadata": {
"command_line":"uftrace record -d xxx t-sleep ",
"recorded_time":"Mon Oct  3 22:45:57 2016"
} }
""")

    def pre(self):
        record_cmd = '%s record -d %s %s' % (TestBase.ftrace, TDIR, 't-' + self.name)
        sp.call(record_cmd.split())
        return TestBase.TEST_SUCCESS

    def runcmd(self):
        return '%s dump -d %s -t 1ms --chrome' % (TestBase.ftrace, TDIR)

    def post(self, ret):
        sp.call(['rm', '-rf', TDIR])
        return ret

    def sort(self, output):
        """ This function post-processes output of the test to be compared .
            It ignores blank and comment (#) lines and remaining functions.  """
        import json

        result = []
        o = json.loads(output)
        for ln in o['traceEvents']:
            result.append("%s %s" % (ln['ph'], ln['name']))
        return '\n'.join(result)
