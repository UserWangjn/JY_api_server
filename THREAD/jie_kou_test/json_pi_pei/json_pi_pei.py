# uncompyle6 version 3.3.4
# Decompiled from: Python 3.7.3 (default, Jun 24 2019, 04:54:02)
# [GCC 9.1.0]
# Embedded file name: C:\Users\sunzhen\Desktop\web flask\HGTP_socket3\app\jie_kou_test\json_pi_pei\json_pi_pei.py
# Compiled at: 2019-04-08 13:04:05
import sys
sys.path.append('../../')
import json
from .excel_data import *

def creat_json(v, data):
    if type(data) not in [list, dict]:
        j = json.loads(data)
    else:
        j = data
    if isinstance(v, dict):
        for k in v:
            if k == 'id_canshu':
                k = 'id'
            if k == 'result_data':
                k = 'result'
            if v[k] == 'change_json':
                v[k] = j[k]
            elif isinstance(v[k], (dict, list)):
                if k not in j:
                    v.pop(k)
                    continue
                else:
                    if type(j[k]) not in [float, int, int] and j[k] != None:
                        try:
                            j[k].strip() == 'data_empty'
                        except:
                            pass

                        if j[k].strip() == 'data_empty':
                            v[k] = ''
                            continue
                        elif j[k] != None and j[k].strip() == '':
                            v.pop(k)
                            continue
                s = change(v[k], j[k])
                v[k] = s

                if type(j[k]) not in [float, int, int] and j[k].strip() == '':
                    continue
                s = change(v[k], j[k])
                v[k] = s
            elif type(v[k]) == list:
                for z in v[k]:
                    creat_json(z, j)

            elif type(v[k]) == dict:
                creat_json(v[k], j)

    return json.dumps(v)




def change(a, b):
    if b == 0.0:
        b = 0
    if type(b) == bool or b == None:
        pass
    else:
        if type(a) == int:
            try:
                b = int(b)
            except:
                pass

        else:
            if type(a) == float:
                try:
                    if float(b) == int(b):
                        b = int(b)
                    else:
                        b = float(b)
                except:
                    pass

            else:
                if type(a) in [str, str]:
                    b = str(b)
                else:
                    try:
                        float(b)
                    except:
                        if type(b) not in [float, int]:
                            pass
                    else:
                        b = str(b).split('.')[0]

    return b


def json_change(a, b):
    if type(a) in [dict, list]:
        if type(a) == list:
            for k, i in enumerate(a):
                if type(a[k]) in [list, dict]:
                    json_change(a[k], b[k])
                else:
                    if type(b[k]) == 'float' and b[k] == int(b[k]):
                        b[k] = int[b[k]]
                    if type(a[k]) == int:
                        b[k] = int(b[k])
                    elif type(a[k]) == float:
                        b[k] = float(b[k])
                    elif type(a[k]) == bool:
                        b[k] = bool(b[k])
                    elif type(a[k]) in [str, str] and a[k] != 'change_json':
                        b[k] = str(b[k])

        elif type(a) == dict:
            for k in a:
                if type(b) == dict and k in list(b.keys()):
                    if type(a[k]) in [list, dict]:
                        json_change(a[k], b[k])
                    else:
                        if type(b[k]) == 'float' and b[k] == int(b[k]):
                            b[k] = int[b[k]]
                        if type(a[k]) == int:
                            b[k] = int(b[k])
                        elif type(a[k]) == float:
                            b[k] = float(b[k])
                        elif type(a[k]) == bool:
                            b[k] = bool(b[k])
                        elif type(a[k]) in [str, str] and a[k] != 'change_json':
                            b[k] = str(b[k])
                        elif type(a[k]) in [str, str] and a[k] != 'empty_data':
                            b[k] = ''


def change_json_data(v, excel_data):
    if v != '':
        if type(v) not in [list, dict]:
            try:
                v = json.loads(v)
            except:
                pass

        if type(v) == dict:
            for k in v:
                if type(v[k]) not in [str, str]:
                    change_json_data(v[k], excel_data)
                elif v[k] == 'change_json':
                    for u in excel_data:
                        if u == k:
                            try:
                                excel_data[u] = json.loads(excel_data[u])
                            except:
                                pass

    return excel_data