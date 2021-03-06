#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Copyright (C) yanghongshun@gmail.com

## http://rtools.cbrc.jp/idiographica/ Version 2.2 (Updated July, 2013) 
## 一、存在观察列，且观察列中数据重复仅取其一，最先遇到就取第一行
## cluster->idiographica
# 生成cluster
##./app.py -c ../data/11182016-1/ -o 20 -f 1 -e 3 -t 2500
## 准备数据
##cp -r ../result/11182016-1 ../data/11182016-1-idio
## 生成map文件
##./idiographica.py -i ../data/11182016-1-idio/ -c 0,9,10 -b 0 -r 9 -n 0 -o gen
## 变更文件名,把文件名作为title添加至map文件,生成对照文件名列表
## ./idiographica.py -i ../result/11182016-1-idio/ -o rename
## 批量提交文件
## ./idiographica.py -i _result/idiographica/11182016-1-idio/ -o post -f gmail.download.ini
## 检查gmail,获取文件下载地址并下载
## ./idiographica.download.py -g gmail.download.ini -r _result/idiographica_rename.csv -p _result/idiographica_post.csv

## 
## 二、不存在观察列,直接取其中若干列，所有行，直接绘图
## 不含cluster的情况->idiographica
##文件格式转换，初步获取感兴趣数据
## excel2csv:xlsx->csv
#./app.py -i ../data/11222016-1-excel2csv -c 8,9 s '' -d ','
## 准备数据
# cp -R ../result/11222016-1-excel2csv/ ../../biotools.ucsc/genome/data/
# 生成map文件(此处没有观察列，有观察列的一把主要考虑观察列不能重复见上述cluster)
# ./idiographica.py -i ../data/11222016-1-excel2csv/ -c 0,1 -r 0 -o gen
## 变更文件名,把文件名作为title添加至map文件,生成对照文件名列表
## ./idiographica.py -i ../result/111222016-1-excel2csv/ -o rename
## 批量提交文件
## ./idiographica.py -i _result/idiographica/11222016-1-excel2csv/ -o post -f gmail.download.ini
## 检查gmail,获取文件下载地址并下载
## ./idiographica.download.py -g gmail.download.ini -r _result/idiographica_rename.csv -p _result/idiographica_post.csv




import os,sys,configparser,getopt
import csv,shutil

import requests
from requests_toolbelt import MultipartEncoder
import lxml.html
import re
from time import sleep
from datetime import datetime, date, time

# get custom columns data from data files 

APP_TOOLS_DIRNAME = 'tools'
APP_TOOLS_DATA_DIRNAME = '_data'
APP_TOOLS_RESULT_DIRNAME = '_result'
APP_DATA_DIRNAME = 'data'
APP_RESULT_DIRNAME = 'result'
APP_TOOLS_IDIO_DIRNAME = 'idiographica'


def usage():
    print('-i:single file or directory')
    print('-c:roi data columns')
    print('-b:observe column,cluster name column')
    print('-r:region column,generates left and right column base this column')
    print('-n:no repeat column,get only one clustername from one group cluster')
    print('-o:operator:gen,rename,post,gmail')
    print('get roi data from single file or directory')
    print('./idiographica.py -i ../data/11182016-1.1/ -c 0,9,10 -b 0 -r 9 -n 0 -o gen')
    print('chanage original file to idiographica map file')
    print('./idiographica.py -i ../result/11182016-1-idio/ -o rename ')
    print('batch post data to remote idiographic ')
    print('./idiographica.py -i _result/idiographica/11182016-1-idio/ -o post -f gmail.download.ini')
    print('download pdf from gmail')
    print('./idiographica.download.py -g gmail.download.ini -r _result/idiographica_rename.csv -p _result/idiographica_post.csv')




def readSetting(option,section,filePath):
        
    conf = configparser.ConfigParser() 
    conf.read(filePath)
    option = option.lower()
    if os.path.isfile(filePath):
        ##print section+":"+option + " read value from " +filePath
        pass
    else:
        print("%s not exist" % filePath)
        sys.exit()
    
    if section not in conf.sections():
        print(" %s not exist" % section)
        sys.exit()
    else:
        if option not in conf.options(section):
            print(" %s not exist" % option)
            sys.exit()
        else:
            val = conf.get(section,option)
            if val != '':
                return val
            else:
                print('%s : %s is null' % (section,option))
                sys.exit()

def getDataFromCSV(title,spliter,filePath):
        print("reading data from csv file:%s" % filePath)
        data = []
        if not os.path.isfile(filePath):
                print("%s not exist!" % filePath)
                sys.exit()
        
        csvfile=csv.reader(open(filePath, 'r'),delimiter=spliter)
        
        for line in csvfile:
                data.append(line)
        if title == True:
                print("delete first row:title row")
                del data[0]
        print("reading end")
        
        return data


def saveDataToCSV(title,data,filePath,fmt=''):
        print("saving data to csv file:%s" % filePath)
        
        if os.path.isfile(filePath):
                print("delete old csv file:%s" % filePath)
                os.remove(filePath)
        
        file_handle = open(filePath,'w')
        
        if fmt=='':
                csv_writer = csv.writer(file_handle,delimiter=' ')
        else:
                csv_writer = csv.writer(file_handle,delimiter=fmt)
        
        if len(title) >0 :
                csv_writer.writerow(title)
        
        csv_writer.writerows(data)
        
        file_handle.close()
        
        print("saved end")

def generateResultFilePath(dataFilePath,prefix=''):
        
        print("generating result file path from data file path:%s" % dataFilePath)
        filename,fileext=os.path.splitext(os.path.basename(dataFilePath))
        
        if prefix=='':
                resultFileName = 'result_'+filename+'.csv'
        else:
                resultFileName = 'result'+prefix+filename+'.csv'


        dataFileAbsPath = os.path.abspath(dataFilePath)
        
        app_root_dir = os.path.dirname(os.path.dirname(os.path.abspath(sys.argv[0])))   
        app_data_dir = app_root_dir + os.sep + APP_DATA_DIRNAME+os.sep
        app_result_dir = app_root_dir + os.sep + APP_RESULT_DIRNAME+os.sep
        
        result_tmp_dirstr = os.path.dirname(dataFileAbsPath).replace(app_data_dir,'')
        
        resultFileDir = os.path.join(app_result_dir,result_tmp_dirstr)

        if not os.path.exists(resultFileDir):
                print("create directory:%s " % resultFileDir)
                os.makedirs(resultFileDir)
        
        resultFilePath = os.path.join(resultFileDir,resultFileName)
        print("result file path is:%s" % resultFilePath)
        print("generated end")
        return resultFilePath


def postObjDataFile(dataFilePath,formSetting):
    _postObjDataFile(dataFilePath,formSetting)

def _postObjDataFile(dataFilePath,formSetting):

    url = readSetting('getUrl','Idiographica',formSetting)

    # url = 'http://rtools.cbrc.jp/idiographica/'

    r=requests.get(url)
    form_page = lxml.html.fromstring(r.text)
    form = form_page.forms[0]
    
    post_url = url+form.action 

    fields = form.fields.keys()
    
    formData = {}

    for field_name in fields:
        formData[field_name]=form.fields[field_name]


    #set default Value
    formData['species']=readSetting('species','Idiographica',formSetting)

    formData['format']=readSetting('format','Idiographica',formSetting)

    formData['orientation']=readSetting('orientation','Idiographica',formSetting)

    formData['size']=readSetting('size','Idiographica',formSetting)

    #formData['mail_to']='yanghongshun@gmail.com'
    formData['mail_to']=readSetting('mail_to','Idiographica',formSetting)

    ## if something is wrong,please 
    ## uncomment below ,check form fields is equal the fields in formSetting file
    # for k,v in formData.items():
        # print('%s=%s' % (k,v))

    # sys.exit()
        

    result_filename = 'idiographica_post.csv'
    result_tmp_dirstr = os.path.dirname(os.path.abspath(sys.argv[0]))
    postResultPath = os.path.join(result_tmp_dirstr,APP_TOOLS_RESULT_DIRNAME,result_filename)
   

    postDataSet = []

    if os.path.isdir(dataFilePath):
        print("  data file is a directory:%s" % dataFilePath)
        for root,dirs,files in os.walk(os.path.abspath(dataFilePath)):
            for fl in files:
                filename,fileext=os.path.splitext(fl)
                if fileext=='.csv':
                    datafileabspath = os.path.join(root,fl)
                    formData['description']=('filename',open(datafileabspath,'rb'),'text/plain')
                    postData = MultipartEncoder(fields=formData)
                    header={'Content-Type': postData.content_type}
                    print('posting...')
                    rp=requests.post(post_url,data=postData,headers=header)
                    if rp.status_code == 200:
                        print('posted successfully')
                        # print(rp.text)
                        responseHtml=lxml.html.fromstring(rp.text)
                        responseHtmlContent = responseHtml.text_content()
                        print(responseHtmlContent)
                        pat=re.compile(r"\((.*?)\)", re.I|re.X)
                        taskList=[]
                        taskList = pat.findall(responseHtmlContent)
                        taskList=list(map(lambda x:x.replace(' ',''),taskList)) 
                        # print(taskList)
                        taskList.append(datetime.now().strftime('%m-%d-%Y %H:%m:%S'))
                        taskList.append(datafileabspath)
                        postDataSet.append(taskList)
                        sleep(3)

        if postDataSet !=[]:
            saveDataToCSV([],postDataSet,postResultPath,'\t')


def renameObjDataFile(dataFilePath):
    _renameObjDataFile(dataFilePath)

def _renameObjDataFile(dataFilePath):

    app_root_dir = os.path.dirname(os.path.dirname(os.path.abspath(sys.argv[0])))
    app_result_dir = os.path.join(app_root_dir, APP_RESULT_DIRNAME)
    
    result_filename = 'idiographica_rename.csv'
    result_tmp_dirstr = os.path.dirname(os.path.abspath(sys.argv[0]))
    result_idio_dir = os.path.join(result_tmp_dirstr,APP_TOOLS_RESULT_DIRNAME,APP_TOOLS_IDIO_DIRNAME)
    renameResultPath = os.path.join(result_tmp_dirstr,APP_TOOLS_RESULT_DIRNAME,result_filename)
    
    # if not os.path.exists(result_idio_dir):
        # print("create directory:%s " % result_idio_dir)
        # os.makedirs(result_idio_dir)

    print("acting input   data file")
    if os.path.isdir(dataFilePath):
        print("  data file is a directory:%s" % dataFilePath)
        i=0
        d2tSets=[]
        for root,dirs,files in os.walk(os.path.abspath(dataFilePath)):
            for fl in files:
                filename,fileext=os.path.splitext(fl)
                if fileext=='.csv':
                    datafileabspath = os.path.join(root,fl)
                    idio_filepath = datafileabspath.replace(app_result_dir,result_idio_dir).replace(filename,str(i))
                    ###read,add title,write
                    #read
                    mapDataSet = getDataFromCSV(False,'\t',datafileabspath)
                    ##title
                    titleSet = ['title',24,'blue',str(i)]
                    mapDataSet.insert(0,titleSet)
                    idio_filepath_dir = os.path.dirname(idio_filepath)
                    if not os.path.exists(idio_filepath_dir):
                        print('creating directory %s' % idio_filepath_dir)
                        os.makedirs(idio_filepath_dir)
                    ##add title save file
                    saveDataToCSV([],mapDataSet,idio_filepath,'\t')
                    ##local file list
                    d2tSets.append([idio_filepath,datafileabspath])
                    i+=1

    saveDataToCSV([],d2tSets,renameResultPath,'\t')
    

    print("action is end")


def genObjDataFromFile(dataFilePath,idioConfigs):
        _genObjDataFromFile(dataFilePath,idioConfigs)

def _genObjDataFromFile(dataFilePath,idioConfigs):
    print("acting input   data file")
    if os.path.isdir(dataFilePath):
        print("  data file is a directory:%s" % dataFilePath)
        for root,dirs,files in os.walk(os.path.abspath(dataFilePath)):
            for fl in files:
                filename,fileext=os.path.splitext(fl)
                if fileext=='.csv':
                    datafileabspath = root+os.sep+fl
                    roiDataSet = _getROIDataFromSingleFile(datafileabspath,idioConfigs)
                    genIdiographicaData(roiDataSet,datafileabspath)
    elif os.path.isfile(dataFilePath):
        print("  data file is a single file:%s" % dataFilePath)
        datafileabspath = os.path.abspath(dataFilePath)
        roiDataSet = _getROIDataFromSingleFile(datafileabspath,idioConfigs)
        genIdiographicaData(roiDataSet,datafileabspath)
    print("action is end")

def _getROIDataFromSingleFile(datafileabspath,idioConfigs):
    print("data file :%s" % datafileabspath)
    if not os.path.isfile(datafileabspath):
        print("data file :%s is not exist!" % datafileabspath)
        sys.exit()

    res_cols = idioConfigs['res_cols']
    chr_column = idioConfigs['chr_column']
    observe_column = idioConfigs['observe_column']
    norepeat_column = idioConfigs['norepeat_column']

    # resultFilePath = generateResultFilePath(datafileabspath)
    # if os.path.isfile(resultFilePath):
        # print("delete old  result file :%s" % resultFilePath)
        # os.remove(resultFilePath)

    print("loading file")
    # print(datafileabspath)
    i=0
    filename,fileext=os.path.splitext(datafileabspath)
    if fileext=='.csv':
        inputFileDataSetOrig = getDataFromCSV(False,',',datafileabspath)
        inputFileDataSetOrigTitleRow = inputFileDataSetOrig[0]
        for col in inputFileDataSetOrigTitleRow:
            print(i,col)        
            i+=1            
        inputFileColIndexMax = len(inputFileDataSetOrigTitleRow)-1
       
        # <= must consider the last columnu
        res_cols = [x for x in res_cols if x <= inputFileColIndexMax]
        print("check valid column index")
        print(res_cols)
        colDataSet=[]      
        repeatColumnData=[]

        i = 0

        for cl in inputFileDataSetOrig:
            row = []

            ## only need one cluster row from one cluster group
            if norepeat_column != -1:
                if cl[norepeat_column] in repeatColumnData:
                    continue

            for idx in range(len(cl)):
                if idx in res_cols:
                    ## title
                    if i==0:
                        row.append(cl[idx])
                    else:
                    #chromsome 1->chr1
                        if chr_column !=-1:
                            chr_str = cl[chr_column]
                            if not chr_str.startswith('chr'):
                                cl[chr_column]='chr'+str(cl[chr_column]).upper()
                    # observe column 是否需要观察列 
                        if observe_column !=-1:
                            if cl[observe_column]!='':###observe column not empty
                                row.append(cl[idx])
                                repeatColumnData.append(cl[norepeat_column])
                        else:
                            row.append(cl[idx])
            i+=1
            print(row)
            if (row != []):
                colDataSet.append(row)
  
    # print(colDataSet)
    return colDataSet
    # saveDataToCSV([],colDataSet,resultFilePath)       

def genIdiographicaData(roiDataSet,datafileabspath):

    #roiDataSet

    #clustername(optional) chromsome region(left)


    resultFilePath = generateResultFilePath(datafileabspath)
    if os.path.isfile(resultFilePath):
        print("delete old  result file :%s" % resultFilePath)
        os.remove(resultFilePath)

    objDataSet=[]

    #idiographica data template
    #http://rtools.cbrc.jp/idiographica/format.html

    titleRow=[] #[title ...]
    legendRows=[] #[[legend ...],[legend ...]]


    chr_column = -1
    region_column = -1
    cluster_column = -1


    for i in range(len(roiDataSet[0])):
        
        if roiDataSet[0][i].lower() == 'clustername':
            cluster_column = i
            print('cluster column:%s' % cluster_column)
        if roiDataSet[0][i].lower() == 'chromosome':
            chr_column = i
            print('chromosome column:%s' % chr_column)
        if roiDataSet[0][i].lower() == 'region':
            region_column = i
            print('region column:%s' % region_column)
    

    mmXY = list(range(1,20,1))
    mmXY.extend(['X','Y'])
    
    chrSet = list(map(lambda x:'chr'+str(x),mmXY))
    # print(roiDataSet)
    # sys.exit()
    for j in range(len(roiDataSet)):
        if j==0:##title
            continue

        if roiDataSet[j][chr_column] not in chrSet:
            print('-'*100)
            print(roiDataSet[j][chr_column])
            continue
        row = []
        ##row.append(roiDataSet[j][cluster_column])
        row.append('mapping')
        row.append(7)
        row.append('red')
        row.append('.')
        row.append('.')
        row.append(roiDataSet[j][chr_column])
        row.append(roiDataSet[j][region_column])
        row.append(int(roiDataSet[j][region_column])+1)
        row.append('.')
        objDataSet.append(row)

    saveDataToCSV([],objDataSet,resultFilePath,'\t')

def main():
    try:
        opts,args = getopt.getopt(sys.argv[1:],"hi:c:b:r:n:o:f:",["--input=","--columns=","--observe-column=","--chr-column=","--norepeat-column=",'--operator=','--form-setting='])
    except getopt.GetoptError as err:
        print(err) 
        usage()
        sys.exit(2)

    input_data=""       
    

    idioConfigs = {
            'res_cols':'',
            'observe_column':-1,
            'chr_column':-1,
            'norepeat_column':-1
    }

    operator = ""

    form_setting = ""


    for opt,arg in opts:
        if opt in ('-h',"--help"):
            usage()
            sys.exit()
        elif opt in ('-i','--input'):
            input_data=arg
        elif opt in ('-c','--columns'):
            idioConfigs['res_cols'] = arg.replace(',','|').replace(' ','|').split('|')
            # delete null
            idioConfigs['res_cols'] = [x for x in idioConfigs['res_cols'] if x !=''] 
            # delete duplicates
            idioConfigs['res_cols'] = [int(idioConfigs['res_cols'][i]) for i in range(len(idioConfigs['res_cols'])) if i == idioConfigs['res_cols'].index(idioConfigs['res_cols'][i])]
        elif opt in ('-b','--observe-column'):
            idioConfigs['observe_column'] = int(arg)
        elif opt in ('-r','--chr-column'):            
            idioConfigs['chr_column'] = int(arg)
        elif opt in ('-n','--norepeat-column'):
            idioConfigs['norepeat_column'] = int(arg)
        elif opt in ('-o','--operator'):
            operator = arg
        elif opt in ('-f','--form-setting'):
            form_setting = arg




    if input_data != '':
        if operator == 'gen':
            genObjDataFromFile(input_data,idioConfigs)
        elif operator == 'rename':##重命名文件，添加title
            renameObjDataFile(input_data)
        elif operator == 'post':##批量提交
            ##check post data is from _result
            tmp_dirstr = os.path.dirname(os.path.abspath(sys.argv[0]))
            idio_dir = os.path.join(tmp_dirstr,APP_TOOLS_RESULT_DIRNAME,APP_TOOLS_IDIO_DIRNAME)
            if not os.path.abspath(input_data).startswith(idio_dir):
                print('*'*100)
                print('Are you kidding me! The post data is not renamed!!')
                print('*'*100)
                sys.exit()
            else:
                postObjDataFile(input_data,form_setting)
    else:
        sys.exit()


if __name__ == "__main__":
        main()

