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
#Distance entre le symbole croche et l'extrémité de la barre verticale
dist_croche_barre = 5
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

#Détermine si la note noire est bien à une position "logique" par rapport à la barre verticale
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

#On associe les notes et les barres verticales qui s'interceptent
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
	
def liste_notes(liste):
	somme = 0
	l = []
	if len(liste) > 4:
		for i in range(3,len(liste)):
			somme = somme + liste[i]
			l.extend(liste[:3])
			l.append(somme/(len(liste)-3))
	elif len(liste) == 3:
		l = liste
		l.append(0)
	else:
		l = liste
	return l

def liste_listes_note(liste):
	l = []
	for elt in liste:
		l.append(liste_notes(elt))
	return l

#--------------------------------------------------------------
#Croches
	
def enleve_notes(img,liste):
	for elt in liste:
		(i,j) = elt
		#on retire les noires précédemment sélectionnées en les mettant en "blanc - fond"
		img[i][j] = 1
	return img
			
def recupere_points(img):
	l = []
	for i in range(img.shape[0]):
		for j in range(img.shape[1]):
			#on récupère les pixels noirs
			if img[i][j] != 1 or img[i][j] == False:
				#plt.plot(j,i,'ro')
				l.append((i,j))
	return l

#Détermine si la croche est bien à une position "logique" par rapport à la barre verticale
def existe_croche(i,croche,j,ecart,place,numero_croche):
	rep = 0
	e2 = int(round(ecart/2))
	if abs(i - croche) <= numero_croche*dist_croche_barre:
		rep = 1
		if place == 'b':
			p = plt2.Rectangle((j-e2,i-e2-(numero_croche-1)*ecart),e2,e2,color='b')
			plt2.gcf().gca().add_artist(p)
		else:
			p = plt2.Rectangle((j,i+ecart*(numero_croche-1)),e2,e2,color='b')
			plt2.gcf().gca().add_artist(p)
	return rep

#Determine d'éventuels autres symboles croche
def existe_plus_croche(i,croche,j,ecart,place):
	rep = 0
	e2 = int(round(ecart/2))
	e3 = int(round(ecart/3))
	if (abs(i - croche) > 2*e3) and (abs(i - croche) <= 3*e3):
		rep = 1
		if place == 'b':
			p = plt2.Rectangle((j-e2,i-ecart-e2),e2,e2,color='b')
			plt2.gcf().gca().add_artist(p)
		else:
			p = plt2.Rectangle((j,i+ecart),e2,e2,color='b')
			plt2.gcf().gca().add_artist(p)
	return rep

			
def bv_collee_croche(bv,croche,ecart,img,numer):
	e2 = int(round(ecart/2))
	for elt in bv:
		for elt2 in croche:
			if (elt[2] == elt2[1]) and (elt2[0] < elt[1]) and (elt2[0] > elt[0]):
				if (abs(elt[1] - elt2[0]) <= ecart) or (abs(elt[0] - elt2[0]) <= ecart):
					img[elt2[0]][elt[2]] = 1
					
				if (elt[3] != 0) and (len(elt) < 5):
					bas = existe_croche(elt[1],elt2[0],elt[2],ecart,'b',numer)
					haut = existe_croche(elt[0],elt2[0],elt[2],ecart,'h',numer)
					if bas !=0:
						elt.append(0) #0 = bas
					elif haut != 0:
						elt.append(1) #1 = haut
						
	#on renvoie la liste des barres verticales augmentées
	return (bv,img)


def bv_collee_croche2(bv,croche,ecart,img,numer):
	e2 = int(round(ecart/2))
	for elt in bv:
		for elt2 in croche:
			if (elt[2] == elt2[1]) and (elt2[0] < elt[1]) and (elt2[0] > elt[0]):
				if (abs(elt[1] - elt2[0]) <= ecart) or (abs(elt[0] - elt2[0]) <= ecart):
					img[elt2[0]][elt[2]] = 1
					
				if (elt[3] != 0) and (len(elt) ==5) and (elt[4] < 2):
					#si on a trouvé une croche en bas
					if elt[4] == 0:
						bas = existe_croche(elt[1],elt2[0],elt[2],ecart,'b',numer)
						if bas !=0:
							elt[4] = 2 + elt[4]
					#si on a trouvé une croche en haut
					if elt[4] == 1:
						haut = existe_croche(elt[0],elt2[0],elt[2],ecart,'h',numer)
						if haut != 0:
							elt[4] = 1 + elt[4]
						
	#on renvoie la liste des barres verticales augmentées
	return (bv,img)


def bv_collee_double_croche(bv,croche,ecart): #,img):
	for elt in bv:
		for elt2 in croche:
			if (elt[2] == elt2[1]) and (elt2[0] < elt[1]) and (elt2[0] > elt[0]):
				#if (abs(elt[1] - elt2[0]) <= ecart) or (abs(elt[0] - elt2[0]) <= ecart):
					#img[elt2[0]][elt[2]] = 1
					
				if (elt[3] != 0) and (len(elt) == 5):
					bas = existe_plus_croche(elt[1],elt2[0],elt[2],ecart,'b')
					haut = existe_plus_croche(elt[0],elt2[0],elt[2],ecart,'h')
					if bas !=0:
						elt[4] = elt[4]+1
					elif haut != 0:
						elt[4] = elt[4]+1
	#on renvoie la liste des barres verticales augmentées
	return bv #(bv,img)
