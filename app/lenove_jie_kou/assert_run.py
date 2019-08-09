# -*- coding: utf-8 -*-
# uncompyle6 version 3.3.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.7.3 (default, Jun 24 2019, 04:54:02) 
# [GCC 9.1.0]
# Embedded file name: C:\jieyuelianhe\old_all_server\HGTP_server\app\lenove_jie_kou\assert_run.py
# Compiled at: 2018-08-23 09:49:41
__author__ = 'SUNZHEN519'
import sys
sys.path.append('../../')
import json, demjson

class assert_run(object):

    def __init__(self):
        pass

    def walk_find(self, v, j):
        if type(v) == dict:
            for k, i in v.items():
                if type(i) != dict and type(i) != list:
                    if i == '*':
                        try:
                            assert str(j[k])
                        except:
                            return False

                    else:
                        try:
                            assert i == j[k]
                        except:
                            return False

            for k, i in v.items():
                if type(i) == dict:
                    self.walk_find(i, j[k])
                if type(i) == list:
                    for b in i:
                        statu = 0
                        for z in j[k]:
                            for u, a in b.items():
                                if type(u) != list and type(u) != dict:
                                    if u in list(z.keys()) and a == z[u]:
                                        pass
                                    else:
                                        statu = 1
                                        break

                            if statu == 0:
                                break

                        self.walk_find(b, z)

        return 1