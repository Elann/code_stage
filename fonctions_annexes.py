#!/usr/bin/python
# -*- coding: Utf-8 -*

"""Module portees_chgt_repere"""

#----------------------------------------------------------
# Importation des librairies

import numpy as np
from matplotlib import pylab as plt

#----------------------------------------------------------
# Fonctions

#on transforme l'image en 0 et en 1
def img_0_1(img):
	for x in range(img.shape[0]):
		for y in range(img.shape[1]):
			if img[x][y] > seuil_noir:
				img[x][y] = 1
			else:
				img[x][y] = 0

#On passe des booléens aux entiers
def imgbooltoint(img):
	for x in range(img.shape[0]):
		for y in range(img.shape[1]):
			if img[x][y] == True:
				img[x][y] = 1
			else:
				img[x][y] = 0
	return img

#fait la soustraction deux à deux de chaque pixel des deux images
def soustraction_img(img1,img2):
	if (img1.shape[0] == img2.shape[0]) and (img1.shape[1] == img2.shape[1]):
		img = np.zeros(img1.shape,np.int)
		for x in range(img1.shape[0]):
			for y in range(img2.shape[1]):
				if (img1[x][y] == img2[x][y]) and (img1[x][y] == 1):
					img[x][y] = 1
				elif (img1[x][y] == img2[x][y]) and (img1[x][y] == 0):
					img[x][y] = 1
				elif (img1[x][y] != img2[x][y]) and (img1[x][y] == 1):
					img[x][y] = 1
				elif (img1[x][y] != img2[x][y]) and (img1[x][y] == 0):
					img[x][y] = 0
	return img

#on est obligé d'avoir des 0 en fond et des 1 pour le noir dans la fonction label
def inverse_0_1(img):
	a = np.zeros(img.shape,np.int)
	for i in range(img.shape[0]):
		for j in range(img.shape[1]):
			if img[i][j] == 1:
				a[i][j] = 0
			else:
				a[i][j] = 1
	return a

def max_matrice(img):
	m=0
	for i in range(img.shape[0]):
		for j in range(img.shape[1]):
			if img[i][j] > m:
				m = img[i][j]
	return m
	
def affiche_points(liste):
	for elt in liste:
		plt.plot(elt[1],elt[0],'ro')
