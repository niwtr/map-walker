#! /usr/bin/python
# -*- coding: utf-8 -*-

'''
Log module.

Maintains the mechanism to write log.
Design: Heranort, L.Laddie
'''

import os, time, shutil

'''
Log mode.
If the mode turns to be 'testing', we must write down all the environment.
And if the mode is 'distributed', we should write at least all the information
we need.
'''
#mode=[]

class Log_file():
    def __init__(self):
        path = os.getcwd()
        pparent_path = os.path.dirname(os.path.dirname(path))   #get the root dir
        self.file_path = os.path.join(pparent_path, 'data')
        self.path_simple_log = os.path.join(self.file_path, 'log.txt')   #get the log path
        self.path_test_log = os.path.join(self.file_path, 'log_test.txt')
        self.open_log()

    '''
    No less and no more.
    '''
    def make_simple_log(self, env):
        pass

    '''
    Used Only during development of the program.
    '''
    def make_full_log(self, env):
        pass

    '''
    Analyze the log file to check where the bug is.
    '''
    def analyzer(self):
        pass

    '''
    Open the log file
    '''
    def open_log(self):
        line_num = 0
        if(os.path.isfile(self.path_simple_log)):
            temp = open(self.path_simple_log, 'r')
            lines = temp.readlines()
            temp.close()
            line_num = len(lines)
        self.log_simple = open(self.path_simple_log, 'a')  #open the log txt with a additional mode
        self.log_test = open(self.path_test_log, 'a')
        if(line_num >= 1000):   #check the log size
            self.roll_log()

    '''
    Preserve the old log
    '''
    def roll_log(self):
        for i in range(1000):
            file_name = os.path.join(self.file_path, 'log_pre_%d.log' % i)
            if(os.path.isfile(file_name)):
                continue
            self.log_simple.close()
            shutil.move(self.path_simple_log, file_name)
            self.open_log()
            self.info('log roll to %s', file_name)
            return

    '''
    Write log to the actual disk.
    '''
    def write_log(self, mode, fmt, *msg):
        str = '%s - [%s] %s\n' % (time.ctime()[4:], mode, fmt % msg)
        self.log_simple.write(str)
        try:
            self.log_simple.flush()
        except:
            pass

    '''
    Three different types of log
    '''
    def debug(self, fmt, *msg):
        self.write_log('DEBUG', fmt, *msg)

    def info(self, fmt, *msg):
        self.write_log('INFO', fmt, *msg)

    def warn(self, fmt, *msg):
        self.write_log('WARN', fmt, *msg)

log_file = Log_file()

if(__name__ == '__main__'):
    log_file.debug('test')
    log_file.debug('%d*%s', 272, 'test')
    log_file.info('%d*%s', 1954, 'test')
    for i in range(1500):
        log_file.warn('%d*%s', i, 'test')