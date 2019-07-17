# -*- coding: utf-8 -*-
# uncompyle6 version 3.3.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.7.3 (default, Jun 24 2019, 04:54:02) 
# [GCC 9.1.0]
# Embedded file name: C:\jieyuelianhe\old_all_server\HGTP_server\app\shell_name.py
# Compiled at: 2018-08-23 09:48:54
__author__ = 'SUNZHEN519'
import os
from flask import Flask, render_template, session

class file(object):

    def __init__(self, *mulu):
        if len(mulu) == 0:
            self.cd = 'D:\\efq_ben'
        else:
            self.cd = 'D:\\' + mulu[0] + '\\'

    def xx(self):
        files = []
        for parent, dirnames, filenames in os.walk(self.cd):
            for i in filenames:
                if '.py' in i and '.pyc' not in i and 'mulu44' not in i:
                    files.append(i)

        return files