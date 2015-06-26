#!/usr/bin/python
# -*- coding: Utf-8 -*

"""
	Module reconnaissance de le clef
"""

#----------------------------------------------------------
# Importation des librairies

import cv2
import sys
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.pyplot as plt2
import warnings
from math import *
#from skimage import data
#from skimage.feature import match_template


#----------------------------------------------------------
# Fonctions

"""
	A partir d'une image en argument
	on la découpe en autant de partie que de portées
"""
def decoupe_images_en_portees(tab,img):
	l = []
	p = []
	
	#si on a qu'une portée, on ne découpe pas
	if len(tab[0]) == 1:
		p.append(img.shape[0])
	else:
		for i in range(len(tab[0])-1):
			#ordonnées des lignes de découpe entre les portées
			p.append((tab[4][i] + tab[0][i+1])/2)
	
	for j in range(len(p)+1):
		if j == 0:
			h = 0
			b = p[j]
		elif j == len(p):
			b = img.shape[0]
			h = p[j-1]
		else:
			b = p[j]
			h = p[j-1]
		
		#on crée une image de la largeur voulue et de longueur identique à celle de l'image d'origine
		if b-h < 0:
			print "mauvaise détection des portées"
			sys.exit(1)
		img2 = np.zeros((b-h,img.shape[1]),np.uint8)
		for x in range(img2.shape[0]):
			for y in range(img2.shape[1]):
				img2[x][y] = img[x+h][y]
		l.append(img2)
	return l

"""
	A partir de la liste des barres verticales
	on détermine la plus petite abscisse d'une barre verticale
	affublée d'une note
"""
def ab_premiere_note(bv,img):
	mini = img.shape[1]
	for elt in bv:
		if elt[3] != 0 and elt[3] < mini:
			mini = elt[3]
		elif elt[5] != 0 and elt[5] < mini:
			mini = elt[5]
	return mini

"""
	On redimensionne les images de clefs
	pour les adapter à la partition
	à l'aide de l'écart moyen entre les portées
"""
def redimensionne_img(ecart,imgf,imgs,imgu):
	h = int(round(4*ecart))
	h2 = int(round(7*ecart))
	bf = int(round(45*h/63))
	bs = int(round(43*h2/103))
	bu = int(round(69*h/106))
	template_fa = cv2.resize(imgf,(bf,h))
	template_sol = cv2.resize(imgs,(bs,h2))
	template_ut = cv2.resize(imgu,(bu,h))
	return (template_fa,template_sol,template_ut)

"""
	On cherche une unique occurence de la clef
	à l'aide du template en argument
"""
def cherche_clef(img,temp,tab,dist):
	rep = 0
	ab = 0
	w,h = temp.shape[::-1]
	res = cv2.matchTemplate(img,temp,cv2.TM_CCOEFF_NORMED)
	min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
	
	#les clefs sont en début de partition
	if (max_loc[0] < dist):
		cv2.rectangle(img, max_loc, (max_loc[0] + w, max_loc[1] + h), 0, 2)
		rep = 1
		ab = max_loc[0]
	#on renvoie l'existence de la clef et son abscisse
	return ab,rep

"""
	A partir des templates des trois clefs étudiées
	on cherche celle qui est représentée dans l'image
"""
def cherche_bonne_clef(img,sol,fa,ut,tab,dist):
	rep = ''
	ab = 0
	
	#on cherche la clef de sol, si on ne trouve pas, on cherche la clef de fa, si on ne trouve pas, on cherche la clef d'ut
	ab_s,if_sol = cherche_clef(img,sol,tab,dist)
	if if_sol == 0:
		ab_f,if_fa = cherche_clef(img,fa,tab,dist)
		if if_fa == 0:
			ab_u,if_ut = cherche_clef(img,ut,tab,dist)
			if if_ut == 0:
				print "mauvaise détection de la clef"
				sys.exit(1)
			else:
				rep = 'ut'
				ab = ab_u
		else:
			rep = 'fa'
			ab = ab_f
	else:
		rep = 'sol'
		ab = ab_s
	
	print rep,ab
	#on renvoie le type de la clef et son abscisse
	return rep,ab
	
	
"""
#avec skimage
def cherche_clef(img,temp,tab):
	rep = 0
	w,h = temp.shape[::-1]
	
	result = match_template(img, temp)
	ij = np.unravel_index(np.argmax(result), result.shape)
	x, y = ij[::-1]
	
	if (x < img.shape[1]/7) and (verifie_pertinence_clef(tab,y,y+h) == 1):
		rep = 1
	return rep

#inutile à ce jour
#on cherche plusieurs occurences de la clef
def cherche_clef2(img,temp,tab):
	rep = 0
	w,h = temp.shape[::-1]
	res = cv2.matchTemplate(img,temp,cv2.TM_CCOEFF_NORMED)
	threshold = 0.6 #ce n'est pas un minimum mais plusieurs au-dessus d'un certain seuil, comment le déterminer ?
	loc = np.where(res >= threshold)
	for pt in zip(*loc[::-1]):
		if pt[0] < img.shape[0]/7 and (verifie_pertinence_clef(tab,pt[1],pt[1]+h) == 1):
			cv2.rectangle(img, pt, (pt[0] + w, pt[1] + h),0, 2)
			rep = 1
	return img,rep
"""
