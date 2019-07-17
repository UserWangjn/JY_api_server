# -*- coding: utf-8 -*-
__author__ = 'SUNZHEN519'
import sys
import urllib
import urllib2
import json
sys.path.append("../../")
class request_flask(object):
    #第一个参数为接口名字
    #第二个参数为字典，字典value为接口返回数据，key为jo.in字符串链接的第一个为result，第二个为id，第三个为comment
    #第三个参数为运行开始时间
    def __init__(self,name,data,time,id_id,server_ip,path,run_id ,git_base_name):
        self.name=name
        self.data=data
        self.server_ip=server_ip
        ua_headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0"
        }
        urllib.urlencode({'path':path,'jeikou_name': name.encode('utf-8'), 'result': data.encode('utf-8'), "time": str(time).encode('utf-8'), "ip": id_id.encode('utf-8'),'git_base_name':git_base_name})
        # url='http://'+server_ip+':5025/piliang_run_result'
        # test_data = urllib.urlencode({'jeikou_name':name.encode('utf-8'),'result':data.encode('utf-8'),"time":str(time).encode('utf-8'),"ip":id_id.encode('utf-8'),'path':'server'})
        # req = urllib2.Request(url=url, data=test_data,headers=ua_headers)
        # res_data=urllib2.urlopen(req).read()
        url='http://'+id_id+':5025/piliang_git_result'
        test_data = urllib.urlencode({'jeikou_name':name.encode('utf-8'),'result':data.encode('utf-8'),"time":str(time).encode('utf-8'),"id":server_ip.encode('utf-8'),'path':'server','path_mulu':path,'run_id':run_id,'git_base_name':git_base_name})
        req = urllib2.Request(url=url, data=test_data,headers=ua_headers)
        res_data=urllib2.urlopen(req).read()
        try:
           res_data = json.loads(res_data)
        except:
            res_data={"res_data":res_data}
