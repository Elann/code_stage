#!/usr/bin/python
# -*- coding: Utf-8 -*

"""Module notes_compacite"""

#----------------------------------------------------------
# Importation des librairies

import numpy as np
from matplotlib import pylab as plt
import matplotlib.pyplot as plt2
from math import *

from fonctions_annexes import *


#----------------------------------------------------------
# Variables globales empiriques

#Valeur minimale du critère de compacité acceptée
seuil_comp = 0.7
#Distance entre la note et l'extrémité de la barre verticale
dist_note_barre = 5
#Aire minimale acceptée pour être une noire
aire = 70

#----------------------------------------------------------
# Fonctions

def calcule_aires(img):
	a = np.zeros((2,max_matrice(img)+1),np.int)
	for i in range(img.shape[0]):
		for j in range(img.shape[1]):
			if img[i][j] != 0:
				co = img[i][j]
				a[0][co] = a[0][co] + 1
	for i in range(a.shape[1]):
		if a[0][i] < aire:
			a[0][i] = 0
	return a

def calcule_perimetres(img,tab):
	for i in range(img.shape[0]):
		for j in range(img.shape[1]):
			if img[i][j] != 0:
				if img[i][j] != img[i-1][j] or img[i][j] != img[i][j-1] or img[i][j] != img[i+1][j] or img[i][j] != img[i][j+1]:
					co = img[i][j]
					tab[1][co] = tab[1][co] + 1
	for i in range(tab.shape[1]):
		tab[0][i] = max(tab[0][i]-tab[1][i],0)
	return tab

def calcule_compacite(tab):
	pi = 4*atan(1)
	a = np.zeros(tab.shape[1],np.float)
	for i in range(len(a)):
		if tab[1][i] != 0:
			a[i] = (4*pi*tab[0][i])/(tab[1][i]*tab[1][i])
	return a

def colorie_bons(img,tab):
	l = []
	for i in range(img.shape[0]):
		for j in range(img.shape[1]):
			co = img[i][j]
			if tab[co] > seuil_comp:
				img[i][j] = 255
				l.append((i,j))
				#plt.plot(j,i,'ro')
	return (l,img)

def extrait_pixels(liste):
	l = []
	for elt in liste:
		for i in range(elt[0],elt[1]+1):
			l.append((i,elt[2]))
	return l

def existe_noire(i,note,j,ecart,place):
	rep = 0
	if abs(i - note) <= dist_note_barre:
		rep = i
		if place == 'b':
			c2 = plt2.Circle(((2*j-ecart)/2,i),3*ecart/4,color='red')
			plt2.gcf().gca().add_artist(c2)
		else:
			c2 = plt2.Circle(((2*j+ecart)/2,i),3*ecart/4,color='red')
			plt2.gcf().gca().add_artist(c2)
	return rep
	
def bv_collee_notes(bv,note,ecart):
	for elt in bv:
		for elt2 in note:
			if (elt[2] == elt2[1]) and (elt2[0] < elt[1]) and (elt2[0] > elt[0]):
				if len(elt) < 4:
					bas = existe_noire(elt[1],elt2[0],elt[2],ecart,'b')
					haut = existe_noire(elt[0],elt2[0],elt[2],ecart,'h')
					if bas !=0:
						elt.append(bas)
					elif haut != 0:
						elt.append(haut)
	return bv
	

"""
#Comparaison brutale, à voir pour faire mieux
def bv_collee_notes(bv,note):
	l = []
	for elt in bv:
		for elt2 in note:
			if elt == elt2: #or (elt[0]-1 == elt2[0]) or (elt[0]+1 == elt2[0]):
				l.append(elt)
				#plt.plot(elt[1],elt[0],'ro')
	return l

def suppr_points_inutiles(liste):
	l2 = []
	l3 = []
	l = sorted(liste,key=lambda colonnes: colonnes[0])
	for i in range(1,len(l)):
		if (l[i-1][1] <= l[i][1]+1) and (l[i-1][1] >= l[i][1]-1) and (l[i-1][0] <= l[i][0]+5) and (l[i-1][0] >= l[i][0]-5):
			continue
		else:
			l2.append(l[i])
	if (l[0][1] > l2[0][1]+1) or (l[0][1] < l2[0][1]-1) or (l[0][0] > l2[0][0]+5) or (l[0][0] < l2[0][0]-5):
		l2.append(l[0])
	
	g = sorted(l2,key=lambda colonnes: colonnes[1])
	for i in range(1,len(g)):
		if (g[i-1][1] <= g[i][1]+1) and (g[i-1][1] >= g[i][1]-1) and (g[i-1][0] <= g[i][0]+5) and (g[i-1][0] >= g[i][0]-5):
			continue
		else:
			l3.append(g[i])
	if (g[0][1] > l3[0][1]+1) or (g[0][1] < l3[0][1]-1) or (g[0][0] > l3[0][0]+5) or (g[0][0] < l3[0][0]-5):
		l3.append(g[0])
		
	return l3"""
