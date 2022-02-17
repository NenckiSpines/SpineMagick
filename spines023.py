# -*- coding: cp1250 -*-
import csv
import numpy
import scipy,os
import Tkinter as tk
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
from easygui import boolbox as boolbox
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
from fill_polygon import measure_brightness as measure_brightness
from fill_polygon import  spine_mask as spine_mask
from fill_polygon import fill_spine as fill_spine
from easygui import buttonbox

class ImageStructure:
        def __init__(self,im):
		size=im.size
		aux_matrix_x=numpy.zeros(size)
		aux_matrix_y=numpy.zeros(size)
		for i in range(size[0]):
			for j in range(size[1]):
				aux_matrix_x[i][j]=j
				aux_matrix_y[i][j]=i
		self.aux_matrix_x=aux_matrix_x
		self.aux_matrix_y=aux_matrix_y

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

                 for step in range(int(vector_length)):
			 
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


class smooth_trajectory():
	def __init__(self,object):
		basic_coordinates=coordinate_system(object.segment_start,object.segment_end)
		right_side=filter(lambda x:x[1]=="r",object.outline)[-1][0]
		left_side=filter(lambda x:x[1]=="l",object.outline)[-1][0]
		foot_vect=subtract(right_side,left_side)
		x_coll=range(len(object.point_list))
		y_coll=[]
		x_vals=[]
		for point,step in zip(object.point_list,x_coll):
			projection=add(object.segment_start,multiply(-basic_coordinates.direction,sum(multiply(basic_coordinates.direction,subtract(object.segment_start,point)))))
			projection1=add(object.segment_start,multiply(step,basic_coordinates.direction))
			projection_distance=sum(multiply(subtract(projection,point),basic_coordinates.orthogonal))
			y_coll.append(projection_distance)
			x_vals.append(projection)
		r_vals=[]
		
		y_coll=numpy.array(y_coll)
		cof=[]
		poly_max=4
		fourier_coeff=pi/x_coll[-1]
		for k in range(1,poly_max):
			#function=lambda x: numpy.sin(k*x*fourier_coeff)
			function=lambda x: pow(x,k)
			cof.append(map(function,x_coll))
		cof=(numpy.array(cof)).transpose()
		mls = ols.ols(y_coll,cof)
		fourier_coefficients=mls.b
		#print fourier_coefficients
		filtered_trajectory=[]
		for i in x_coll:
			r_val=fourier_coefficients[0]
			for k in range(1,poly_max):
				#r_val=r_val+fourier_coefficients[k]*sin(k*i*fourier_coeff)
				r_val=r_val+fourier_coefficients[k]*pow(i,k)
			filtered_position=add(multiply(r_val,-basic_coordinates.orthogonal),x_vals[i])
			#filtered_position=x_vals[i]
			foot_right_to_trajectory_vect=subtract(right_side,filtered_position)
			if (symplectic(foot_vect,foot_right_to_trajectory_vect)>0):
				filtered_trajectory.append(filtered_position)
		object.geometry_details.append(["filtered_trajectory",filtered_trajectory])
		self.trajectory=filtered_trajectory
		
class profile_finder():
	def __init__(self,object,trajectory):
		print "analyzing spine:",object.counter 
		basic_coordinates=coordinate_system(object.segment_start,object.segment_end)
		right_side=filter(lambda x:x[1]=="r",object.outline)
		left_side=filter(lambda x:x[1]=="l",object.outline)
		
		trajectory_length=len(trajectory)
		trans_widths=[]
		head_edges=[]
		trajectory_orthogonals=[]
		extras=[]
		for point in range(0,trajectory_length-1):
			trajectory_normal=trajectory[point]-trajectory[point+1]
			#print trajectory_normal
			trajectory_normal=multiply(1.0/norm(trajectory_normal),trajectory_normal)
			trajectory_orthogonal=[-trajectory_normal[1],trajectory_normal[0]]
			
			
			closest_point_to_orthogonal_r=None
			closest_point_to_orthogonal_l=None
			
			min_distance_to_orthogonal=numpy.inf
			for y_0 in right_side: 
				t_val=point_to_line(trajectory_orthogonal,trajectory[point],y_0[0])
				y_1=add(multiply(t_val,trajectory_orthogonal),trajectory[point])
				distance=norm(subtract(y_1,y_0[0]))
				if (distance<min_distance_to_orthogonal):
					min_distance_to_orthogonal=distance
					closest_point_to_orthogonal_r=y_0[0]
					
			if (min_distance_to_orthogonal>2):
				closest_point_to_orthogonal_r=None
			#print min_distance_to_orthogonal	
			min_distance_to_orthogonal=numpy.inf
			for y_0 in left_side: 
				t_val=point_to_line(trajectory_orthogonal,trajectory[point],y_0[0])
				y_1=add(multiply(t_val,trajectory_orthogonal),trajectory[point])
				distance=norm(subtract(y_1,y_0[0]))
				if (distance<min_distance_to_orthogonal):
					min_distance_to_orthogonal=distance
					closest_point_to_orthogonal_l=y_0[0]
					
			if (min_distance_to_orthogonal>2):
				closest_point_to_orthogonal_l=None
			#print min_distance_to_orthogonal
			
			try:		
				cross_section_width=norm(subtract(closest_point_to_orthogonal_r,closest_point_to_orthogonal_l))
			except(TypeError):
				cross_section_width=numpy.nan
				#print "nan"
			#print cross_section_width
			#print "---"
			head_edges.append([closest_point_to_orthogonal_r,closest_point_to_orthogonal_l])
			trans_widths.append(cross_section_width)
			trajectory_orthogonals.append(trajectory_orthogonal)
		point=argv_max(trans_widths[:-trajectory_length/3])
		neck_point=point+argv_min(trans_widths[point:])
		max_width=argv_max(trans_widths)
		#print trans_widths
		#print "+++"
		if (point!=None):
			#print point,trans_widths[point]
			#max_location=[add(trajectory[point],multiply(-20,trajectory_orthogonals[point])),add(trajectory[point],multiply(20,trajectory_orthogonals[point]))]
			object.geometry_details.append(["head_position",trajectory[point]])
			object.geometry_details.append(["head_width",trans_widths[point]])
			object.geometry_details.append(["max_width",trans_widths[max_width]])
			object.geometry_details.append(["neck_width",trans_widths[neck_point]])
			object.geometry_details.append(["neck_point",neck_point])
			object.geometry_details.append(["head_edges",head_edges[point]])
			object.geometry_details.append(["max_width_loc",(1.0*max_width)/(trajectory_length-1)])
			
class dendrite_finder:
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
                 dendrite_offset=int(dendrite_width/2)
                 tranverse_disk=range(-dendrite_offset,dendrite_offset)
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
			 #gradient_array=[]
			 mpoint_nr=0
			 middle=0
			 l_max=0
                         for linear_position in tranverse_disk_oriented:
                                                        
                                                        
                                                        point_position=add(linear_position,path_start)
                                                        #print path_start
                                                        #print point_position
                                                        intensity=original_image[point_position[1],point_position[0]]
							intensity_array.append(int(intensity))
							points_array.append(point_position)
							#gradient_array.append(original_image_gradient[point_position[1],point_position[0]])
                                                        #print "pos:",point_position
                                                        #print intensity,maximum_intensity
                                                        #pygame.draw.circle(screen, pygame.Color("violet"), point_position, 2, 1)
                                                        if (intensity>maximum_intensity):
                                                                #print "MAX"
                                                                if ((max_tranverse_dist-norm(subtract(projection,point_position)))>0):
										maximum_intensity=intensity
										maximum_position=point_position[:]
										middle=mpoint_nr
										l_max=linear_position
                                                                
                                                        mpoint_nr=mpoint_nr+1
			 int_mean=mean(intensity_array)
			 #print points_array
			 #print intensity_array
			 center=vect_center(intensity_array,range(len(intensity_array)))
			 maximum_position=points_array[center]
			 #print p_center
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
		 self.status="dendrite"
		 self.geometry_details=[]
		 self.parameters=[]


class smooth_trajectory_dendrite():
	def __init__(self,object):
		basic_coordinates=coordinate_system(object.segment_start,object.segment_end)
		x_coll=range(len(object.point_list))
		y_coll=[]
		x_vals=[]
		for point,step in zip(object.point_list,x_coll):
			projection=add(object.segment_start,multiply(-basic_coordinates.direction,sum(multiply(basic_coordinates.direction,subtract(object.segment_start,point)))))
			projection_distance=sum(multiply(subtract(projection,point),basic_coordinates.orthogonal))
			y_coll.append(projection_distance)
			x_vals.append(projection)
		r_vals=[]
		
		y_coll=numpy.array(y_coll)
		cof=[]
		poly_max=smoothing_degree+1
		fourier_coeff=pi/x_coll[-1]
		for k in range(1,poly_max):
			#function=lambda x: numpy.sin(k*x*fourier_coeff)
			function=lambda x: pow(x,k)
			cof.append(map(function,x_coll))
		cof=(numpy.array(cof)).transpose()
		mls = ols.ols(y_coll,cof)
		fourier_coefficients=mls.b
		#print fourier_coefficients
		filtered_trajectory=[]
		for i in x_coll:
			r_val=fourier_coefficients[0]
			for k in range(1,poly_max):
				#r_val=r_val+fourier_coefficients[k]*sin(k*i*fourier_coeff)
				r_val=r_val+fourier_coefficients[k]*pow(i,k)
			filtered_position=add(multiply(r_val,-basic_coordinates.orthogonal),x_vals[i])
			#filtered_position=x_vals[i]
			#foot_right_to_trajectory_vect=subtract(right_side,filtered_position)
			#if (symplectic(foot_vect,foot_right_to_trajectory_vect)>0):
			filtered_trajectory.append(filtered_position)
		object.geometry_details.append(["filtered_trajectory",filtered_trajectory])
		self.trajectory=filtered_trajectory
		
def count_spines(main_object_list):
		count=0
		for object in main_object_list:
			if ((object.status!="deleted")&(object.status!="dendrite")):
				count=count+1
		return(count)
		
			
		
def format_input(int_string):
	int_string=uppercase(int_string)
	int_string=int_string.replace(" ","")
	int_string=int_string.replace(",",".")
	return(int_string)
def render_geometry(object):
	if object.status!="dendrite":
		try:
			trajectory=(smooth_trajectory(object)).trajectory
			object.status="rendered"
		except(IndexError):
			object.status="deleted"
			trajectory=None
		if (trajectory!=None):
			try:
				profile_finder(object,trajectory)
			except:
				object.status="deleted"

			
	
		
            
def extract_item(sequence,item_name):
	try:   
		item_index=map(lambda x: x[0],sequence).index(item_name)
		return(sequence[item_index][1])
	except (IndexError,ValueError):
		return(None)
			
def remove_item(sequence,item_name):
	try:   
		item_index=map(lambda x: x[0],sequence).index(item_name)
		sequence.pop(item_index)
	except (IndexError,ValueError):
		pass
	return(sequence)

def archive_old_entries(sequence):
	new_seq=[]
	for item in sequence:
			if item[0]!="image_data":
				#if item[0][-4:]!="_mod":
				#	header_item=item[0]+"_mod"
				#else:
				#header_item=item[0]
				new_seq.append(item)
	return (new_seq)
def archive_tracking(picture_description,picture_description_archived):
			 items_modified=[]
			 for item in picture_description:
				 if (item[0]!='image_data'):
					 archived_item=extract_item(picture_description_archived,item[0])
					 if item[1]!=archived_item:
						 print "Modified",item,archived_item
						 items_modified.append([item[0]+"_changed",archived_item,item[1],time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime())])
			 for item in picture_description_archived:
				 if item[0][-8:]=="_changed":
					items_modified.append(item)
			 items_modified.append(["picture_changed",time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime())])
			 return(items_modified)
			 
def display_surface_update():	
						global zoom_window_origin
						rect_position=10
						small_text_shift=60
						display_screen.blit(screen,(0,0),(shift_horizontal,shift_vertical,max_x,max_y))
						try:
							object_to_zoom=multiply(add((main_object_list[-1]).segment_start,(main_object_list[-1]).segment_end),0.5)
							object_to_zoom=add(object_to_zoom,zoom_shift)
							zoom_window_origin=(object_to_zoom[0]-magnification_window_size_2,object_to_zoom[1]-magnification_window_size_2)
						
							magnification_surface=pygame.Surface((magnification_window_size, magnification_window_size))
							
							magnification_surface.blit(screen,(0,0),(zoom_window_origin[0],zoom_window_origin[1],magnification_window_size_2*2,magnification_window_size_2*2))
							magnification_surface_new=pygame.transform.scale(magnification_surface,(magnification_window_size*zoom_factor, magnification_window_size*zoom_factor))
							display_screen.blit(magnification_surface_new,(first_tab,display_size[1]))
						
						except(IndexError):
							pass
						print first_tab,extra_space
						parameter_surface=pygame.Surface((first_tab,extra_space))
						parameter_surface.fill(color=pygame.Color(10,10,10,1))
						offset_down=0
						if ((method==0)&(mode==0)):
							gameprint(parameter_surface,"THRESHOLD: "+str(threshold),10,small_text_shift+15,"orange",font_size=13)
							gameprint(parameter_surface,"HALO CORRECTION: "+str(round(halo_correct,1)),10,small_text_shift+30,"orange",font_size=13)
							gameprint(parameter_surface,"SKELETON DRIFT: "+str(round(skeleton_drift,1)),10,small_text_shift+45,"orange",font_size=13)
							offset_down=offset_down+60
						if ((method==1)&(mode==0)):
							gameprint(parameter_surface,"GRADIENT OFFSET: "+str(gradient_offset),10,small_text_shift+15,"orange",font_size=13)
							offset_down=offset_down+30
						if (mode==1):
							gameprint(parameter_surface,"SMOOTHING DEGREE: "+str(smoothing_degree),10,small_text_shift+15,"orange",font_size=13)
							offset_down=offset_down+30
						gameprint(parameter_surface,"COUNTER: "+str(counter),10,small_text_shift+offset_down,"green",font_size=13)
						offset_down=offset_down+15
						gameprint(parameter_surface,"max width",10,small_text_shift,"blue",font_size=11)
						if turn_spines_off==1:
							gameprint(parameter_surface,"LAST SPINE HIDDEN !",10,small_text_shift+offset_down,"red",font_size=13)
							offset_down=offset_down+15
						if turn_spines_off==2:
							gameprint(parameter_surface,"ALL SPINES HIDDEN !",10,small_text_shift+offset_down,"red",font_size=13)
							offset_down=offset_down+15
						gameprint(parameter_surface,"MODE: "+str(mode_dict[mode]),10,small_text_shift+offset_down,"yellow",font_size=13)	
						if mode==0:
							current_width=spine_width
						if mode==1:
							current_width=dendrite_width
						pygame.draw.line(parameter_surface,pygame.Color("blue"),(78,small_text_shift+2), (78,small_text_shift+10), 1)
						pygame.draw.line(parameter_surface,pygame.Color("blue"),(78+current_width,small_text_shift+2), (78+current_width,small_text_shift+10), 1)
						rect_shift_x=int(shift_horizontal*40.0/size[0])
						#print shift_horizontal
						rect_shift_xm=int((display_size[0])*40.0/size[0])
						rect_shift_y=int(shift_vertical*40.0/size[0])
						rect_shift_ym=int((display_size[1])*40.0/size[0])
						if (oversize==True):
							parameter_surface.blit(pic_icon,(10,rect_position))
							#print [10+rect_shift_x,rect_position+rect_shift_y,rect_shift_xm,rect_shift_ym]
							pygame.draw.rect(parameter_surface,pygame.Color("orange"), [10,rect_position,40,icon_y_size],1)
							pygame.draw.rect(parameter_surface,pygame.Color("yellow"), [10+rect_shift_x,rect_position+rect_shift_y,rect_shift_xm,rect_shift_ym],1)
						display_screen.blit(parameter_surface,(0,display_size[1]))
						pygame.display.flip()

                                         
                                  
class redraw:
	def __init__(self,old_surface=None,turn_last=0):
			screen.blit(picture, (0,0))
			object_nr=len(main_object_list)
			
			if turn_last!=2:
				if ((old_surface==None)|(object_nr<max_nr_to_display_individually)):
					objects_to_display=range(object_nr)
					
				else:
					objects_to_display=[object_nr-2,object_nr-1]
					screen.blit(old_screen_copy,(0,0))
			else:
				objects_to_display=[]
			#turns the last one off
			if turn_last==1:
				try:
					objects_to_display.pop(-1)
				except (ValueError,IndexError):
					pass
			
			for i in objects_to_display:
				 object=main_object_list[i]
				 if (object.status!="deleted"):
					#t_s=time.time()
					if (i!=object_nr-1):
						ccolor="blue"
					else:
						ccolor="red"
					draw_object(object,screen,ccolor)
					#print "T0",time.time()-t_s
					t_s=time.time()
					trajectory=extract_item(object.geometry_details,"filtered_trajectory")
					if (trajectory!=None):
						if object.status!="dendrite":
							display_path(trajectory)
						else:
							display_path(trajectory,color="orange",lw=2)
					if (privilige==2):
						head_edges=extract_item(object.geometry_details,"head_edges")
						if (head_edges!=None):
							pygame.draw.line(screen,pygame.Color("red"),head_edges[0],head_edges[1], 1)
					
			display_surface_update()
			
	
def merge_objects(main_object_list):
	msg = "Objects to merge:"
        title = "Merge objects"
        fieldNames = ["Outer object","Inner object"]
	fieldValues =["",""]
        fieldValues = multenterbox(msg,title, fieldNames,fieldValues)
        
	try:
		obj1,obj2=map(int,fieldValues) 
		
		object1=main_object_list[get_object(main_object_list,obj1)]
		object2=main_object_list[get_object(main_object_list,obj2)]
		if ((object1.status!="dendrite")&(object2.status!="dendrite")):
			object1.segment_end=object2.segment_end
			object1.status="merged"
			object2.status="deleted"
			object1.outline=object1.outline+object2.outline
			display_path(object1.point_list,"red")
			display_path(object2.point_list,"green")
			object1.point_list=object1.point_list+object2.point_list
			display_path(object1.point_list,"yellow")
	#except(IOError):
	except(IndexError,TypeError,ValueError,AttributeError):
		print "no objects"
def max_objectnr(main_object_list):
	max_nr=0
	for object in main_object_list:
			if object.counter>max_nr:
				max_nr=object.counter
	return(max_nr)
def rename_objects(main_object_list):
	global counter
	msg = "Objects to renumber:"
        title = "Renumber objects"
        fieldNames = ["Old Number","New Number"]
	fieldValues =["",""]
        fieldValues = multenterbox(msg,title, fieldNames,fieldValues)
        
	try:
		nr_1,nr_2=map(int,fieldValues) 
		can_rename=1
		for object in main_object_list:
			if object.counter==nr_2:
				can_rename=0
		if can_rename==1:
			for object in main_object_list:
				if object.counter==nr_1:
					object.counter=nr_2
	except(IndexError,TypeError,ValueError):
		print "no objects"
	counter=max_objectnr(main_object_list)

def get_object(main_object_list,object_nr):
	out=None
	for i,object in enumerate(main_object_list):
			if object.counter==object_nr:
				out=i
	return(out)

def delete_object(main_object_list):
	object_id=integerbox(msg='Enter object number to delete', title='Delete Object ', argLowerBound=1, argUpperBound=counter+1)	
	try:	
		object_to_remove=get_object(main_object_list,object_id)
		if object_to_remove!=None:
			(main_object_list[object_to_remove]).status="deleted"
	except(IndexError,TypeError):
		print "Wrong Value"

def rearrange_numbers(main_object_list,ask_for_manual="auto"):
	global counter
	#print len(main_object_list)
	for i in range(len(main_object_list),0,-1):
		#print (main_object_list[i-1]).status
		#print (main_object_list[i-1]).segment_end
		if (((main_object_list[i-1]).status)=="deleted"):
			main_object_list.pop(i-1)
	
	
	main_object_list.sort(lambda x, y: cmp(x.segment_end[0],y.segment_end[0]),reverse=0)
	if ask_for_manual=="auto":
		for i in range(len(main_object_list)):
			(main_object_list[i]).counter=i+1
		counter=len(main_object_list)
	if ask_for_manual=="manual":
		rename_objects(main_object_list)
	
		
def calculate_pearson(brightness_info_1,brightness_info_2):
							covariance=numpy.mean(numpy.multiply(brightness_info_1.spine,brightness_info_2.spine))
							denominator=(brightness_info_1.std*brightness_info_2.std)
							if denominator!=0:
								pearson_coeff=(covariance-brightness_info_1.mean*brightness_info_2.mean)/denominator
							else:
								pearson_coeff=0
							return(pearson_coeff)		


def ask_password(licence):
	msg = "Licence Number: "+str(licence)
        title = "Registration"
        fieldNames = ["Enter Key Number"]
	fieldValues = multenterbox(msg,title, fieldNames)
	return (fieldValues[0])

def set_parameters():
	global threshold
	global skeleton_drift
	global tube_solig_angle_ratio
	global offset_range
	global backup_file
	global spine_width
	msg = "Modify parameters"
        title = "Parameters Setting"
        fieldNames = ["Threshold","Skeleton Drift","Cone solid angle","Width","Backup File"]
        fieldValues = [threshold,skeleton_drift,tube_solig_angle_ratio,spine_width,backup_file]  # we start with blanks for the values
        fieldValues = multenterbox(msg,title, fieldNames,fieldValues)
	try:
		threshold,skeleton_drift,tube_solig_angle_ratio,spine_width=map(double,fieldValues[:-1])
		backup_file=fieldValues[-1]
		offset_range=spine_width/2
	except(ValueError):
		print "Wrong Values"
	except(TypeError):
		print "No Change"
	
	#threshold=integerbox(msg='Threshold',default=threshold, title=' ',argLowerBound=0, argUpperBound=255)

def last_value(lst,value,side="right"):
	i=0
	out=0
	for intensity in lst:
		if (intensity>value):
			out=i
			if (side=="left"):
				break
		i=i+1 
	return(out)


class im_opening_3d:
        def __init__(self,stack_name):
		
		im =Image.open(stack_name)
		stack_screens=[]
		stack_data=[]
		frame_index=0
		try:
		  while 1:
		    im.seek(frame_index)
		    print frame_index
		    frame_index = frame_index + 1
		    if (im!=None):
			if (im.mode!="RGB"):
			    frame=im.convert("RGB")
			else:
			    frame=im
			frame = frame.filter(GAUSSIAN)
			data = frame.tostring()
			size=frame.size
			#print size
			#print "ll"
			picture = pygame.image.fromstring(data, size, pg_mode)
			stack_screens.append(picture)
			stack_data.append(scipy.misc.fromimage(frame,flatten=False))
			#q.put(frame_filtered)
			#tkIm = ImageTk.PhotoImage(frame_filtered)
			#label_image = tk.Label(root, image=tkIm)
			#label_image.place(x=0,y=0,width=im.size[0],height=im.size[1])
			#root.update()
			#time.sleep(15)
		except EOFError:
		   print "eof"
		   im.seek(0)
		   pass
		   
		last_frame_index=frame_index-1
		self.screens=stack_screens
		self.data=stack_data
		self.frame_number=last_frame_index



class first_value:
        def __init__(self,lst,value,side):
		if (side=="left"):
			i=0
			out=0
			
			for intensity in lst[:len(lst)/2]:
				if (intensity<value):
					out=i+1
				i=i+1 
			if (out==0):
				if_found=0
			else:
				if_found=1
		if (side=="right"):
			
			if_found=0
			out=len(lst)/2+1
			i=out
			for intensity in lst[len(lst)/2:]:
				if (intensity<value):
					out=i-1
					if_found=1
					break
				i=i+1 
		self.found=if_found
		self.out=out
			
class gradient_max:
        def __init__(self,series,middle,side):
		length=len(series)
		if (side=="left"):
			a=range(0,middle)
			lk=-gradient_offset
		if (side=="right"):
			a=range(middle,length)
			lk=gradient_offset
		intensity=0
		out=middle
		for i in a:
			if ((series[i])>intensity):
				intensity=series[i]
				out=i+lk
		try:
			if (out<a[0]):
				out=a[0]
			if (out>a[-1]):
				out=a[-1]
			found=1
		except (IndexError):
			found=0
			
		self.found=found
		self.out=out


def draw_notrendered(point,color):
	#print "begin",begin[0],begin[1]
	#print "end",end[0],end[1]
	pygame.gfxdraw.pixel(screen,int(point[0]),int(point[1]), pygame.Color(color)) 
	
			
		 
		 
def measure_path(path):
	distance=0
	for i in range(1,len(path)):
		 point_start=path[i-1]
		 point_end=path[i]
		 #print subtract(point_start, point_end)
		 distance=distance+metric(subtract(point_start, point_end),metric_components)
	return(distance)

def display_path(path,color="purple",lw=1):
	for i in range(1,len(path)):
		 point_start=path[i-1]
		 point_end=path[i]
		 pygame.draw.line(screen, pygame.Color(color), point_start, point_end, lw)
	
	#display_screen.blit(screen,(0,0),(shift_horizontal,shift_vertical,max_x,max_y))
	#pygame.display.flip()
	

def differentiate(series):
      ka=list(numpy.zeros(len(series)))
      for i in range (1,len(series)):
            ka[i]=series[i]-series[i-1]
      return (ka)

def render_all(main_object_list,rendering_all=False):
	 if (rendering_all==False):
		for object in main_object_list:
				 if ((object.status!="rendered")&(object.status!="deleted")&(object.status!="dendrite")):
					render_geometry(object)
	 else:
		 for object in main_object_list:
				 if ((object.status!="deleted")&(object.status!="dendrite")):
					object.geometry_details=[]
					try:
						render_geometry(object)
					except(ZeroDivisionError):
						object.status="deleted"
		 
	 
					
	
					
def object_measurements(path,aux_structure):
	trajectory=extract_item(path.geometry_details,"filtered_trajectory")
	
	#print path.geometry_details
	#print "MEASURING:",path.counter
	if (trajectory!=None):
	
		if path.status!="dendrite":
			
			right_side=filter(lambda x:x[1]=="r",path.outline)
			left_side=filter(lambda x:x[1]=="l",path.outline)
			
			if ((len(right_side)>0)&((len(left_side)>0))):

				# structures from outline
				right_side=map(lambda x:x[0],right_side)
				left_side=map(lambda x:x[0],left_side)
				contour=right_side[:]
				contour.reverse()
				contour=left_side+contour
				
				#length measurements
				length=measure_path(trajectory)
				print "length",length
				path.parameters.append(["length",length])
				
				#head width measurements
				head_width=extract_item(path.geometry_details,"head_width")
				max_width_location=extract_item(path.geometry_details,"max_width_loc")
				max_width=extract_item(path.geometry_details,"max_width")
				if (head_width!=None):
					head_width_metric=head_width*metric_components[0]
					path.parameters.append(["head_width",head_width_metric])
					path.parameters.append(["max_width_location",max_width_location])
					if (max_width!=None):
						path.parameters.append(["max_width",max_width*metric_components[0]])
					else:
						path.parameters.append(["max_width",numpy.nan])
					try:
						path.parameters.append(["width_length_ratio",head_width_metric/length])
					except:
						path.parameters.append(["width_length_ratio",numpy.nan])
					try:
						path.parameters.append(["length_width_ratio",length/head_width_metric])
					except:
						path.parameters.append(["length_width_ratio",numpy.nan])
					
				else:
					path.parameters.append(["head_width",numpy.nan])
					
				#neck measurements
				neck_width=extract_item(path.geometry_details,"neck_width")
				neck_point=extract_item(path.geometry_details,"neck_point")
				top_contour=right_side[:neck_point]
				top_contour.reverse()
				top_contour=left_side[:neck_point]+top_contour
				bottom_contour=right_side[neck_point:]
				bottom_contour.reverse()
				bottom_contour=left_side[neck_point:]+bottom_contour
				
				if (neck_width!=None):
					path.parameters.append(["neck_width",neck_width*metric_components[0]])
				else:
					path.parameters.append(["neck_width",numpy.nan])
			
				
				try:   
					tip_vector=subtract(right_side[0],left_side[0])
					tip_length=metric(tip_vector,metric_components)
					foot_vector=subtract(right_side[-1],left_side[-1])
					foot_length=metric(foot_vector,metric_components)
					print "foot",foot_length
					path.parameters.append(["foot",foot_length])
				except(IndexError):
					foot_length=0
					print "insufficient contour:"
				try:
					circumference=measure_path(right_side)+measure_path(right_side)+foot_length+tip_length
					print "circumference",circumference
					path.parameters.append(["circumference",circumference])
				except(IndexError):
					print "insufficient contour:"
				
				try:
					area=measure_area(contour,metric_components)
					path.parameters.append(["area",area])
				except(IndexError):
					print "insufficient contour:"
				try:
					path.parameters.append(["length_area_ratio",length/area])
				except:
					path.parameters.append(["length_area_ratio",numpy.nan])
				if (head_width<1.0):
					path.status="deleted"
				if (area<0):
					path.status="deleted"
				
				try:
					#filling interior of the spine
					fill=fill_spine(contour)
					fill_top=fill_spine(top_contour)
					fill_bottom=fill_spine(bottom_contour)
					
					
					#measurements based on interior
					fill_mask=spine_mask(fill,size)
					fill_mask_top=spine_mask(fill_top,size)
					fill_mask_bottom=spine_mask(fill_bottom,size)
					membrane_matrix=spine_membrane(right_side,left_side,size)
					int_brightness=(measure_brightness(original_image,fill_mask)).mean
					path.parameters.append(["mean_brightness",int_brightness])
					
					#other channels
					
					if channel_info!=None:
						
						x_m=measure_brightness(aux_structure.aux_matrix_x,fill_mask).mean
						y_m=measure_brightness(aux_structure.aux_matrix_y,fill_mask).mean
						
						brightness_info_1=measure_brightness(extra_channels[colocalizing_channels[0]],fill_mask)
						brightness_info_2=measure_brightness(extra_channels[colocalizing_channels[1]],fill_mask)
						
						brightness_info_top_1=measure_brightness(extra_channels[colocalizing_channels[0]],fill_mask_top)
						brightness_info_top_2=measure_brightness(extra_channels[colocalizing_channels[1]],fill_mask_top)
						
						brightness_info_bottom_1=measure_brightness(extra_channels[colocalizing_channels[0]],fill_mask_bottom)
						brightness_info_bottom_2=measure_brightness(extra_channels[colocalizing_channels[1]],fill_mask_bottom)
						
						membrane_info_1=measure_brightness(extra_channels[colocalizing_channels[0]],membrane_matrix)
						membrane_info_2=measure_brightness(extra_channels[colocalizing_channels[1]],membrane_matrix)
						
						mean_channel_1=numpy.mean(extra_channels[colocalizing_channels[0]])
						mean_channel_2=numpy.mean(extra_channels[colocalizing_channels[1]])
						
						path.parameters.append(["x_m",x_m])
						path.parameters.append(["y_m",y_m])
						
						path.parameters.append(["mean_brightness_"+channel_names[colocalizing_channels[0]],brightness_info_1.mean])
						path.parameters.append(["mean_brightness_"+channel_names[colocalizing_channels[1]],brightness_info_2.mean])
						
						path.parameters.append(["mean_brightness_top_"+channel_names[colocalizing_channels[0]],brightness_info_top_1.mean])
						path.parameters.append(["mean_brightness_top_"+channel_names[colocalizing_channels[1]],brightness_info_top_2.mean])
						
						path.parameters.append(["mean_brightness_bottom_"+channel_names[colocalizing_channels[0]],brightness_info_bottom_1.mean])
						path.parameters.append(["mean_brightness_bottom_"+channel_names[colocalizing_channels[1]],brightness_info_bottom_2.mean])
						
						path.parameters.append(["membrane_brightness_"+channel_names[colocalizing_channels[0]],membrane_info_1.mean])
						path.parameters.append(["membrane_brightness_"+channel_names[colocalizing_channels[1]],membrane_info_2.mean])
						
						path.parameters.append(["BCKG_sub_brght_"+channel_names[colocalizing_channels[0]],brightness_info_1.mean-mean_channel_1])
						path.parameters.append(["BCKG_sub_brght_"+channel_names[colocalizing_channels[1]],brightness_info_2.mean-mean_channel_2])
						
						#calculate pearson
						
						pearson_coeff=calculate_pearson(brightness_info_1,brightness_info_2)
						path.parameters.append(["in_spine_pearson",pearson_coeff])						
				except:
					path.status="deleted"
				
		if path.status=="dendrite":
			length=measure_path(trajectory)
			path.parameters.append(["length",length])

def parameters_dumper(object_list,out_file_csv):
	write_file3=open(out_file_csv, "wb")
	csv_writer = csv.writer(write_file3,delimiter=',')			 
	names=[]
	for object in object_list:
		for name in map(lambda x:x[0],object.parameters):
			if (names.count(name)==0):
				names.append(name)
	csv_writer.writerow(["File name:",stack])
	csv_writer.writerow(["Scale:",global_scale])
	csv_writer.writerow(["ID_0:",random_id[0]])
	csv_writer.writerow(["ID_1:",random_id[1]])
	csv_writer.writerow(["Version:",globs.version])
	
	for animal_parameter,animal_parameters_name in zip(animal_parameters,animal_parameters_names):
		csv_writer.writerow([animal_parameters_name,animal_parameter])
	
	total_dendrite_width=0

	true_spines_nr=double(extract_item(picture_description,"spines_nr"))
	dendrite_length=double(extract_item(picture_description,"marked_dendrite_length"))
	csv_writer.writerow(["Marked Dendrite Length"]+[dendrite_length])
	if dendrite_length!=0:
		csv_writer.writerow(["Spines Linear Density"]+[true_spines_nr/dendrite_length])
	csv_writer.writerow(["------"])
	csv_writer.writerow(["spine number"]+names)
	parameter_matrix=[]
	for object in object_list:
		if ((object.status=="deleted")|(object.status=="dendrite")):
			continue
		parameter_row=empty_list(len(names))
		for parameter in object.parameters:
			parameter_index=names.index(parameter[0])
			parameter_row[parameter_index]=parameter[1]
		parameter_matrix.append(parameter_row)	
		csv_writer.writerow([object.counter]+parameter_row)
	mean_values_of_par=[]
	std_values_of_par=[]
	try:
		for column_index in range(len(parameter_matrix[0])):
			ensemble=[]
			for row_index in range(len(parameter_matrix)):
				current_element=parameter_matrix[row_index][column_index]
				if (current_element!="N/A"):
					ensemble.append(current_element)
			ensemble_filtered=filter(lambda x:numpy.isfinite(x),ensemble)
			mean_values_of_par.append(mean(ensemble_filtered))
			std_values_of_par.append(std(ensemble_filtered))
		csv_writer.writerow([" "])
		csv_writer.writerow(["Mean Values:"]+mean_values_of_par)
		csv_writer.writerow(["Standard Deviations:"]+std_values_of_par)
	except(IndexError):
		csv_writer.writerow(["Error: Cannot calculate statistics!"])
		
	write_file3.close()

def gaussian_grid(size = 5):
        """
        Create a square grid of integers of gaussian shape
        e.g. gaussian_grid() returns
        array([[ 1,  4,  7,  4,  1],
                   [ 4, 20, 33, 20,  4],
                   [ 7, 33, 55, 33,  7],
                   [ 4, 20, 33, 20,  4],
                   [ 1,  4,  7,  4,  1]])
        """
        m = size/2
        n = m+1  # remember python is 'upto' n in the range below
        x, y = mgrid[-m:n,-m:n]
        # multiply by a factor to get 1 in the corner of the grid
        # ie for a 5x5 grid   fac*exp(-0.5*(2**2 + 2**2)) = 1
        fac = exp(m**2)
        g = fac*exp(-0.5*(x**2 + y**2))
        return g.round().astype(int)

class GAUSSIAN(ImageFilter.BuiltinFilter):
        name = "Gaussian"
        gg = gaussian_grid().flatten().tolist()
        filterargs = (5,5), sum(gg), 0, tuple(gg)
	

def data_entry():
	
	msg = "Enter Scale:"
	title = "Image Parameters"
	fieldNames = ["Global Scale"]+animal_parameters_names
	numerical_id=[0]
	try:
		fieldValues = [global_scale]+animal_parameters
	except (NameError):
		fieldValues=[]
	fieldValues = multenterbox(msg,title, fieldNames,fieldValues)
	    
	while 1:
	      errmsg = ""
	      for i in range(len(fieldNames)):
		try:   
			if i in numerical_id:
				fieldValues[i]=double(fieldValues[i].strip())
			else:
				fieldValues[i]=str(fieldValues[i].strip())
			
		except(ValueError):
			errmsg = errmsg + ('Wrong value of "%s" \n\n' % fieldNames[i])
	      if errmsg == "": break # no problems found
	      fieldValues = multenterbox(errmsg, title, fieldNames, fieldValues)
	return(fieldValues)
	
def in_set(variables,lower_boundes,shift_values):
	outcome=True
	for variable,lower_bond,shift_value in zip(variables,lower_boundes,shift_values):
		if ((variable<lower_bond)|(variable>lower_bond+shift_value)):
			outcome=False
	return (outcome)
        
def change_object(main_object_list,object_number):
	object_changed=main_object_list.pop(object_number)
	try:
		if mode==0: 
			path=path_finder(object_changed.segment_start,object_changed.segment_end)
		if mode==1: 
			try:
				path=dendrite_finder(object_changed.segment_start,object_changed.segment_end)
				smooth_trajectory_dendrite(path)
			except:
				path=object_changed
		main_object_list.append(path)
	except(IndexError):
		print "no object"
	redraw(old_screen_copy)

def shift_zoom(current_event):
			# SHIFT RIGHT:
			 if (current_event.key==275):
				 zoom_shift[0]=zoom_shift[0]+5
				 display_surface_update()
			# SHIFT LEFT:
			 if (current_event.key==276):
				 zoom_shift[0]=zoom_shift[0]-5
				 display_surface_update()
			# SHIFT UP:
			 if (current_event.key==274):
				 zoom_shift[1]=zoom_shift[1]+5
				 display_surface_update()
			# SHIFT DOWN:
			 if (current_event.key==273):
				 zoom_shift[1]=zoom_shift[1]-5
				 display_surface_update()


class stack_reading:
	def __init__(self,stack,channel_info):
		im =Image.open(stack)
		im=im.convert("RGB")
		if channel_info=="get":
			chosen_channel=get_channel_info()
			if chosen_channel!=3:
				channel_info=[chosen_channel,[1,1,1]]
				channel_info[1][channel_info[0]]=0
			else:
				channel_info=None
			
		channels = im.split()
		if channel_info==None:
			max_values=map(lambda x: x.getextrema()[1],channels)
			max_values_index=max_values.index(numpy.max(max_values))
			im = Image.merge("RGB", (channels[max_values_index], channels[max_values_index], channels[max_values_index]))
		
		data = im.tostring()
		self.channel_info=channel_info
		self.data=data
		self.im=im		
def make_animal_description(picture_description,changable_parameters):	
	animal_parameters=[]
	
	for animal_parameter_desc in animal_parameters_names:
				animal_parameter=extract_item(picture_description,animal_parameter_desc)
				if (animal_parameter!=None):
					if (current_record!=None)&(animal_parameter_desc in changable_parameters):
						try:
							animal_parameters.append(current_record[1][current_record[0].index(animal_parameter_desc)])
						except (IndexError,ValueError):
							animal_parameters.append("None")
					else:
						animal_parameters.append(animal_parameter)
					
				else:
					animal_parameters.append("")
	return(animal_parameters)
class get_active_image:
  def __init__(self,data,active_channel,size,channel_info):
	im=Image.fromstring("RGB", size,data)
	channels = im.split()
	other_channels=None
	if channel_info!=None:
			other_channels=[]
			for i in range(3):
				if channel_info[1][i]==1:
					other_channels.append(scipy.misc.fromimage(channels[i],flatten=True))
				else:
					other_channels.append(None)
	print "active_channel",active_channel
	im = Image.merge("RGB", (channels[active_channel], channels[active_channel], channels[active_channel]))
	data = im.tostring()
	self.other_channels=other_channels
	self.data=data
	self.im=scipy.misc.fromimage(im,flatten=True)	
	self.channel_info=channel_info
def get_channel_info():
	output=buttonbox(msg='Choose Active Channel:', title='Spine Magick', choices=('RED','GREEN','BLUE','MONOCHROMATIC'), image=None, root=None)
	return((channel_names+['MONOCHROMATIC']).index(output))

#GLOBAL VARIABLES
global mode
global threshold
global skeleton_drift
global tube_solig_angle_ratio
global counter
global offset_range
global metric_components
global stack
global backup_file
global spine_width
global zoom_window_origin
global zoom_shift
global random_id
global halo_correct
global method
global gradient_offset
global global_scale
global privilige
global animal_parameters
global animal_parameters_names
global turn_spines_off
global mode_dict
global smoothing_degree
global dendrite_width
global manual_renumbering


backup_interval=90
manual_renumbering=globs.renumbering
old_screen_copy=None
gradient_offset=0
mode=0
method=0
halo_correct=0
skeleton_drift=2
threshold=120
segment_point=0
spine_width=30
dendrite_width=spine_width/2
smoothing_degree=4
offset_range=spine_width/2
tube_solig_angle_ratio=1
counter=0


max_x=globs.xsize
max_y=globs.ysize
oversize=False
main_object_list=[]
shift_horizontal=0
shift_vertical=0
zoom_window_origin=[0,0]
zoom_shift=[0,0]
dragging_position=None
max_nr_to_display_individually=100
mode_dict=dict({0: "spines", 1: "dendrite"}) 
update_needed=0
channel_names=['RED','GREEN','BLUE']

#magnification_window_data
magnification_window_size=80
zoom_factor=3
turn_spines_off=0

#channel_info [[active_channel][red_on,g_on,b_on]]
channel_info=None
channel_info=[0,[0,0,0]]
channel_info="get"
extra_channels=None

#NAME OF INITIAL DIRECTORY
initdirpath=globs.configpath+"\\init_dir.dat"
file_name_path=globs.configpath+"\\image_name.dat"
parameterspath=globs.configpath+"\\parameters.dat"
changable_parameters=["Experiment Name","Animal Type","Animal ID","Group ID","Subgroup 1 ID","Subgroup 2 ID","Picture Nr","Brain Region","Dendrite Rank","Notes"]

global_scale=""
try:
	parms_file = open(parameterspath, 'rb')
	animal_parameters= pickle.load(parms_file)
	parms_file.close()
except(IOError):
	animal_parameters=["","Rat_Wistar","1","Control","WT","","1","Hippocampus","Appical",""]
	animal_parameters=map(format_input,animal_parameters)
animal_parameters_names=["Experiment Name","Animal Type","Animal ID","Group ID","Subgroup 1 ID","Subgroup 2 ID","Picture Nr","Brain Region","Dendrite Rank","Notes"]


try:
    parms_file = open(initdirpath, 'rb')
    dir_name= pickle.load(parms_file)
    parms_file.close()
except(IOError,EOFError,KeyError):
    dir_name="c:\\"

root = tk.Tk()
root.withdraw()        
    

#IMAGE OPENING    

#check if file given automatically
parser=OptionParser()
parser.add_option("-f", "--file",dest="filename")
parser.add_option("-i", "--info",dest="info_file")
parser.add_option("-s","--autosave",dest="autosave",action="store_true")
(options,args)=parser.parse_args()
if (options.autosave!=None):
	autosave=True
else:
	autosave=False
	
#check if not crashed	
try:
    image_name_file = open(file_name_path,'rb')
    stack= pickle.load(image_name_file)
    image_name_file.close()
except:
    stack=None

recovery_action=0
if (options.filename!=None):
	stack=str(options.filename)
else:
	if (stack!=None):
		recovery_action=ccbox(msg='Shall I recover the last document ?', title='Auto-Recovery', choices=('Continue', 'Cancel'))
	if recovery_action==0:
		if sys.argv[1:]==[]:
			stack=askfn(initialdir= dir_name,title="Open Image File",filetypes=[('TIFF files', '.tif'),("JPG files" , '.jpg'),('SPINES files', '.cnt')])
		else:
			stack=sys.argv[1]
try:
	image_name_file = open(file_name_path, 'wb')
	pickle.dump(stack,image_name_file,2)
	image_name_file.close()
except:
	pass
if (options.info_file!=None):
	database_info=get_database_info(str(options.info_file))
else:
	database_info=None
stack_extension=os.path.splitext(stack)[1]
pg_mode = "RGB"
#3d image being opened
#image_3d=im_opening_3d(stack)
#arr=multiply(0.5,add(numpy.mean(stack_data,0),numpy.max(stack_data,0)))
#flattening 
#arr=numpy.mean(image_3d.data,0)
#im=scipy.misc.toimage(arr,mode="RGB")
#stack='c:\\biophysics\\kolce_dendrytowe\\test_flat2.jpg'
out_file=stack[:-3]+"cnt"
out_file_csv=stack[:-3]+"csv"
out_picture=stack[:-4]+"_contours.tif"
time_backup=time.time()-backup_interval
backup_file=os.path.split(initdirpath)[0]+"\\backup.cnt"
backup_file=os.path.normpath(backup_file)


#CONVERTING BRIGTEST CHANNEL TO BW OF IMAGE
if ((stack_extension!=".cnt")&(recovery_action==0)):
	data_entered=data_entry()
	global_scale=data_entered[0]
	animal_parameters=data_entered[1:]
	animal_parameters=map(format_input,animal_parameters)
	#zapisywanie parametrow
	try:
	  parms_file = open(parameterspath, 'wb')
	  pickle.dump(animal_parameters,parms_file,2)
	  parms_file.close()
	except:
	  print "Writing error, allow writing permission to",globs.configpath
	
	input_image=stack_reading(stack,channel_info)
	data=input_image.data
	im=input_image.im
	channel_info=input_image.channel_info
	
	random_id=[long(random.random()*1e9),long(random.random()*1e9)]
	picture_description=[]
	#DATA ENTRY
	


else:
	#LOAD CNT FILE
	if (recovery_action==0):
		pkl_file = open(stack, 'rb')
		main_object_list,picture_description= pickle.load(pkl_file)
		pkl_file.close()
		counter=len(main_object_list)
		data=extract_item(picture_description,"image_data")
		channel_info=extract_item(picture_description,"channel_info")
		if (data==None):
			if (autosave==True):
				os._exit(0)
			tkMessageBox.showwarning("Opening Error", "No image appended. Open image first and then load contours (.cnt) file")
			os._exit(0)
		size=extract_item(picture_description,"size")
		im=Image.fromstring("RGB",size,data)
		channel_info=extract_item(picture_description,"channel_info")
	if (recovery_action==1)&(stack[-3:]!="cnt"):
		
		pkl_file = open(backup_file, 'rb')
		main_object_list,picture_description= pickle.load(pkl_file)
		channel_info=extract_item(picture_description,"channel_info")
		
		input_image=stack_reading(stack,channel_info)
		data=input_image.data
		im=input_image.im
		channel_info=input_image.channel_info
		
		print picture_description
		pkl_file.close()
		counter=len(main_object_list)
	if (recovery_action==1)&(stack[-3:]=="cnt"):
		pkl_file = open(stack, 'rb')
		picture_description= pickle.load(pkl_file)[1]
		pkl_file.close()
		pkl_file = open(backup_file, 'rb')
		main_object_list= pickle.load(pkl_file)[0]
		pkl_file.close()
		data=extract_item(picture_description,"image_data")
		channel_info=extract_item(picture_description,"channel_info")
		size=extract_item(picture_description,"size")
		im=Image.fromstring("RGB",size,data)
	global_scale=extract_item(picture_description,"scale")
	id_0,id_1=extract_item(picture_description,"identifier")
	if database_info!=None:
		current_record=get_record(database_info,str(id_0),str(id_1))
	else: 
		current_record=None
	#print extract_item(picture_description,"address")
	#print extract_item(picture_description,"scale")
	animal_parameters=make_animal_description(picture_description,changable_parameters)
	
	random_id=extract_item(picture_description,"identifier")
	print random_id
	if (random_id==None):
		random_id=[long(random.random()*1e9),long(random.random()*1e9)]
	if autosave==True:
		manual_renumbering_stored=extract_item(picture_description,"renumbering")
		if manual_renumbering_stored!=None:
			manual_renumbering=manual_renumbering_stored
		
	if manual_renumbering=="manual":
		counter=max_objectnr(main_object_list)
	
	

picture_description_archived=archive_old_entries(picture_description)
picture_description=[]
size=im.size
aux_structure=ImageStructure(im)
	
icon_y_size=int(40.0*size[1]/size[0])
print size,icon_y_size
metric_components=[global_scale,global_scale]

#channels used to colocalize
colocalizing_channels=[]
if channel_info!=None:
	for ch_nr in range(3):
		if channel_info[1][ch_nr]==0:
			continue
		else:
			colocalizing_channels.append(ch_nr)
			

im = im.filter(GAUSSIAN)
if channel_info==None:
	original_image=scipy.misc.fromimage(im,flatten=True)
	data_to_show=data
	
else:
	active_image=get_active_image(data,channel_info[0],size,channel_info)
	data_to_show=active_image.data
	original_image=active_image.im
	extra_channels=active_image.other_channels
original_image_gradient=scipy.ndimage.laplace(original_image)
#im_out=scipy.misc.toimage(original_image)
display_size=size[:]
oversize=False
oversize_x=False
oversize_y=False
extra_space=magnification_window_size*zoom_factor
magnification_window_size_2=magnification_window_size/2


if ((size[0]>max_x)&(size[1]>max_y)): 
	oversize=True
	oversize_x=True
	oversize_y=True
	display_size=[max_x,max_y]
else:
		if (size[0]>max_x):
			oversize=True
			oversize_x=True
			display_size=[max_x,size[1]]
			
		if (size[1]>max_y): 
			oversize=True
			oversize_y=True
			display_size=[size[0],max_y]
print "sizes:"
print size
print display_size
print oversize,oversize_x,oversize_y
first_tab=display_size[0]/2-magnification_window_size_2*zoom_factor
	


screen=pygame.Surface(size)
display_screen=pygame.display.set_mode([display_size[0],display_size[1]+extra_space])
pygame.init()
picture = pygame.image.fromstring(data_to_show, size, pg_mode)
if oversize==True:
	pic_icon=pygame.transform.smoothscale(picture, (40, icon_y_size))

#screen.blit(picture, (0,0,20,20),disp_rect)

pygame.display.set_caption("Spine Magick!")
pygame.display.flip()


#MAIN LOOP
redraw()
if (autosave==True):
	pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_END}))	

while True:
         time.sleep(0.01)
         current_event=pygame.event.poll()
	 key_pressed=pygame.key.get_pressed()
	 mouse_buttons_state=pygame.mouse.get_pressed()
	 if current_event.type==12:
		 decision=boolbox(msg="Are you sure you want to quit without saving?")
		 if decision==1:
			 pygame.quit()
			 os.remove(file_name_path)
			 os._exit(0)
	 if (current_event.type==KEYDOWN):
		 print current_event.key
		 # RENDER SURFACE
		 #normally renders only not-rendered objects...
		 if (current_event.key==114):
			 if (key_pressed[pygame.K_LSHIFT]):
				render_all(main_object_list,rendering_all=True)
			 else:
				render_all(main_object_list)
			 redraw()
		#CHANGE PARAMETERS
		 if (current_event.key==278):
			if (key_pressed[pygame.K_LSHIFT]):
				data_entered=data_entry()
				global_scale=data_entered[0]
				animal_parameters=data_entered[1:]
				animal_parameters=map(format_input,animal_parameters)
				metric_components=[global_scale,global_scale]
			else:
				set_parameters()
				
				
			redraw()
		#INCREASE/DECREASE SMOOTHING
		 if (mode==1):
			if (key_pressed[pygame.K_RSHIFT]|key_pressed[pygame.K_LSHIFT])!=1:
				# shift +/- changes width
				if (current_event.key==61): 
					smoothing_degree=smoothing_degree+1	
					if (smoothing_degree>10):
						smoothing_degree=10
				if (current_event.key==45): 
					smoothing_degree=smoothing_degree-1
					if (smoothing_degree<1):
						smoothing_degree=1
				change_object(main_object_list,-1)
			if ((current_event.key==61)|(current_event.key==45)):
			
			# shift +/- changes width
				if (key_pressed[pygame.K_RSHIFT]|key_pressed[pygame.K_LSHIFT]): 
					if (current_event.key==61): 
						dendrite_width=dendrite_width+2
						if (dendrite_width>100):
							dendrite_width=100
					if (current_event.key==45): 
						dendrite_width=dendrite_width-2
						if (dendrite_width<4):
							dendrite_width=4
				change_object(main_object_list,-1)

		#INCREASE/DECREASE THRESHOLD
		 if (((current_event.key==61)|(current_event.key==45))&(mode==0)):
			
			# shift +/- changes width
			special_key=0
			if (key_pressed[pygame.K_RSHIFT]|key_pressed[pygame.K_LSHIFT]): 
				if (current_event.key==61): 
					spine_width=spine_width+2
					if (spine_width>100):
						spine_width=100
				if (current_event.key==45): 
					spine_width=spine_width-2
					if (spine_width<10):
						spine_width=10
				offset_range=spine_width/2
				special_key=1
		
			if (key_pressed[pygame.K_RCTRL]|key_pressed[pygame.K_LCTRL]): 
					if (current_event.key==61): 
						halo_correct=halo_correct+0.1
						if (halo_correct>2.5):
							halo_correct=2.5
					if (current_event.key==45): 
						halo_correct=halo_correct-0.1
						if (halo_correct<0):
							halo_correct=0.0
					special_key=1
			if (key_pressed[pygame.K_RALT]|key_pressed[pygame.K_LALT]):
					skeleton_step=0.5
					if skeleton_drift<2.0:
						skeleton_step=0.2
					if skeleton_drift<1.4:
						skeleton_step=0.1
					if (current_event.key==61):
						skeleton_drift=skeleton_drift+skeleton_step
						if (skeleton_drift>5):
							skeleton_drift=5
					if (current_event.key==45): 
						skeleton_drift=skeleton_drift-skeleton_step
						if (skeleton_drift<1):
							skeleton_drift=1
					special_key=1
			if (special_key==0):
				if method==0:
					if (current_event.key==61): 
						threshold=threshold+10
						if (threshold>255):
							threshold=255
					if (current_event.key==45): 
						threshold=threshold-10
						if (threshold<0):
							threshold=0
				else:
				
					if (current_event.key==61): 
						gradient_offset=gradient_offset+1
						if (gradient_offset>10):
							gradient_offset=10
					if (current_event.key==45): 
						gradient_offset=gradient_offset-1
						if (gradient_offset<-10):
							gradient_offset=-10
				
			
			change_object(main_object_list,-1)
		#DELETE OBJECT
		 if (current_event.key==127):
			 delete_object(main_object_list)
			 redraw()
			 old_screen_copy=None
			 segment_point=0
		#DELETE LAST
		 if (current_event.key==8):
			try:
				(main_object_list[-1]).status="deleted"
			except(IndexError):
				print "no object"
			redraw()
			old_screen_copy=None
			segment_point=0
		#REARRANGE NUMBERS
		 if (current_event.key==110):
			 rearrange_numbers(main_object_list,ask_for_manual=manual_renumbering)
			 redraw()
			 old_screen_copy=None
		#MERGE OBJECTS
		 if (current_event.key==109):
			 merge_objects(main_object_list)
			 redraw()
			 old_screen_copy=None
		 if ((oversize==True)&(((key_pressed[pygame.K_RCTRL]|key_pressed[pygame.K_LCTRL]))==False)):
			# SHIFT RIGHT:
			update_needed=0
			if ((current_event.key==275)&(oversize_x==True)):
				 shift_horizontal=shift_horizontal+50
				 update_needed=1
			# SHIFT LEFT:
			if ((current_event.key==276)&(oversize_x==True)):
				 shift_horizontal=shift_horizontal-50
				 update_needed=1
			# SHIFT UP:
			if ((current_event.key==274)&(oversize_y==True)):
				 shift_vertical=shift_vertical+50
				 update_needed=1
			# SHIFT DOWN:
			if ((current_event.key==273)&(oversize_y==True)):
				 shift_vertical=shift_vertical-50
				 update_needed=1
			 
		#SHIFT ZOOM WINDOW:
		 if (key_pressed[pygame.K_LCTRL]|key_pressed[pygame.K_RCTRL]): 
			shift_zoom(current_event)
		#CHANGE MODE
		 if (current_event.key==291):
			 segment_point=0
			 if (mode==0):
				mode=1
			 else:
				mode=0
			 #change_object(main_object_list,-1)
			 display_surface_update()
			 #redraw()	
		#CHANGE METHOD
		 if (current_event.key==9):
			 if (method==0):
				method=1
			 else:
				method=0
			 change_object(main_object_list,-1)
			 display_surface_update()
		 #TURN VISIBILITY OF SPINES
		 if (current_event.key==293):
			 turn_spines_off=turn_spines_off+1
			 turn_spines_off=turn_spines_off%3
			 redraw(turn_last=turn_spines_off)
		
		#LOAD FILE	
		 if (current_event.key==108):

			  file_name=askfn(initialdir=os.path.split(stack)[0],title="LOAD CONTOURS",filetypes=[('CNT files', '.cnt')])
			  pkl_file = open(file_name, 'rb')
			  main_object_list,picture_description_loaded= pickle.load(pkl_file)
			  id_0,id_1=extract_item(picture_description_loaded,"identifier")
			  random_id=extract_item(picture_description_loaded,"identifier")
			  global_scale=extract_item(picture_description_loaded,"scale")
			  metric_components=[global_scale,global_scale]
			  if database_info!=None:
				current_record=get_record(database_info,str(id_0),str(id_1))
			  else: 
				current_record=None
			  animal_parameters=make_animal_description(picture_description_loaded,changable_parameters)
			  pkl_file.close()
			  counter=len(main_object_list)
			  redraw()
		#QUIT GAME	
		
		 if (current_event.key==279):
			 render_all(main_object_list,rendering_all=True)
			 if manual_renumbering=="auto":
				 ask_for_manual="auto"
			 else:
				 ask_for_manual="None"
			 rearrange_numbers(main_object_list,ask_for_manual)
			 redraw()
			 im_string=pygame.image.tostring(screen,"RGB")
			 #picture = pygame.image.fromstring(im_string, size, pg_mode)
			 im_out=Image.fromstring(pg_mode, size, im_string)
			 #im_out=scipy.misc.toimage(im_string)
			 im_out=im_out.convert("RGB")
			 im_out.save(out_picture,format="TIFF")
			 #pygame.image.save(screen, out_picture)
			 pygame.quit()
			 write_file1=open(out_file, "wb")
			 picture_description.append(["spines_nr",count_spines(main_object_list)])
			 picture_description.append(["image_data",data])
			 picture_description.append(["size",size])
			 picture_description.append(["counter",str(counter)])
			 picture_description.append(["scale",global_scale])
			 picture_description.append(["identifier",random_id])
			 picture_description.append(["ip",computer_data().ip])
			 picture_description.append(["user",computer_data().user])
			 picture_description.append(["address",computer_data().address])
			 picture_description.append(["renumbering",manual_renumbering])
			 picture_description.append(["channel_info",channel_info])
			 
			 for animal_parameter,animal_parameter_desc in zip(animal_parameters,animal_parameters_names):
				picture_description.append([animal_parameter_desc,animal_parameter])
			 print "archived"
			 print picture_description_archived
			 print archive_tracking(picture_description,picture_description_archived)
			 picture_description=picture_description+archive_tracking(picture_description,picture_description_archived)
			 print "description"
			 for item in picture_description:
				 if item[0]!='image_data':
					 print item
			 pickle.dump([main_object_list,picture_description],write_file1,2)
			 write_file1.close()
			 #do not save parameters in auto mode
			 if autosave==False:
				 try:
					 parms_file = open(initdirpath, 'wb')
					 pickle.dump(os.path.split(stack)[0],parms_file,2)
					 parms_file.close()
				 except(IOError):
					 print "CAN NOT SAVE CONFIGURATION FILE"

			 # MEASURE EVERYTHING
			 total_dendrite_length=0
			 for path in main_object_list:
				 object_measurements(path,aux_structure)
				 print path.status
				 if (path.status=="dendrite"):
					print extract_item(path.parameters,"length") 
					try:
						dendrite_length=double(extract_item(path.parameters,"length"))
						total_dendrite_length=total_dendrite_length+dendrite_length
					except:
						pass
			 picture_description.append(["marked_dendrite_length",total_dendrite_length])
			 parameters_dumper(main_object_list,out_file_csv)
			 try:
				 os.remove(file_name_path)
			 except:
				 pass
			 os._exit(0)
	 
         if (current_event.type==MOUSEBUTTONDOWN):
                 if (current_event.button==3):
			dragging_position=current_event.pos
			#remeber pagging beginning
                 if (current_event.button==1):
				 # process click if outside area
				 current_click=add(current_event.pos,[shift_horizontal,shift_vertical])
				 
				 if (current_event.pos[1]>display_size[1]):
					
					if in_set(current_event.pos,[first_tab,display_size[1]],[magnification_window_size*zoom_factor,magnification_window_size*zoom_factor]):
						click_pos=add(zoom_window_origin,multiply(1.0/zoom_factor,subtract(current_event.pos,[first_tab,display_size[1]])))

						key_pressed=pygame.key.get_pressed()
						if (key_pressed[pygame.K_RALT]|key_pressed[pygame.K_LALT]|(segment_point==1)):
							current_click=click_pos[:]
							
						else:
							if (key_pressed[pygame.K_RSHIFT]|key_pressed[pygame.K_LSHIFT]): 
								(main_object_list[-1]).segment_end=click_pos
							else:
								(main_object_list[-1]).segment_start=click_pos
							change_object(main_object_list,-1)
							continue
					else:
						continue
				 print current_click
                                 if (segment_point==0):
                                         segment_point=1
                                         segment_start=current_click
                                         pygame.draw.circle(screen, pygame.Color("blue"), segment_start, 2, 1)
					 display_surface_update()
                                 else:
                                         segment_point=0
                                         segment_end=current_click
                                         counter=counter+1
					 zoom_shift=[0,0]
                                         


                                         try: 
						if mode==1:
							
							try:   
								path=dendrite_finder(segment_start,segment_end)
								smooth_trajectory_dendrite(path)
							except(MemoryError):
								path=None
						if mode==0:
							path=path_finder(segment_start,segment_end)
						if path!=None:
							main_object_list.append(path)
						if turn_spines_off!=2:
							old_screen_copy=screen.copy()
						
						redraw()
					 except(IndexError):
						 print "no point"
					 turn_spines_off=0
					 display_surface_update()
	 #screen pagging	
	 if ((mouse_buttons_state[2]==1)&(dragging_position!=None)):
		 mouse_current_position=pygame.mouse.get_pos()
		 mouse_shift=subtract(mouse_current_position,dragging_position)
		 dragging_position=mouse_current_position[:]
		 shift_horizontal=shift_horizontal-mouse_shift[0]
		 shift_vertical=shift_vertical-mouse_shift[1]
		 update_needed=1
	 if update_needed==1:
				 update_needed=0
				 if (shift_vertical>size[1]-max_y): shift_vertical=size[1]-max_y
				 if (shift_horizontal>size[0]-max_x): shift_horizontal=size[0]-max_x
				 if (shift_horizontal<0): shift_horizontal=0
				 if (shift_vertical<0): shift_vertical=0
				 display_surface_update()
				 time.sleep(0.1)
	 #BACKUPING
	 #print time.time()-time_backup
	 if ((time.time()-time_backup)>backup_interval):
		 time_backup=time.time()
		 print "BACKUPING"
		 try:
			 parms_file = open(backup_file, 'wb')
			 picture_description_temp=[]
			 picture_description_temp.append(["channel_info",channel_info])
			 for animal_parameter,animal_parameter_desc in zip(animal_parameters,animal_parameters_names):
				picture_description_temp.append([animal_parameter_desc,animal_parameter])
			 pickle.dump([main_object_list,picture_description+picture_description_temp+[["scale",global_scale]]+[["identifier",random_id]]],parms_file,2)
			 parms_file.close()
		 except(IOError,TypeError):
			 print "CAN NOT SAVE CONFIGURATION FILE: ",backup_file