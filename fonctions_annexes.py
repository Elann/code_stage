#!/usr/bin/python
# -*- coding: Utf-8 -*

"""
	Module portees_chgt_repere
"""

#----------------------------------------------------------
# Importation des librairies

import numpy as np
from matplotlib import pylab as plt

#----------------------------------------------------------
# Fonctions

"""
	Binarise l'image en paramètre
	avec un seuil donné
"""
def img_0_1(img):
	for x in range(img.shape[0]):
		for y in range(img.shape[1]):
			if img[x][y] > seuil_noir:
				img[x][y] = 1
			else:
				img[x][y] = 0

"""
	Transforme l'image de booléens en paramètre
	en une image (binaire) d'entiers : 0,1
"""
def imgbooltoint(img):
	for x in range(img.shape[0]):
		for y in range(img.shape[1]):
			if img[x][y] == True:
				img[x][y] = 1
			else:
				img[x][y] = 0
	return img

"""
	Fait la soustraction deux à deux
	de chaque pixel des deux images en paramètres
"""
def soustraction_img(img1,img2):
	if (img1.shape[0] == img2.shape[0]) and (img1.shape[1] == img2.shape[1]):
		img = np.zeros(img1.shape,np.int)
		for x in range(img1.shape[0]):
			for y in range(img2.shape[1]):
				#si dans les deux images, le pixel est blanc, on laisse blanc
				if (img1[x][y] == img2[x][y]) and (img1[x][y] == 1):
					img[x][y] = 1
				#si dans les deux images, le pixel est noir, on le met à blanc
				elif (img1[x][y] == img2[x][y]) and (img1[x][y] == 0):
					img[x][y] = 1
				#si dans la première image le pixel est blanc et noir dans la deuxième, on le met à blanc
				elif (img1[x][y] != img2[x][y]) and (img1[x][y] == 1):
					img[x][y] = 1
				#si dans la première image le pixel est noir et blanc dans la deuxième, on le met à noir
				elif (img1[x][y] != img2[x][y]) and (img1[x][y] == 0):
					img[x][y] = 0
	return img


"""
	On inverse la position des pixels noirs et blancs
	dans l'image en paramètre
"""
def inverse_0_1(img):
	a = np.zeros(img.shape,np.int)
	for i in range(img.shape[0]):
		for j in range(img.shape[1]):
			if img[i][j] == 1:
				a[i][j] = 0
			else:
				a[i][j] = 1
	return a

"""
	Donne le maximum d'une matrice à coefficients positifs
"""
def max_matrice(img):
	m=0
	for i in range(img.shape[0]):
		for j in range(img.shape[1]):
			if img[i][j] > m:
				m = img[i][j]
	return m

"""
	A partir d'une liste de couples en paramètre
	on affiche les points d'abscisse le deuxième argument
	et d'ordonnée le premier argument
"""
def affiche_points(liste):
	for elt in liste:
		plt.plot(elt[1],elt[0],'ro')
