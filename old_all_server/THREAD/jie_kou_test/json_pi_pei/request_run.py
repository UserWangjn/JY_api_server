# -*- coding: utf-8 -*-
# uncompyle6 version 3.3.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.7.3 (default, Jun 24 2019, 04:54:02) 
# [GCC 9.1.0]
# Embedded file name: E:\old_all_server\THREAD\THREAD_fuben\jie_kou_test\json_pi_pei\request_run.py
# Compiled at: 2019-05-06 18:19:42
__author__ = 'SUNZHEN519'
import sys
sys.path.append('../../')
import requests, copy
from json_pi_pei import *
from sing_data.sing_data import *
import urllib, urllib2, hashlib
from sing_data.sing_data import *
from excel_data import *

class request_run(object):

    def __init__(self, json_moban, path, mu_lu):
        self.json_moban = json_moban
        self.path = path
        if 'run_interval' in self.path.options('sign'):
            try:
                time.sleep(float(self.path.get('sign', 'run_interval')))
            except:
                pass

        self.url = self.path.get('config', 'url')
        self.config = dict(self.path.items('config'))
        self.sign = dict(self.path.items('sign'))

    def post_run(self, data, *url):
        self.data = data
        if len(url) != 0:
            self.sign_url = url[0].split(self.public_url)[(-1)]
            self.url = url[0]
            head = make_head(self.sign_url, self.sign['app_key'], data, self.config['method'], self.path)
        else:
            head = make_head(self.path.get('sign', 'url'), self.sign['app_key'], data, self.config['method'], self.path)
        try:
            response = requests.post(url=self.url, data=self.data, headers=head, verify=False)
        except:
            response = requests.post(url=self.url, data=self.data, headers=head, verify=False)

        return response

    def get_run(self, data, *url):
        if str(data).strip() != '':
            if len(url) != 0:
                url = url[0] + '?' + urllib.urlencode(eval(data))
            else:
                url = self.url + '?' + urllib.urlencode(eval(data))
        else:
            if len(url) == 0:
                url = self.url + '?' + urllib.urlencode(eval(data))
            else:
                url = url[0]
        self.sign_url = url.split(self.config['url'].split(self.sign['url'])[0])[(-1)]
        head = make_head(self.sign_url, self.sign['app_key'], data, self.config['method'], self.path)
        response = requests.get(url=url, headers=head, verify=False)
        return response

    def post(self, data, config, *url):
        data = change_data_db(config, data).data
        json_change(copy.deepcopy(self.json_moban), json.loads(data))
        if 'sign_type' not in dict(self.path.items('sign')).keys() or self.path.get('sign', 'sign_type') == 'web_nosign':
            head_data = {config.get('config', 'head_key'): config.get('config', 'head_value')}
            parm = json.loads(data)
            parm['api_key'] = config.get('sign', 'api_key')
            parm['sign'] = buildMySign(parm, config.get('sign', 'secretKey'))
            parm['api_key'] = config.get('sign', 'api_key')
            if len(url) != 0:
                if 'http://' in url[0] or 'https://' in url[0]:
                    all_url = url[0]
                else:
                    all_url = self.path.get('config', 'public_url') + url[0]
            else:
                all_url = self.url
            try:
                respons = requests.post(url=all_url, data=parm, headers=head_data, verify=False).text
            except Exception as e:
                respons = json.dumps({'error_detail': str(e)})

        if self.path.get('sign', 'sign_type') == 'v3':
            auth = CoinbaseExchangeAuth(config.get('sign', 'api_key'), config.get('sign', 'secretKey'), self.path.get('sign', 'password'))
            parm = json.loads(data)
            if len(url) != 0:
                if 'http://' in url[0] or 'https://' in url[0]:
                    all_url = url[0]
                else:
                    all_url = self.path.get('config', 'public_url') + url[0]
            else:
                all_url = self.url
            respons = requests.post(url=all_url, json=parm, auth=auth).text
        if self.path.get('sign', 'sign_type') == 'Backstage_web':
            parm = json.loads(data)
            print 777777777777777777777777777777777777777777777
            print self.path.get('login', 'token')
            header = {'Authorization': self.path.get('login', 'token'), 'Content-type': 'application/json'}
            if len(url) != 0:
                if 'http://' in url[0] or 'https://' in url[0]:
                    all_url = url[0]
                else:
                    all_url = self.path.get('config', 'public_url') + url[0]
            else:
                all_url = self.url
            try:
                if 'request_type' in self.path.options('config') and self.path.get('config', 'request_type').strip() == 'form_data':
                    header['Content-Type'] = 'application/x-www-form-urlencoded'
                    request = urllib2.Request(all_url, urllib.urlencode(parm), headers=header)
                    respons = urllib2.urlopen(request, timeout=60).read()
                else:
                    request = urllib2.Request(all_url, json.dumps(parm), headers=header)
                    respons = urllib2.urlopen(request, timeout=60).read()
            except Exception as e:
                respons = json.dumps({'error_detail': str(e)})

        if self.path.get('sign', 'sign_type') == 'zhixin':
            parm = json.loads(data)
            header = {'Cookie': self.path.get('login', 'token')}
            if len(url) != 0:
                if 'http://' in url[0] or 'https://' in url[0]:
                    all_url = url[0]
                else:
                    all_url = self.path.get('config', 'public_url') + url[0]
            else:
                all_url = self.url
            try:
                if 'request_type' in self.path.options('config') and self.path.get('config', 'request_type').strip() == 'form_data':
                    respons = urllib2.Request(url=all_url, data=urllib.urlencode(parm), headers=header)
                    respons = urllib2.urlopen(respons)
                    respons = respons.read()
                else:
                    respons = urllib2.Request(url=all_url, data=json.dumps(parm), headers=header)
                    respons = urllib2.urlopen(respons)
                    respons = respons.read()
            except Exception as e:
                respons = json.dumps({'error_detail': str(e)})

        if self.path.get('sign', 'sign_type') == 'haofang_server':
            parm = json.loads(data)
            header = json.loads(self.path.get('login', 'haofang_headertoken'))
            if len(url) != 0:
                if 'http://' in url[0] or 'https://' in url[0]:
                    all_url = url[0]
                else:
                    all_url = self.path.get('config', 'public_url') + url[0]
            else:
                all_url = self.url
            try:
                if 'request_type' in self.path.options('config') and self.path.get('config', 'request_type').strip() == 'form_data':
                    respons = urllib2.Request(url=all_url, data=urllib.urlencode(parm), headers=header)
                    respons = urllib2.urlopen(respons)
                    respons = respons.read()
                else:
                    respons = urllib2.Request(url=all_url, data=json.dumps(parm), headers=header)
                    respons = urllib2.urlopen(respons)
                    respons = respons.read()
            except Exception as e:
                respons = json.dumps({'error_detail': str(e)})

        if self.path.get('sign', 'sign_type') == 'hkci':
            parm = json.loads(data)
            header = json.loads(self.path.get('login', 'huasheng_headertoken'))
            if len(url) != 0:
                if 'http://' in url[0] or 'https://' in url[0]:
                    all_url = url[0]
                else:
                    all_url = self.path.get('config', 'public_url') + url[0]
            else:
                all_url = self.url
            try:
                if 'request_type' in self.path.options('config') and self.path.get('config', 'request_type').strip() == 'form_data':
                    respons = requests.post(all_url, data=data, headers=header)
                    respons = respons.text
                else:
                    respons = requests.post(all_url, json=json.loads(data), headers=header)
                    respons = respons.text
            except Exception as e:
                respons = json.dumps({'error_detail': str(e)})

        if self.path.get('sign', 'sign_type') == 'web':
            parm = json.loads(data)
            if self.path.has_option('sign', 'login') and self.path.get('sign', 'login') == 'false':
                header = {}
            else:
                hash = hashlib.md5()
                code = self.path.get('login', 'url').strip() + self.path.get('login', 'name').strip() + self.path.get('login', 'password').strip()
                hash.update(code)
                code = str(hash.hexdigest())
                header = json.loads([ self.path.get('login_value', i) for i in self.path.options('login_value') if code == i ][0])
            if len(url) != 0:
                if 'http://' in url[0] or 'https://' in url[0]:
                    all_url = url[0]
                else:
                    all_url = self.path.get('config', 'public_url') + url[0]
            else:
                all_url = self.url
            try:
                if 'request_type' in self.path.options('config') and self.path.get('config', 'request_type') == 'json':
                    respons = requests.post(all_url, data=json.dumps(parm), headers=header).text
                else:
                    header['authorization'] = 'UzAwMQ=='
                    request = urllib2.Request(all_url, urllib.urlencode(parm), headers=header)
                    respons = urllib2.urlopen(request, timeout=60).read()
            except Exception as e:
                respons = json.dumps({'error_detail': str(e)})

        if self.path.get('sign', 'sign_type') == 'app':
            parm = json.loads(data)
            header = {}
            head_key = self.path.get('config', 'head_key').split(',')
            head_value = self.path.get('config', 'head_value').split(',')
            if len(head_key) == len(head_value):
                head = dict(zip(head_key, head_key))
                header['Content-Type'] = 'application/json'
            else:
                header_dict = {'Content-Type': 'application/json'}
            header['Content-Type'] = 'application/json'
            if 'head_data' in self.path.sections():
                for k, i in json.loads(self.path.get('head_data', 'head_data')).iteritems():
                    header[k] = i

            if len(url) != 0:
                if 'http://' in url[0] or 'https://' in url[0]:
                    all_url = url[0]
                else:
                    all_url = self.path.get('config', 'public_url') + url[0]
            else:
                all_url = self.url
            try:
                if 'request_type' in self.path.options('config') and self.path.get('config', 'request_type').strip() == 'form_data':
                    header['Content-Type'] = 'application/x-www-form-urlencoded'
                    request = urllib2.Request(all_url, urllib.urlencode(parm), headers=header)
                    respons = urllib2.urlopen(request, timeout=60).read()
                else:
                    request = urllib2.Request(all_url, data=json.dumps(parm), headers=header)
                    respons = urllib2.urlopen(request, timeout=60).read()
                    print 4444444444444444444444444444444444444444
                    print respons
            except Exception as e:
                respons = json.dumps({'error_detail': str(e)})

            print '接口返回信息'
            print respons
        if self.path.get('sign', 'sign_type') == 'xiang_qian':
            parm = json.loads(data)
            header = {}
            head_key = self.path.get('config', 'head_key').split(',')
            head_value = self.path.get('config', 'head_value').split(',')
            if len(head_key) == len(head_value):
                head = dict(zip(head_key, head_key))
                header['Content-Type'] = 'application/json'
            else:
                header_dict = {'Content-Type': 'application/json'}
            header['Content-Type'] = 'application/json'
            if 'head_data' in self.path.sections():
                for k, i in json.loads(self.path.get('head_data', 'head_data')).iteritems():
                    header[k] = i

            if len(url) != 0:
                if 'http://' in url[0] or 'https://' in url[0]:
                    all_url = url[0]
                else:
                    all_url = self.path.get('config', 'public_url') + url[0]
            else:
                all_url = self.url
            en_de_aes = AESCipher('Jy_ApP_0!9i+90&#')
            parm = {'aesRequest': en_de_aes.encrypt(json.dumps(parm))}
            try:
                if 'request_type' in self.path.options('config') and self.path.get('config', 'request_type').strip() == 'form_data':
                    header['Content-Type'] = 'application/x-www-form-urlencoded'
                    request = urllib2.Request(all_url, urllib.urlencode(parm), headers=header)
                    respons = en_de_aes.decrypt(json.loads(urllib2.urlopen(request, timeout=60).read())['aesResponse'])
                else:
                    request = urllib2.Request(all_url, data=json.dumps(parm), headers=header)
                    respons = en_de_aes.decrypt(json.loads(urllib2.urlopen(request, timeout=60).read())['aesResponse'])
            except Exception as e:
                respons = json.dumps({'error_detail': str(e)})

            print '接口返回信息 '
            print respons
        if self.path.get('sign', 'sign_type') == 'jy_appServer':
            parm = all_jiami(data, self.path.get('sign_url', 'encode_url'))
            header = {}
            header['Content-Type'] = 'application/json'
            if len(url) != 0:
                if 'http://' in url[0] or 'https://' in url[0]:
                    all_url = url[0]
                else:
                    all_url = self.path.get('config', 'public_url') + url[0]
            else:
                all_url = self.url
            try:
                if 'request_type' in self.path.options('config') and self.path.get('config', 'request_type').strip() == 'form_data':
                    header['Content-Type'] = 'application/x-www-form-urlencoded'
                    request = urllib2.Request(all_url, urllib.urlencode(parm), headers=header)
                    respons = urllib2.urlopen(request, timeout=60).read()
                else:
                    request = urllib2.Request(all_url, data=parm, headers=header)
                    respons = urllib2.urlopen(request, timeout=60).read()
                    respons = all_jiemi(respons, self.path.get('sign_url', 'decode_url'))
            except Exception as e:
                respons = json.dumps({'error_detail': str(e)})

            print '接口返回信息'
            print respons
        config.set('config', 'req', json.dumps(parm))
        try:
            config.set('config', 'respons', respons)
        except:
            pass

        return {'respons': respons, 'url': all_url}

    def delete(self, data, config, *url):
        data = change_data_db(config, data).data
        json_change(copy.deepcopy(self.json_moban), json.loads(data))
        if 'sign_type' not in dict(self.path.items('sign')).keys() or config.get('sign', 'sign_type') == 'v1':
            head_data = dict(zip(config.get('config', 'head_key'), config.get('config', 'head_value')))
            parm = json.loads(data)
            parm['sign'] = buildMySign(parm, config.get('sign', 'secretKey'))
            if len(url) != 0:
                if 'http://' in url[0] or 'https://' in url[0]:
                    all_url = url[0]
                else:
                    all_url = self.path.get('config', 'public_url') + url[0]
            else:
                all_url = self.url
            try:
                respons = requests.delete(url=all_url, params=parm, headers=head_data, verify=False).text
            except Exception as e:
                respons = json.dumps({'error_detail': str(e)})

        if config.get('sign', 'sign_type') == 'v3':
            auth = CoinbaseExchangeAuth(config.get('sign', 'api_key'), config.get('sign', 'secretKey'), self.path.get('sign', 'password'))
            parm = json.loads(data)
            if len(url) != 0:
                if 'http://' in url[0] or 'https://' in url[0]:
                    all_url = url[0]
                else:
                    all_url = self.path.get('config', 'public_url') + url[0]
            else:
                all_url = self.url
            try:
                respons = requests.delete(url=all_url, json=parm, auth=auth).text
            except Exception as e:
                respons = json.dumps({'error_detail': str(e)})

        if config.get('sign', 'sign_type') == 'Backstage_web':
            parm = json.loads(data)
            if self.path.has_option('sign', 'login') and self.path.get('sign', 'login') == 'false':
                header = {}
            else:
                code = self.path.get('login', 'url').strip() + self.path.get('login', 'name').strip() + self.path.get('login', 'password').strip()
                hash.update(code)
                code = str(hash.hexdigest())
                header = json.loads([ self.path.get('login_value', i) for i in self.path.options('login_value') if code == i ][0])
            if len(url) != 0:
                if 'http://' in url[0] or 'https://' in url[0]:
                    all_url = url[0]
                else:
                    all_url = self.path.get('config', 'public_url') + url[0]
            else:
                all_url = self.url
            try:
                respons = requests.delete(url=all_url, json=parm, headers=header).text
            except Exception as e:
                respons = json.dumps({'error_detail': str(e)})

        if config.get('sign', 'sign_type') == 'web':
            parm = json.loads(data)
            if self.path.has_option('sign', 'login') and self.path.get('sign', 'login') == 'false':
                header = {}
            else:
                code = self.path.get('login', 'url').strip() + self.path.get('login', 'name').strip() + self.path.get('login', 'password').strip()
                hash.update(code)
                code = str(hash.hexdigest())
                header = json.loads([ self.path.get('login_value', i) for i in self.path.options('login_value') if code == i ][0])
            if len(url) != 0:
                if 'http://' in url[0] or 'https://' in url[0]:
                    all_url = url[0]
                else:
                    all_url = self.path.get('config', 'public_url') + url[0]
            else:
                all_url = self.url
            try:
                respons = requests.delete(url=all_url, json=parm, headers=header).text
            except Exception as e:
                respons = json.dumps({'error_detail': str(e)})

        if self.path.get('sign', 'sign_type') == 'app':
            parm = json.loads(data)
            header = json.loads(self.path.get('app_head', 'app_head'))
            header['Content-Type'] = 'application/json'
            if len(url) != 0:
                if 'http://' in url[0] or 'https://' in url[0]:
                    all_url = url[0]
                else:
                    all_url = self.path.get('config', 'public_url') + url[0]
            else:
                all_url = self.url
            try:
                request = urllib2.Request(all_url, data=urllib.urlencode(parm), headers=header)
                respons = urllib2.urlopen(request, timeout=60).read()
            except Exception as e:
                respons = json.dumps({'error_detail': str(e)})

        return {'respons': respons, 'url': all_url}

    def get(self, data, congig, *url):
        data = change_data_db(self.path, data).data
        json_change(copy.deepcopy(self.json_moban), json.loads(data))
        if 'sign_type' not in dict(self.path.items('sign')).keys() or self.path.get('sign', 'sign_type') == 'v1':
            parm = json.loads(data)
            if len(url) != 0:
                if 'http://' in url[0]:
                    all_url = url[0]
                else:
                    all_url = self.path.get('config', 'public_url') + url[0]
            else:
                all_url = self.url
            try:
                respons = requests.get(url=all_url, params=parm, headers=dict(zip(self.path.get('config', 'head_key'), self.path.get('config', 'head_value'))), verify=False).text
            except Exception as e:
                respons = json.dumps({'error_detail': str(e)})

        if self.path.get('sign', 'sign_type') == 'v3':
            auth = CoinbaseExchangeAuth(self.path.get('sign', 'api_key'), self.path.get('sign', 'secretKey'), self.path.get('sign', 'password'))
            parm = json.loads(data)
            if len(url) != 0:
                if 'http://' in url[0] or 'https://' in url[0]:
                    all_url = url[0]
                else:
                    all_url = self.path.get('config', 'public_url') + url[0]
            else:
                all_url = self.url
            try:
                if len(parm) == 0:
                    respons = requests.get(url=all_url, auth=auth).text
                else:
                    respons = requests.get(url=all_url, params=parm, auth=auth).text
            except Exception as e:
                respons = json.dumps({'error_detail': str(e)})

        if self.path.get('sign', 'sign_type') == 'web':
            if self.path.has_option('sign', 'login') and self.path.get('sign', 'login') == 'false':
                header = {}
            else:
                code = self.path.get('login', 'url').strip() + self.path.get('login', 'name').strip() + self.path.get('login', 'password').strip()
                hash.update(code)
                code = str(hash.hexdigest())
                header = json.loads([ self.path.get('login_value', i) for i in self.path.options('login_value') if code == i ][0])
            parm = json.loads(data)
            if len(url) != 0:
                if 'http://' in url[0] or 'https://' in url[0]:
                    all_url = url[0]
                else:
                    all_url = self.path.get('config', 'public_url') + url[0]
            else:
                all_url = self.url
            try:
                if len(parm) == 0:
                    respons = requests.get(url=all_url, headers=header).text
                else:
                    respons = requests.get(url=all_url, params=parm, headers=header).text
            except Exception as e:
                respons = json.dumps({'error_detail': str(e)})

        if self.path.get('sign', 'sign_type') == 'app':
            parm = json.loads(data)
            header = {}
            head_key = self.path.get('config', 'head_key').split(',')
            head_value = self.path.get('config', 'head_value').split(',')
            if len(head_key) == len(head_value):
                head = dict(zip(head_key, head_key))
                header['Content-Type'] = 'application/json'
            else:
                header_dict = {'Content-Type': 'application/json'}
            header['Content-Type'] = 'application/json'
            if 'head_data' in self.path.sections():
                for k, i in json.loads(self.path.get('head_data', 'head_data')).iteritmes():
                    header[k] = i

            if len(url) != 0:
                if 'http://' in url[0] or 'https://' in url[0]:
                    all_url = url[0]
                else:
                    all_url = self.path.get('config', 'public_url') + url[0]
            else:
                all_url = self.url
            try:
                request = requests.get(all_url, params=parm, headers=header, timeout=5)
                respons = request.text
            except Exception as e:
                respons = json.dumps({'error_detail': str(e)})

            print '接口返回信息 '
            print respons
        if self.path.get('sign', 'sign_type') == 'xiang_qian':
            parm = json.loads(data)
            header = {}
            head_key = self.path.get('config', 'head_key').split(',')
            head_value = self.path.get('config', 'head_value').split(',')
            if len(head_key) == len(head_value):
                head = dict(zip(head_key, head_key))
                header['Content-Type'] = 'application/json'
            else:
                header_dict = {'Content-Type': 'application/json'}
            header['Content-Type'] = 'application/json'
            if 'head_data' in self.path.sections():
                for k, i in json.loads(self.path.get('head_data', 'head_data')).iteritmes():
                    header[k] = i

            if len(url) != 0:
                if 'http://' in url[0] or 'https://' in url[0]:
                    all_url = url[0]
                else:
                    all_url = self.path.get('config', 'public_url') + url[0]
            else:
                all_url = self.url
            xiangqian_sign = AESCipher('Jy_ApP_0!9i+90&#')
            parm = {'aesRequest': xiangqian_sign.encrypt(json.dumps(parm))}
            try:
                request = requests.get(all_url, params=parm, headers=header, timeout=5)
                respons = xiangqian_sign.decrypt(json.loads(request.text)['aesResponse'])
            except Exception as e:
                respons = json.dumps({'error_detail': str(e)})

            print '接口返回信息 '
            print respons
        if self.path.get('sign', 'sign_type') == 'Backstage_web':
            parm = json.loads(data)
            header = json.loads(self.path.get('app_head', 'app_head'))
            header = {'Authorization': self.path.get('login', 'token'), 'Content-type': 'application/json'}
            if len(url) != 0:
                if 'http://' in url[0] or 'https://' in url[0]:
                    all_url = url[0]
                else:
                    all_url = self.path.get('config', 'public_url') + url[0]
            else:
                all_url = self.url
            try:
                request = requests.get(all_url, params=parm, headers=header, timeout=5)
                respons = request.text
            except Exception as e:
                respons = json.dumps({'error_detail': str(e)})

        if self.path.get('sign', 'sign_type') == 'zhixin':
            parm = json.loads(data)
            header = json.loads(self.path.get('app_head', 'app_head'))
            header = {'Authorization': self.path.get('login', 'token'), 'Content-type': 'application/json'}
            if len(url) != 0:
                if 'http://' in url[0] or 'https://' in url[0]:
                    all_url = url[0]
                else:
                    all_url = self.path.get('config', 'public_url') + url[0]
            else:
                all_url = self.url
            try:
                request = requests.get(all_url, params=parm, headers=header, timeout=5)
                respons = request.text
            except Exception as e:
                respons = json.dumps({'error_detail': str(e)})

        if self.path.get('sign', 'sign_type') == 'hkci':
            parm = json.loads(data)
            header = json.loads(self.path.get('login', 'huasheng_headertoken'))
            header = {'Authorization': self.path.get('login', 'token'), 'Content-type': 'application/json'}
            if len(url) != 0:
                if 'http://' in url[0] or 'https://' in url[0]:
                    all_url = url[0]
                else:
                    all_url = self.path.get('config', 'public_url') + url[0]
            else:
                all_url = self.url
            try:
                request = requests.get(all_url, params=parm, headers=header, timeout=5)
                respons = request.text
            except Exception as e:
                respons = json.dumps({'error_detail': str(e)})

        if self.path.get('sign', 'sign_type') == 'haofang_server':
            parm = json.loads(data)
            header = json.loads(self.path.get('login', 'haofang_headertoken'))
            if len(url) != 0:
                if 'http://' in url[0] or 'https://' in url[0]:
                    all_url = url[0]
                else:
                    all_url = self.path.get('config', 'public_url') + url[0]
            else:
                all_url = self.url
            try:
                request = requests.get(all_url, params=parm, headers=header, timeout=5)
                respons = request.text
            except Exception as e:
                respons = json.dumps({'error_detail': str(e)})

        return {'respons': respons, 'url': all_url}