#!/usr/bin/python
# -*- coding: Utf-8 -*

"""Module notes_amas"""

#----------------------------------------------------------
# Importation des librairies

import numpy as np
from matplotlib import pylab as plt
import matplotlib.pyplot as plt2
from math import *

#----------------------------------------------------------
# Variables globales empiriques

#Nombre maximal de croches sur une même note
nbr_croches = 2

#----------------------------------------------------------
# Fonctions

#on retire les portées de l'image
def enleve_portees(img,soluce):
	for x in range(img.shape[0]):
		for y in range(img.shape[1]):
			if round(y*soluce[0]+soluce[1]) == round(x):
				img[x][y] = 1
				img[x-1][y] = 1
				img[x+1][y] = 1 #peu précis mais imprécision des droites détectées oblige	
	return img

def enleve_portees_liste(img,liste):
	img1 = np.zeros(img.shape,np.int)
	img2 = np.zeros(img.shape,np.int)
	for elt in liste:
		img1 = enleve_portees(img,elt)
		img2 = union(img2,img1)
	return img2

#Dessine un structurant adapté pour l'ouverture en tout ou rien
def cree_structurant(rayon):
	h = int(3 + 4*rayon)
	l = int(7 + 2*rayon)
	a = np.zeros((h,l),int)
	#2 : indifférent, blanc ou noir
	for x in range(h):
		for y in range(l):
			a[x][y] = 2
	
	#1: points blancs
	"""for y in range(1+rayon):
		a[0][y] = 1	
		a[a.shape[0]-1][a.shape[1]-1-y] = 1"""
	"""for x in range(rayon):
		a[x][0] = 1	
		a[a.shape[0]-1-x][a.shape[1]-1] = 1"""
	for x in range(h):
		a[x][0] = 1
		a[x][l-1] = 1
	
	#0: points noirs
	for x in range(1+rayon,a.shape[0]-(1+rayon)):
		for y in range(a.shape[1]):
			a[x][a.shape[1]/2] = 0
	for x in range(1+rayon,a.shape[0]/2+1):
		for y in range(a.shape[1]/2-(x-(1+rayon)),1+a.shape[1]/2+(x-(1+rayon))):
			a[x][y] = 0
			a[a.shape[0]-x-1][y] = 0
	return a	

#détermine s'il y a une note à proximité de /collées à la barre verticale
def existe_note(img,ecart,i,j,seuil,coul):
	somme = 0
	rep = False
	ecart = int(round(ecart))
	for x in range(i-ecart,i):
		for y in range(j-ecart,j):
			if x < img.shape[0] and y < img.shape[1]:
				if img[x][y] == 0:
					somme = 1 + somme
				#plt.plot([j-ecart,j,j,j-ecart,j-ecart],[i-ecart-1,i-ecart-1,i-1,i-1,i-ecart-1])
	#si on remplit plus de 20% du carré "en bas"
	if somme*100 >= seuil*ecart*ecart:
		c1 = plt2.Circle(((2*j-ecart)/2,i),3*e/2,color=coul)
		plt2.gcf().gca().add_artist(c1)
		rep = True
	else:
		somme = 0
		for x in range(i-ecart,i):
			for y in range(j,j+ecart):
				if x < img.shape[0] and y < img.shape[1]:
					if img[x][y] == 0:
						somme = 1 + somme
					#plt.plot([j,j+ecart,j+ecart,j,j],[i-ecart+1,i-ecart+1,i+1,i+1,i-ecart+1])
		#si on remplit plus de 20% du carré "en haut"
		if somme*100 >= seuil*ecart*ecart:
			c1 = plt2.Circle(((2*j+ecart)/2,i),3*e/2,color=coul)
			plt2.gcf().gca().add_artist(c1)
			rep = True
	return rep

#pour chaque barre verticale identifiée, on regarde si c'est une note de musique
def existe_noire_img(img,liste,ecart,pc_note):
	for elt in liste:
		elt.append(existe_note(img,ecart,elt[1],elt[2],pc_note,'g'))
		elt.append(existe_note(img,ecart,elt[0],elt[2],pc_note,'g'))
	return liste

#identifie une éventuelle croche en haut d'une barre verticale
def existe_croche_haut(img,ecart,i,j,pc_cro):
	somme = 0
	rep = 0
	ecart = int(round(ecart))
	e2 = int(round(ecart/2))
	for x in range(i,i+e2):
		for y in range(j-e2,j):
			if x < img.shape[0] and y < img.shape[1]:
				if img[x][y] == 0:
					somme = 1 + somme
	if somme*100 >= pc_cro*e2*e2:
		p = plt2.Rectangle((j,i),e2,e2,color='b')
		plt2.gcf().gca().add_artist(p)
		rep = 1
	else:
		somme = 0
		for x in range(i,i+e2):
			for y in range(j,j+e2):
				if x < img.shape[0] and y < img.shape[1]:
					if img[x][y] == 0:
						somme = 1 + somme
		if somme*100 >= pc_cro*e2*e2:
			p = plt2.Rectangle((j,i),e2,e2,color='b')
			plt2.gcf().gca().add_artist(p)
			rep = 1
	return rep

#identifie une éventuelle croche en bas d'une barre verticale
def existe_croche_bas(img,ecart,i,j,pc_cro):
	somme = 0
	rep = 0
	ecart = int(round(ecart))
	e2 = int(round(ecart/2))
	for x in range(i-e2,i):
		for y in range(j-e2,j):
			if x < img.shape[0] and y < img.shape[1]:
				if img[x][y] == 0:
					somme = 1 + somme
	if somme*100 >= pc_cro*e2*e2:
		p = plt2.Rectangle((j-e2,i-e2),e2,e2,color='b')
		plt2.gcf().gca().add_artist(p)
		rep = 1
	else:
		somme = 0
		for x in range(i-e2,i):
			for y in range(j,j+e2):
				if x < img.shape[0] and y < img.shape[1]:
					if img[x][y] == 0:
						somme = 1 + somme
		if somme*100 >= pc_cro*e2*e2:
			p = plt2.Rectangle((j-e2,i-e2),e2,e2,color='b')
			plt2.gcf().gca().add_artist(p)
			rep = 1
	return rep

#jusqu'à nbr_croches croches
def existe_autre_croche(img,liste,ecart,pc_cro):
	ecart = int(round(ecart))
	for elt in liste:
		if len(elt) > 5:
			if elt[5] != 0:
				for i in range(1,nbr_croches):
					elt[5] = (existe_croche_haut(img,ecart,elt[0]+i*ecart,elt[2],pc_cro) or existe_croche_bas(img,ecart,elt[1]-i*ecart,elt[2],pc_cro)) + elt[5]
	return liste

#détermine suivant les résultats de l'existence de notes, l'existence de croches, de blanches ou de barres de mesure
def existe_croche_blanche_mesure(img,img2,liste,ecart,pc_cro,pc_blan):
	for elt in liste:
		#Si on a une noire en haut ou (exclusif) en bas
		if (not(elt[3]) and elt[4]) or (elt[3] and not(elt[4])):
			if elt[3]:
				elt.append(existe_croche_haut(img,ecart,elt[0],elt[2],pc_cro))
			else:
				elt.append(existe_croche_bas(img,ecart,elt[1],elt[2],pc_cro))
			#on regarde s'il y a d'autres croches
			liste = existe_autre_croche(img,liste,ecart,pc_cro)
			elt.extend([False,False])
			
		#s'il n'y a pas de noire
		elif (not(elt[3]) and not(elt[4])):
			#on met le nombre de croches à zéro
			elt.append(0)
			elt.append(existe_note(img2,ecart,elt[1],elt[2],pc_blan,'magenta'))
			elt.append(existe_note(img2,ecart,elt[0],elt[2],pc_blan,'magenta'))
			
			#c'est une barre de mesure (ni noire, ni blanche)
			if (not(elt[6]) and not(elt[7])):
				#elt.extend('m')
				x = [elt[2],elt[2]]
				y = [elt[0],elt[1]]
				plt.plot(x,y,'b')
	return liste

def max_matrice(img):
	m=0
	for i in range(img.shape[0]):
		for j in range(img.shape[1]):
			if img[i][j] > m:
				m = img[i][j]
	return m
