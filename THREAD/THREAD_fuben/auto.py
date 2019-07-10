# -*-coding:utf-8-*-
import smtplib

server = smtplib.SMTP_SSL("smtp.exmail.qq.com",port=465)

server.login('zhen.sun@okcoin.com','gfXD8b7ojmhWbD9u')


server.sendmail('zhen.sun@okcoin.com','zhen.sun@okcoin.com','22222')
server.close()