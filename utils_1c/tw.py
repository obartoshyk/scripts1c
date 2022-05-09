#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import threading
from time import sleep


class ThreadWorker(object):
    """The basic idea is given a function create an object.
    The object can then run the function in a thread.
    It provides a wrapper to start it,check its status,and get data out the function."""
    def __init__(self, target) -> object:
        self.thread = None
        self.data = None
        self.target = self.save_data(target)

    def save_data(self, func):
        def new_func(*args, **kwargs):
            self.data = func(*args, **kwargs)

        return new_func

    def start(self, args):
        self.thread = threading.Thread(target=self.target, args=args)
        self.thread.start()
        return self.thread.is_alive()

    def is_alive(self):
        if self.thread is None:
            return False
        else:
            return self.thread.is_alive()

    def get_data(self):
        return self.data

    def make_work(self, args, countdown):
        done = False
        self.start(args)
        timer = countdown
        while timer > 0 and not done:
            sleep(5)
            timer = timer - 5
            if not self.is_alive():
                done = True
                break
        return done
