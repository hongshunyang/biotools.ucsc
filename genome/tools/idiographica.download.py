#!/usr/bin/env python2
# -*- coding:utf-8 -*-
# Copyright (C) yanghongshun@gmail.com
#download
#./idiographica.download.py -g gmail.download.ini -r _result/idiographica_rename.csv -p _result/idiographica_post.csv


import os,sys,ConfigParser,getopt
import csv

import shutil

import requests
import lxml.html
import re
from datetime import datetime, date, time

from gmail import Gmail

import wget

APP_TOOLS_DIRNAME = 'tools'
APP_TOOLS_DATA_DIRNAME = '_data'
APP_TOOLS_RESULT_DIRNAME = '_result'
APP_DATA_DIRNAME = 'data'
APP_RESULT_DIRNAME = 'result'
APP_TOOLS_IDIO_DIRNAME = 'idiographica'



def usage():
    print 'idiographic download from gmail'
    print '-g,gmail account settings'
    print '-r,idiographica_rename.csv'
    print '-p,idiographica_post.csv'
    print 'example:'
    print './idiographica.download.py -g gmail.download.ini -r _result/idiographica_rename.csv -p _result/idiographica_post.csv'

def getDataFromCSV(title,spliter,filePath):
	data = []
	if not os.path.isfile(filePath):
		print " file not exist!"
		sys.exit()
	
	csvfile=csv.reader(open(filePath, 'r'),delimiter=spliter)
	
	for line in csvfile:
		data.append(line)
	if title == True:
		del data[0]
	print "reading end"
	
	return data


def readSetting(option,section,filePath):
	
	conf = ConfigParser.ConfigParser() 
	conf.read(filePath)
	
	option = option.lower()

	
	if os.path.isfile(filePath):
		##print section+":"+option + " read value from " +filePath
		pass
	else :
		print filePath+" not exist"
		sys.exit()
	
	if section not in conf.sections():
		print section + " not exist"
		sys.exit()
	else :
		if option not in conf.options(section):
			print option + " not exist"
			sys.exit()
		else:
			val = conf.get(section,option)
			if val != '':
				return val
			else :
				print section + ':' +option +'is null'
				sys.exit()
	


def download(settings):
    #login gmail
    username = readSetting('username','Gmail',settings['gmail_download'])
    password = readSetting('password','Gmail',settings['gmail_download'])
   
    
    sender  = readSetting('sender','Gmail',settings['gmail_download'])

    g=Gmail()
    g.login(username,password)
    if g.logged_in:
        print 'login successfully'

    messages = g.inbox().mail(sender=sender)###after


    rename_list = getDataFromCSV(False,'\t',settings['rename_list'])
    post_task= getDataFromCSV(False,'\t',settings['post_task'])


    ##key:idio file name  value:row
    renameListDict={}
    for item in rename_list:
        renameListDict[item[0]]=item

    ##key:idio file name value:row
    postTaskDict ={}
    for item in post_task:
        postTaskDict[item[2]]=item

    for email in messages:
        email.read()
        email.fetch()
        content = email.body
        email.delete()
        download_url = re.search("(?P<url>https?://[^\s]+)", content).group("url")
        download_url = download_url.replace(' ','')
        filename = wget.download(download_url)
        print filename
        for t in post_task:
            if filename.lower().endswith((t[0]+'.pdf').lower()):##task id
                #print 'idio name:'+t[2]  ##file path
                #print 'real name:'+renameListDict[t[2]][1]
                dstfile=renameListDict[t[2]][1]+'.pdf'
                shutil.move(filename,dstfile)
                break

    g.logout()


def main(argv):

    settings = {
        'gmail_download':"",
        'post_task':"",
        'rename_list':""
    }

    try:
        opts, args = getopt.getopt(argv,"hp:g:r:",["post-task=","gmail-download=","rename-list="])
    except getopt.GetoptError:
	print '请使用 -h 选项查看帮助'
        usage()
	sys.exit()
    for opt, arg in opts:
        if opt in ('-h'):
            usage()
            sys.exit()
        elif opt in ('-p','--post-task'):
            settings['post_task'] = arg
        elif opt in ("-g",'--gmail-download'):
            settings['gmail_download'] = arg
        elif opt in ("-r","--rename-list"):
            settings['rename_list']=arg

    download(settings)        
		
if __name__=='__main__':
    if len(sys.argv) <=1:
        print "please use option -h"
    else :
	main(sys.argv[1:])

