#!/usr/bin/env python3
"""
exec_with_pipe.py
Parent writes lines to a pipe, children exec 'grep' to filter lines.
Demonstrates fork + exec + pipes.
"""
import os
import sys
import time

def run_exec_pipe():
    r, w = os.pipe()
    pid = os.fork()
    if pid == 0:
        # Child: execute grep to filter lines containing "ok"
        os.dup2(r, 0)   # replace stdin with read-end of pipe
        os.close(w)
        os.close(r)
        # exec grep
        os.execvp("grep", ["grep", "ok"])
        # if exec fails:
        print("Exec failed", file=sys.stderr)
        sys.exit(1)
    else:
        # Parent: write messages to pipe, close and wait
        os.close(r)
        wfd = os.fdopen(w, 'w')
        lines = ["this is ok\n", "this is not\n", "ok indeed\n"]
        for L in lines:
            wfd.write(L)
            wfd.flush()
            time.sleep(0.2)
        wfd.close()
        # wait for child to finish; capture exit status
        pid_done, status = os.waitpid(pid, 0)
        exit_code = os.WEXITSTATUS(status)
        print(f"Parent: child {pid_done} exited with code {exit_code}")

if __name__ == "__main__":
    run_exec_pipe()
