#!/usr/bin/env python
import os
import pty
import subprocess
# https://stackoverflow.com/questions/1283061/python-capture-popen-stdout-and-display-on-console
def call_and_peek_output(cmd, shell=False):
    # Create a new pair master, slave
    master, slave = pty.openpty()
    print cmd
    p = subprocess.Popen(cmd, shell=shell, stdin=None, stdout=slave, close_fds=True)
    os.close(slave)
    line = ""
    while True:
        try:
            ch = os.read(master, 1)
        except OSError:
            # We get this exception when the spawn process closes all references to the
            # pty descriptor which we passed him to use for stdout
            # (typically when it and its childs exit)
            break
        line += ch
        if ch == '\n':
            yield line
            line = ""
    if line:
        yield line

    ret = p.wait()
    if ret:
        raise subprocess.CalledProcessError(ret, cmd)


if __name__ == '__main__':
    counter = 0
    try:
        for l in call_and_peek_output(['docker run --rm --net=host -ti cloudflare/goflow:latest -sflow=false -loglevel=debug -kafka=false'], shell=True):
            counter += 1
            if counter % 500 == 0:
                print("{}\n".format(counter))
    except:
        print(counter)
