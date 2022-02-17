# -*- coding: cp1250 -*-
import numpy,scipy,os
import Tkinter as tk
import csv
from scipy.special import j1
from scipy.optimize import fminbound
from scipy import *
import pygame, sys,os
from pygame.locals import *
import pygame.display
import pygame.gfxdraw
from scipy.ndimage.fourier import fourier_ellipsoid
from sys import argv
import time
import pickle
import threading
import globs
import glob
import pygame.font
import pygame.surface
from easygui import multenterbox as multenterbox
from easygui import ccbox as ccbox
from easygui import integerbox as integerbox
from tkFileDialog import askopenfilename as askfn
import Tkinter as tk
import tkMessageBox
from PIL import Image
from PIL import ImageTk
from PIL import ImageDraw
from PIL import ImageFilter
from PIL import ImageFont
from PIL import ImageOps
import pygame.rect
from spines_main_functions002 import *
import ols
from string import upper as uppercase
from optparse import OptionParser
from computer_data import computer_data as computer_data
from check_records_update_info import get_info as get_database_info
from check_records_update_info import get_record as get_record
from spines_main_functions002 import *

def get_limits(corners):

	return [numpy.min(corners,0),numpy.max(corners,0)]


def make_lines(limits,corners):
	out=[]
	y_min=int(limits[0][1])
	y_max=int(limits[1][1])
	for i in range(y_min,y_max):
		out.append([i,[]])
	return(out)
	
def cross_segment(line,segment):
	y_line=line[0]
	delta_y=segment[0][1]-segment[1][1]
	if delta_y>0:
		orientation=1
	else:
		orientation=-1
	
	t_pos=(segment[0][1]-y_line)
	b_pos=(segment[1][1]-y_line)
	crossing=t_pos*b_pos
	out=0
	
	if crossing<0:
		out=1
	else:	
		
		if (crossing==0)&(t_pos==0):
			out=2
		
	return [out,orientation,t_pos,b_pos]
	
def cross_point(line,segment):
	den=segment[1][1]-segment[0][1]
	#print den
	if den!=0:
		rho=float(segment[1][0]-segment[0][0])/float(den)
		x_l=int(segment[0][0]+rho*(line[0]-segment[0][1]))
		
	else:
		#print "none"
		x_l=None
	#print "x_l",x_l,line[0]
	
	return x_l


def fill_spine(corners):
	polygon_limits=get_limits(corners)
	v_lines=make_lines(polygon_limits,corners)

	for line_nr,line in enumerate(v_lines):
		cross_points=[]
		for i in range(len(corners)):
			segment=[corners[i-1],corners[i]]
			#print "seg",segment
			crossing_details=cross_segment(line,segment)
			if crossing_details[0]==1:
				x_pos=cross_point(line,segment)
				cross_points.append(x_pos)
			if crossing_details[0]==2:
				segment_pr=[corners[i-2],corners[i-1]]
				
				print line[0]
				print segment
				print segment_pr
				if crossing_details[1]==cross_segment(line,segment_pr)[1]:
					x_pos=cross_point(line,segment)
					cross_points.append(x_pos)
				print "---"
					
		cross_points.sort(lambda x, y: cmp(x,y),reverse=0)
		#print cross_points
		v_lines[line_nr][1]=cross_points
		#print v_lines[i]
	return(v_lines)
	
def extract_item(sequence,item_name):
	try:   
		item_index=map(lambda x: x[0],sequence).index(item_name)
		return(sequence[item_index][1])
	except (IndexError,ValueError):
		return(None)




class path_finder:
        def __init__(self,segment_start,segment_end):
		 outline_points=[]
		 #fig = plt.figure()             
		 #ax = fig.add_subplot(111)
		 
                 basic_coordinates=coordinate_system(segment_start,segment_end)
                 vector_length=basic_coordinates.length
		 vector_direction_delta=basic_coordinates.direction
                 orthogonal_1=basic_coordinates.orthogonal
		 
		 
                 path_start=segment_start[:]

                 

                 #oriented disk tranverse to the thorn
                 
                 tranverse_disk=range(-offset_range,offset_range)
                 tranverse_disk_oriented=[]
                 for offset in tranverse_disk:
                   tranverse_disk_oriented.append(map(int,multiply(offset,orthogonal_1)))
                 skeleton_list=[]  

                 for step in range(vector_length):
			 
                         projection=add(segment_start,multiply(step,vector_direction_delta))
                         distance_to_end=vector_length-step
                         max_tranverse_dist=tube_solig_angle_ratio*distance_to_end
                         #pygame.draw.circle(screen, pygame.Color("violet"), projection, 2, 1)
                         origin_to_start_looking=add(path_start,vector_direction_delta)
                         path_start=add(path_start,vector_direction_delta)
                         maximum_position=path_start[:]
                         maximum_intensity=0
			 points_array=[]
			 intensity_array=[]
			 gradient_array=[]
			 mpoint_nr=0
			 middle=0
                         for linear_position in tranverse_disk_oriented:
                                                        
                                                        
                                                        point_position=add(linear_position,path_start)
                                                        #print path_start
                                                        #print point_position
                                                        intensity=original_image[point_position[1],point_position[0]]
							intensity_array.append(int(intensity))
							points_array.append(point_position)
							gradient_array.append(original_image_gradient[point_position[1],point_position[0]])
                                                        #print "pos:",point_position
                                                        #print intensity,maximum_intensity
                                                        #pygame.draw.circle(screen, pygame.Color("violet"), point_position, 2, 1)
                                                        if (intensity>maximum_intensity):
                                                                #print "MAX"
                                                                if ((max_tranverse_dist-norm(subtract(projection,point_position)))>0):
									if (norm(linear_position)<skeleton_drift):
										maximum_intensity=intensity
										maximum_position=point_position[:]
										middle=mpoint_nr
                                                                
                                                        mpoint_nr=mpoint_nr+1
                         #print maximum_intensity
                         #print "final:",maximum_position
                         #print "---"
                         #pygame.gfxdraw.pixel(screen,maximum_position[0],maximum_position[1], pygame.Color("yellow"))                       
                         skeleton_list.append(maximum_position)
                         path_start=maximum_position[:]
			 #section_differentiated=differentiate(intensity_array)
			 #p_max=max(section_differentiated[:offset_range])
			 #p_min=min(section_differentiated[offset_range:])
			 #pp_max_index=(section_differentiated).index(p_max)
			 #pp_min_index=(section_differentiated).index(p_min)
			 #shift_horizontal_max_index=last_value(intensity_array,min(0.9*maximum_intensity,100),"left")
			 #shift_horizontal_min_index=last_value(intensity_array,min(0.9*maximum_intensity,100),"right")
			 if (method==1):
				p_max_index=gradient_max(gradient_array,middle,"left")
				p_min_index=gradient_max(gradient_array,middle,"right")
			 else:
				p_max_index=first_value(intensity_array,min(0.9*maximum_intensity,(1.0+halo_correct*(double(step)/vector_length))*threshold),"left")
				p_min_index=first_value(intensity_array,min(0.9*maximum_intensity,(1.0+halo_correct*(double(step)/vector_length))*threshold),"right")
							 
			
			 point=points_array[p_max_index.out]
			 if (p_max_index.found==1):
				outline_points.append([point,"l"])
			 else:
				pass
				
			 point=points_array[p_min_index.out]
			 if (p_min_index.found==1):
				 outline_points.append([point,"r"])
			 else:
				draw_notrendered(point,"orange")
			 
			
			 #pygame.draw.circle(screen, pygame.Color("violet"), points_array[p_max_index], 2, 1)
			 #ax.plot(section_differentiated,ls="-",marker="None")
		 #plt.show()
		 #print "OUTLINE",outline_points
		 self.segment_start=segment_start
		 self.segment_end=segment_end
		 self.outline=outline_points
		 self.threshold=threshold
                 self.point_list=skeleton_list
		 self.counter=counter
		 self.status="found"
		 self.geometry_details=[]
		 self.parameters=[]


def spine_mask(fill,image_size):
	l_spine_mask=numpy.ones(image_size)
	for line in fill:
			#print line
			cross_points=line[1]
			#print cross_points
			spine_pixels=[]
			for i in range(len(cross_points)/2):
			#if cross_segment(line,d_segment):
				l_spine_mask[line[0],cross_points[i*2]:cross_points[i*2+1]+1]=0
		
	return l_spine_mask

class measure_brightness:
   def __init__(self,image_data,l_spine_mask):
	t_1=time.time()
	picture_masked=numpy.ma.masked_array(image_data,l_spine_mask)
	core=numpy.ma.compressed(picture_masked)
	self.mean=numpy.mean(core)
	self.std=numpy.std(core)
	self.spine=core
	
def measure_correlation(fill,image_data_1,image_data_2,image_size):
	spine_mask=numpy.ones(image_size)
	for line in fill:
			#print line
			cross_points=line[1]
			#print cross_points
			spine_pixels=[]
			for i in range(len(cross_points)/2):
			#if cross_segment(line,d_segment):
				spine_mask[line[0],cross_points[i*2]:cross_points[i*2+1]+1]=0
	picture_masked_1=numpy.ma.masked_array(image_data_1,spine_mask)
	picture_masked_2=numpy.ma.masked_array(image_data_1,spine_mask)
	return numpy.mean(picture_masked)
		


def transform_object(object):
	#print "begin",begin[0],begin[1]
	#print "end",end[0],end[1]
	left_points=filter(lambda x: x[1]=="l",object.outline)
	right_points=filter(lambda x: x[1]=="r",object.outline)
	out=[]
	
	for i in range(0,len(left_points)):
			out.append(left_points[i][0])
			#pygame.gfxdraw.pixel(screen,left_points[i][0][0], left_points[i][0][1],pygame.Color(current_color))
	for i in range(0,len(right_points)):
			out.append(right_points[-1-i][0])
	return(out)
if __name__ in '__main__':
	if True:
		corners=[[10,10],[10,50],[14,34],[40,180],[100,100],[70,34],[180,180],[180,56],[400,2]]
		corners=multiply(3,corners)
		polygon_limits=get_limits(corners)
		size=add(10,polygon_limits[1])
		pg_mode = "RGB"
		display_screen=pygame.display.set_mode(size)
		pygame.init()
		#picture = pygame.image.fromstring(data, size, pg_mode)
		screen=pygame.Surface(size)
		#print polygon_limits
		fill=fill_spine(corners)
		for line in fill:
			print line
			cross_points=line[1]
			print cross_points
			for i in range(len(cross_points)/2):
			#if cross_segment(line,d_segment):
				pygame.draw.line(screen,pygame.Color("brown"),[cross_points[i*2],line[0]], [cross_points[i*2+1],line[0]], 1)


		for i in range(len(corners)):
			pygame.draw.line(screen,pygame.Color("yellow"),corners[i-1], corners[i], 1)
			
		display_screen.blit(screen,(0,0))
		pygame.display.flip()					
		while (True):
			pygame.event.pump()
			time.sleep(0.1)
	
	
	
	corners=[[10,10],[10,50],[14,34],[40,180],[100,100],[70,34],[180,180],[180,56],[400,2]]
	corners=multiply(3,corners)
	polygon_limits=get_limits(corners)
	fill=fill_spine(corners)
	
	
	#stack=askfn("C:\\Users\\k\\Desktop")
	stack="C:\\Users\\k\\Desktop\\b_5_21.cnt"
	pkl_file = open(stack, 'rb')
	main_object_list,picture_description= pickle.load(pkl_file)
	pkl_file.close()	
	size=extract_item(picture_description,"size")
	data=extract_item(picture_description,"image_data")
	
	
	pg_mode = "RGB"
	picture = pygame.image.fromstring(data, size, pg_mode)
	original_image=scipy.misc.fromimage(Image.fromstring(pg_mode, size,data),flatten=True)
	
	print type(original_image)
	display_screen=pygame.display.set_mode(size)
	pygame.init()
		#picture = pygame.image.fromstring(data, size, pg_mode)
	screen=pygame.Surface(size)
	screen.blit(picture, (0,0))
		#print polygon_limits
	fill=fill_spine(corners)
		
	
		
	for object in main_object_list:
		#draw_object(object,screen,current_color="green",connect_points=True)
		right_side=filter(lambda x:x[1]=="r",object.outline)
		left_side=filter(lambda x:x[1]=="l",object.outline)
		right_side=map(lambda x:x[0],right_side)
		left_side=map(lambda x:x[0],left_side)
		spmatrix=spine_membrane(right_side,left_side,size)
		
		for x in range(size[0]):
		   for y in range(size[1]):
			   if spmatrix[x][y]!=0:
				pygame.gfxdraw.pixel(screen,x,y,pygame.Color("white"))
		fill=fill_spine(transform_object(object))
		try:
			print measure_brightness(fill,original_image,size)
		
			for line in fill:
				#print line
				cross_points=line[1]
				#print cross_points
				#for i in range(len(cross_points)/2):
				#if cross_segment(line,d_segment):
					#pygame.draw.line(screen,pygame.Color("white"),[cross_points[i*2],line[0]], [cross_points[i*2+1],line[0]], 1)
		except:
			pass
		
				#pygame.draw.line(screen,pygame.Color("yellow"),[500,40], [502,40], 1)
	display_screen.blit(screen,(0,0))
	pygame.display.flip()
	im_string=pygame.image.tostring(screen,"RGB")
	im_out=Image.fromstring(pg_mode, size, im_string)
	im_out=im_out.convert("RGB")
	im_out.save("C:\\Users\\k\\Desktop\\test.tif",format="TIFF")
	pygame.quit()	
	#while (True):
	#		pygame.event.pump()
	#		time.sleep(0.1)
	
		