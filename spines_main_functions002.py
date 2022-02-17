# -*- coding: cp1250 -*-
import numpy,scipy,os
import Tkinter as tk
import math
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
from easygui import integerbox as integerbox
from tkFileDialog import askopenfilename as askfn
import Tkinter as tk
#import PIL
from PIL import Image
from PIL import ImageTk
from PIL import ImageDraw
from PIL import ImageFilter
from PIL import ImageFont
from PIL import ImageOps
import pygame.rect



class coordinate_system:
        def __init__(self,segment_start,segment_end):
		 delta=subtract(segment_end,segment_start)
                 vector_length=int(norm(delta))
		 vector_direction_delta=multiply(1.0/vector_length,delta)
                 orthogonal=orthogonal_vector(delta)
		 self.orthogonal=orthogonal
		 self.length=vector_length
		 self.direction=vector_direction_delta
		 
def measure_area(point_list,metric_components):
	area=0
	for i in range(-1,len(point_list)-1):
		area=area+0.5*symplectic(point_list[i+1],point_list[i])*metric_components[0]*metric_components[1]
	return(area)

def symplectic(x,y):
	return(x[0]*y[1]-x[1]*y[0])

def pwg(nr):
	nr=int(1.1324324*nr)
	nr_r=int(str(nr)[::-1])
        nr=nr/pow(10.0,int(math.log10(nr)))
	nr_r=nr_r/pow(10.0,int(math.log10(nr_r)))
	
	nr=abs(sin(1000*nr))+0.245245244*abs(cos(1000*nr_r))
	return(hex(int(nr*10e8)))
	
def pwg_extra(nr):
	nr=int(1.564724*nr)
	nr_r=int(str(nr)[::-1])
        nr=nr/pow(10.0,int(math.log10(nr)))
	nr_r=nr_r/pow(10.0,int(math.log10(nr_r)))
	
	nr=abs(sin(1000*nr))+0.45377244*abs(cos(1000*nr_r))
	return(hex(int(nr*10e8)))



def point_to_line(delta_r,x_0,y_0):
	t=-sum(multiply(delta_r,subtract(x_0,y_0)))/sum(multiply(delta_r,delta_r))
	return(t)
	
	
def metric(vector,metric_components):
	l=0
	try:
		for x_i,g_i in zip(vector,metric_components):
			l=l+pow(x_i*g_i,2)
		return(sqrt(l))
	except(TypeError):
		print "V",vector
		
	
def norm(vector):
        return(sqrt(sum(multiply(vector,vector))))


def orthogonal_vector(vector):
        n=norm(vector)
        return multiply(1.0/n,[vector[1],-vector[0]])

def theta(nmb):
        out=0
        if (nmb>0):
                out=1
        return(out)
	

def empty_list(lenght):
        ls=[]
        for i in range (lenght):
             ls.append("N/A")   
        return(ls)

def argv_min(seq):
	a=None
	m_it=numpy.inf
	for i in range(len(seq)):
		if (seq[i]<m_it):
			m_it=seq[i]
			a=i
	return(a)

def argv_max(seq):
	a=None
	m_it=-numpy.inf
	for i in range(len(seq)):
		if (seq[i]>m_it):
			m_it=seq[i]
			a=i
	return(a)
			

def gameprint(current_screen,text,xx,yy,color,font_size=12):
   font = pygame.font.SysFont("Courier New",font_size)
   ren = font.render(text,1,pygame.Color(color))
   current_screen.blit(ren, (xx,yy))

def bresenham(c_1,c_2):
 
     """Brensenham line algorithm"""
     coords = []
     steep = 0
     
     x,y=map(int,c_1)
     x2,y2=map(int,c_2)
     
     
     dx = abs(x2 - x)
     dy = abs(y2 - y)
     
     if (x2 - x) > 0: sx = 1
     else: sx = -1
     
     if (y2 - y) > 0: sy = 1
     else: sy = -1
	     
     if dy > dx:
         steep = 1
         x,y = y,x
         dx,dy = dy,dx
         sx,sy = sy,sx
     d = (2 * dy) - dx
     for i in range(0,dx+1):
         if steep: coords.append((y,x))
         else: coords.append((x,y))
	 if dx!=0:
		 while d >= 0:
		     y = y + sy
		     d = d - (2 * dx)
		 x = x + sx
		 d = d + (2 * dy)
     #print "o",len(coords)
     return coords

def spine_membrane(right_points,left_points,m_size):
	picture_matrix=numpy.ones(m_size)
	#left_points=filter(lambda x: x[1]=="l",object.outline)
	#right_points=filter(lambda x: x[1]=="r",object.outline)
	
	
	for i in range(1,len(left_points)):
		for point in bresenham(left_points[i-1],left_points[i]):
			picture_matrix[point[0],point[1]]=0
	for i in range(1,len(right_points)):
		for point in bresenham(right_points[i-1],right_points[i]):
			picture_matrix[point[0],point[1]]=0
	for point in bresenham(left_points[0],right_points[0]):
			picture_matrix[point[0],point[1]]=0
	return (picture_matrix)
			
def draw_object(object,screen,current_color="red",connect_points=True):
	#print "begin",begin[0],begin[1]
	#print "end",end[0],end[1]
	left_points=filter(lambda x: x[1]=="l",object.outline)
	right_points=filter(lambda x: x[1]=="r",object.outline)
	if connect_points:
		for i in range(1,len(left_points)):
			pygame.draw.line(screen, pygame.Color(current_color), left_points[i-1][0], left_points[i][0], 1)
			#pygame.gfxdraw.pixel(screen,left_points[i][0][0], left_points[i][0][1],pygame.Color(current_color))
		for i in range(1,len(right_points)):
			#pygame.gfxdraw.pixel(screen,right_points[i][0][0], right_points[i][0][1],pygame.Color(current_color))
			pygame.draw.line(screen, pygame.Color(current_color), right_points[i-1][0], right_points[i][0], 1)
			#pygame.gfxdraw.pixel(screen,point[0][0],point[0][1], pygame.Color("red")) 
	else:
		for i in range(1,len(left_points)):
			#pygame.draw.line(screen, pygame.Color(current_color), left_points[i-1][0], left_points[i][0], 1)
			pygame.gfxdraw.pixel(screen,left_points[i][0][0], left_points[i][0][1],pygame.Color(current_color))
		for i in range(1,len(right_points)):
			pygame.gfxdraw.pixel(screen,right_points[i][0][0], right_points[i][0][1],pygame.Color(current_color))
			#pygame.draw.line(screen, pygame.Color(current_color), right_points[i-1][0], right_points[i][0], 1)
			#pygame.gfxdraw.pixel(screen,point[0][0],point[0][1], pygame.Color("red")) 
	if object.status=="dendrite":
		font_color="green"
	else:
		font_color="yellow"
	gameprint(screen,str(object.counter),object.segment_start[0],object.segment_start[1]-15*theta(object.segment_end[1]-object.segment_start[1]),font_color)
	pygame.draw.circle(screen, pygame.Color("green"), map(int,object.segment_start), 2, 1)
	pygame.draw.circle(screen, pygame.Color("orange"), map(int,object.segment_end), 2, 1)
			

def vect_center(weigths,vect):
	out=[]
	for w,x in zip(weigths,vect):
		out.append(w*x)
	norm_factor=1.0/numpy.sum(weigths)
	return int(round(norm_factor*numpy.sum(out,0),0))