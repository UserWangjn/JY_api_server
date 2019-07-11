# -*-coding:utf-8-*-
import smtplib

server = smtplib.SMTP_SSL("smtp.jieyuechina.com",port=25)

server.login('test@jieyuechina.com','Test.1234*')


server.sendmail('test@jieyuechina.com','test@jieyuechina.com','22222')
server.close()