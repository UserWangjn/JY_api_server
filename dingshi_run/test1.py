#-*-coding:utf-8-*-
__author__ = 'SUNZHEN519'
import requests
import json
data={}
data["serviceName"]="PERSONAL_REGISTER_EXPAND"
data["platformNo"]="5000001104"
data["responseType"]="CALLBACK"
data["keySerial"]="1"
data["respData"]={"platformUserNo":"HFJYJFCR190507000000162","realName":"孙振","idCardType":"PRC_ID","userRole":"INVESTOR","idCardNo":"372928198510260038","mobile":"19992131026","bankcardNo":"6222600260001072444","bankcode":"COMM","accessType":"FULL_CHECKED","auditStatus":"PASSED","groupAccountNO":"","requestNo":"19050713405053234100","code":"0","status":"SUCCESS"}
data["userDevice"]="MOBILE"
data["sign"]="N5N0I+t6p/HyETQNLTyfyJY5D2VpdIUFKaoLPiojAAti/1PxkcnIWa/ybGpb69m7u9nb65jik5wgK4Kh7I6XSjSFdyIGxFO74H8bSCKmE60vnf2pEL/GDcEjbosBwDqdfdDvbIaK7Ekcn6Q0//rymVMKMDHAwt6TkuObKTig4RMnfEmDzHdmqxLJkpq0dhbfE3BMdYYYJCPr+U3qHdp1+za+HWaS/omBV6C+0IPWL1AKTa6ZrFPvBZDSWhXgyfwl+vTpthMHyiHMJJi6oCrKyjddStjmbpjSOlg/2HuaSEEaE0nJbkfaltzqou+po5W8JG1Z6kAG2vlhW0o+/KvyGw=="
data["showBankInfoError"]="true"
url="http://115.182.212.71:8783/core-web-pub/hfFundDeposit/bindCard/confirm"
url_sing='http://192.168.32.65:8080/xqAppServer/api/APPBizRest/sign/v1/'
headers={"Content-Type": "application/json"}
k=requests.post(url_sing,data=json.dumps(data["respData"]),headers=headers)
print json.loads(k.text)['responseBody']['sign']
data["sign"]=k
s=requests.post(url,data=data)
print s.text