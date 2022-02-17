# -*- coding: cp1250 -*-

import glob
import os

from tkFileDialog import askopenfilename,asksaveasfilename,askdirectory
import time

import pprint, pickle
import numpy as n
import csv,scipy,math
from time import strftime, localtime
from tkFileDialog import askopenfilename,asksaveasfilename,askdirectory
import time
import pickle
import datetime,random
from scipy import special,stats
from numpy.random import randn

from scipy import *
import glob
import os
import string
import sys
import globs
from easygui import *

import tkMessageBox
import math
from string import upper as uppercase
from tkFileDialog import askopenfilename as askfn

def get_info(f_name):
	
	x_file=open(f_name)
	read_data=[]
	start_flag=0
	for line in csv.reader(x_file,delimiter=","):
		
		if start_flag==0:
			header=line
			start_flag=1
		else:
			read_data.append(line)
	print header
	return ([header,read_data])
def get_record(database_info,id_0,id_1):
	id_0_index=database_info[0].index("ID_0:")
	id_1_index=database_info[0].index("ID_1:")
	out_line=None
	for line in database_info[1]:
		#print id_0,id_1
		#print line
		if (line[id_0_index]==id_0)&(line[id_1_index]==id_1):
			out_line=line
	return ([database_info[0],out_line])