#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
from utils_1c import argparse_1c, connection_1c
import os
from time import sleep

parser = argparse_1c.ArgumentParser_1C("sBudkf", description=__doc__)
parser.decode_arg()

with connection_1c.Connection(srv=parser.args["server"][0], **parser.args) as conn:
    tmp_dt = '/tmp/screenshot.png'
    conn.cast("DISPLAY=:1 xwd -root -silent | convert xwd:- png:{}".format(tmp_dt))
    sleep(2)
    conn.move_file(tmp_dt, tmp_dt)
    os.popen("xdg-open {}".format(tmp_dt)).read()


#xdg-open /tmp/screenshot.png