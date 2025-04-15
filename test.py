#!/usr/bin/env python3
def test():
    M = {}
    with open("/home/baal/200.log", "r") as f:
       while True:
           line = f.readline()
           if not line:
               break
           M[line] = None

    with open("/home/baal/201.log", "w") as f:
        f.writelines(M.keys())

test()


