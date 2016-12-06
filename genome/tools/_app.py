#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Copyright (C) yanghongshun@gmail.com
#
import os,sys,configparser,getopt
import csv



# 1、对单个文件按主列(gene_name (mus_musculus_ensembl_v80_Genes))对行进行分组
# 2、对单个文件分组后的每一组按找从列(Frequency)求和
# note:
# 分组的原则根据主列中每一行的名字，进行归类，同名归属一组
# 3、支持文件批量求和，从整体上看，对位于不同文件的主列进行分组，原则同上。也就是跨文件分组。
# 4、支持合并后的分组进行求和

#http://stackoverflow.com/questions/2387697/best-way-to-convert-csv-data-to-dict
#http://www.tbk.ren/article/168.html?from=similar

def usage():
    print('...')

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

def setSumResultPath(groupColumn,followColumn):
    print("setting sum result path")
    result_tmp_dirstr = os.path.dirname(os.path.abspath(sys.argv[0]))	
    
    result_filename = 'g'+groupColumn+'_'+'f'+followColumn+'_'+'sum'	
    result_filename +='.csv'
    
    sumResultPath = os.path.join(result_tmp_dirstr,APP_TOOLS_RESULT_DIRNAME,result_filename)
    
    print("sum result path is:%s" % sumResultPath )
    print("set end")

    return sumResultPath


def sumByGroup(sumParams):
    print("start acting")

    input_path=sumParams['input_path']
    groupColumnIndex=sumParams['group_column']
    followColumnIndex=sumParams['follow_column']

    csvDictData={}
  
    if os.path.isdir(input_path):
        print("result file is a directory:%s" % input_path)
        for root,dirs,files in os.walk(os.path.abspath( input_path)):
            for file in files:
                filename,fileext=os.path.splitext(file)
                if fileext=='.csv':
                    singleFileData = []
                    resultfileabspath = root+os.sep+file					
                    ##
                    print(resultfileabspath)
                    
    elif os.path.isfile(input_path):
        print("input file is a single file:%s" % input_path)
        resultfileabspath = os.path.abspath(input_path)
        singleFileData = []
        ## 
        print(resultfileabspath)



def main():
    try:
        opts,args = getopt.getopt(sys.argv[1:],"hi:g:f:",["--help=","--input=","--group=","--follow="])
    except getopt.GetoptError as err:
        print(err) 
        usage()
        sys.exit(2)

    sumParams = {
        'input_path':'',
        'group_column':'',
        'follow_column':''
    }



    for opt,arg in opts:
        if opt in ('-h',"--help"):
            usage()
            sys.exit()
        elif opt in ('-i','--input'):
            sumParams['input_path']=arg
        elif opt in ('-g','--group'):
            sumParams['group_column']=arg
        elif opt in ('-f','--follow'):
            sumParams['follow_column']=arg
    

       
    if sumParams['input_path'] != '':
        sumByGroup(sumParams)
    else:
        sys.exit()


if __name__ == "__main__":
    main()
