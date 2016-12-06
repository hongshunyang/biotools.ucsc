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



