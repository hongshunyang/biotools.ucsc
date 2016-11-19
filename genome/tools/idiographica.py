#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Copyright (C) yanghongshun@gmail.com
#
##./app.py -c ../data/11182016-1/ -o 20 -f 1 -e 3 -t 2500
##cp -r ../result/11182016-1 11182016-1-idio
##./idiographica.py -i ../data/11182016-1-idio/ -c 0,9,10 -b 0 -r 9 -n 0

import os,sys,configparser,getopt
import csv,shutil


# get custom columns data from data files 

APP_TOOLS_DIRNAME = 'tools'
APP_TOOLS_DATA_DIRNAME = '_data'
APP_TOOLS_RESULT_DIRNAME = '_result'
APP_DATA_DIRNAME = 'data'
APP_RESULT_DIRNAME = 'result'

def usage():
    print('-i:single file or directory')
    print('-c:roi data columns')
    print('-b:observe column,cluster name column')
    print('-r:region column,generates left and right column base this column')
    print('-n:no repeat column,get only one clustername from one group cluster')
    print('get roi data from single file or directory')
    print('./idio.py -i ../result/11182016-1.1/ -c 0,9,10 -b 0 -r 9 -n 0')

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
        
        res_cols = [x for x in res_cols if x < inputFileColIndexMax]
        print("check valid column index")
        print(res_cols)
        colDataSet=[]      
        repeatColumnData=[]

        i = 0

        for cl in inputFileDataSetOrig:
            row = []

            ## only need one cluster row from one cluster group
            if cl[norepeat_column] in repeatColumnData:
                continue

            for idx in range(len(cl)):
                if idx in res_cols:
                    if i==0:
                        row.append(cl[idx])
                    else:
                    #chromsome 1->chr1
                        if chr_column !=-1:
                            chr_str = cl[chr_column]
                            if not chr_str.startswith('chr'):
                                cl[chr_column]='chr'+str(cl[chr_column]).upper()
                    # observe column not ''
                        if observe_column !=-1:
                            if cl[observe_column]!='':###observe column not empty
                                row.append(cl[idx])
                                repeatColumnData.append(cl[norepeat_column])
            
            i+=1
            if (row != []):
                colDataSet.append(row)
    
    return colDataSet
    # saveDataToCSV([],colDataSet,resultFilePath)	

def genIdiographicaData(roiDataSet,datafileabspath):

    #roiDataSet

    #clustername chromsome region(left)


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

    for j in range(len(roiDataSet)):
        if j==0:
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
        opts,args = getopt.getopt(sys.argv[1:],"hi:c:b:r:n:",["--input=","--columns=","--observe-column=","--chr-column=","--norepeat-column="])
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


    if input_data != '':
        genObjDataFromFile(input_data,idioConfigs)
        #重命名文件
        #添加title
    else:
        sys.exit()


if __name__ == "__main__":
	main()





    
