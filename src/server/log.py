#! /usr/bin/python
# -*- coding: utf-8 -*-

'''
Log module.

Maintains the mechanism to write log.
Design: Heranort
'''

'''
Log mode.
If the mode turns to be 'testing', we must write down all the environment.
And if the mode is 'distributed', we should write at least all the information
we need.
'''
mode=[]

'''
Path of the log file.
'''
log_path="~/map-walker/test/log.txt"



'''
No less and no more.
'''
def make_simple_log(env):
    pass

'''
Used Only during development of the program.
'''
def make_full_log(env):
    pass


'''
Write log to the actual disk.
'''
def write_log(msg):
    with open(log_path, "a") as lf:
        
    pass


'''
Analyze the log file to check where the bug is.
'''
def analyzer():
    pass