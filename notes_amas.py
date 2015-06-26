#!/usr/bin/python
# -*- coding: Utf-8 -*

"""
	Module notes_amas
"""

#----------------------------------------------------------
# Importation des librairies

import numpy as np
from matplotlib import pylab as plt
import matplotlib.pyplot as plt2
from math import *

from fonctions_annexes import *

#----------------------------------------------------------
# Variables globales empiriques

#Nombre maximal de croches sur une même note
nbr_croches = 2

#----------------------------------------------------------
# Fonctions

"""
	A partir d'une équation de droite définie par
	son ordonnée à l'origine b et sa pente a
	on retire de l'image en paramètre
	tous les points (x,y) tels que y = ax+b
"""
def enleve_portees(img,soluce):
	for x in range(img.shape[0]):
		for y in range(img.shape[1]):
			if round(y*soluce[0]+soluce[1]) == round(x):
				#peu précis mais imprécision des droites détectées oblige	
				img[x][y] = 1
				img[x-1][y] = 1
				img[x+1][y] = 1 
	return img

"""
	A partir d'une image et d'une liste d'équations de droites
	on retire les points de l'image situés sur les droites
"""
def enleve_portees_liste(img,liste):
	img1 = np.zeros(img.shape,np.int)
	img2 = np.zeros(img.shape,np.int)
	for elt in liste:
		#on retire une droite à chaque fois
		img1 = enleve_portees(img,elt)
		#on fait l'union de toutes les images à qui il manque une droite
		img2 = union(img2,img1)
	return img2

"""
	A partir d'un rayon r donné
	on crée une image représentant un cercle noir de rayon r
	sur fond blanc
"""
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

"""
	img : image sur laquelle on travaille
	ecart : ecart moyen entre les portées
	i : abscisse du point à considérer
	j : ordonnée du point à considérer
	seuil : pourcentage minimal de remplissage du carré
	coul : couleur du rond à dessiner
	
	A gauche du point de coordonnées i,j
	on trace virtuellement un carré de longueur ecart 
	on fait la somme des pixels noirs contenus dans le carré
	si la somme dépasse le seuil en argument
	on considère qu'il y a une note et on la dessine
	Dans le cas contraire, on recommence à droite du point
	
	on renvoie un booléen indiquant la présence ou non d'une note
"""
def existe_note(img,ecart,i,j,seuil,coul):
	somme = 0
	rep = False
	ecart = int(round(ecart))
	#forme le carré
	for x in range(i-ecart,i):
		for y in range(j-ecart,j):
			#compte les pixels noirs
			if x < img.shape[0] and y < img.shape[1]:
				if img[x][y] == 0:
					somme = 1 + somme
				#plt.plot([j-ecart,j,j,j-ecart,j-ecart],[i-ecart-1,i-ecart-1,i-1,i-1,i-ecart-1])
				
	#si on remplit plus de seuil % du carré
	#à gauche du point : note en bas de la barre
	if somme*100 >= seuil*ecart*ecart:
		c1 = plt2.Circle(((2*j-ecart)/2,i),3*e/2,color=coul)
		plt2.gcf().gca().add_artist(c1)
		rep = True
	else:
	
		somme = 0
		#forme le carré
		for x in range(i-ecart,i):
			for y in range(j,j+ecart):
				#compte les pixels noirs
				if x < img.shape[0] and y < img.shape[1]:
					if img[x][y] == 0:
						somme = 1 + somme
					#plt.plot([j,j+ecart,j+ecart,j,j],[i-ecart+1,i-ecart+1,i+1,i+1,i-ecart+1])
					
		#si on remplit plus de seuil % du carré
		#à droite du point : note en haut de la barre
		if somme*100 >= seuil*ecart*ecart:
			c1 = plt2.Circle(((2*j+ecart)/2,i),3*e/2,color=coul)
			plt2.gcf().gca().add_artist(c1)
			rep = True
	return rep

"""
	Pour chaque barre verticale contenue dans la liste en argument
	on regarde en bas de cette barre puis en haut
	s'il y a une note détectée
"""
def existe_noire_img(img,liste,ecart,pc_note):
	for elt in liste:
		#en bas
		elt.append(existe_note(img,ecart,elt[1],elt[2],pc_note,'g'))
		#en haut
		elt.append(existe_note(img,ecart,elt[0],elt[2],pc_note,'g'))
	return liste

"""
	img : image sur laquelle on travaille
	ecart : ecart moyen entre les portées
	i : abscisse du point à considérer
	j : ordonnée du point à considérer
	pc_cro : pourcentage minimal de remplissage du carré
	
	On s'intéresse à la présence d'une croche en haut de la barre
	A gauche du point de coordonnées i,j
	on trace virtuellement un carré de longueur ecart 
	on fait la somme des pixels noirs contenus dans le carré
	si la somme dépasse le seuil en argument
	on considère qu'il y a une croche et on la dessine
	Dans le cas contraire, on recommence à droite du point
	
	on renvoie un entier indiquant la présence ou non d'une croche
	1 : une croche, 0 : pas de croche
"""
def existe_croche_haut(img,ecart,i,j,pc_cro):
	somme = 0
	rep = 0
	ecart = int(round(ecart))
	e2 = int(round(ecart/2))
	#forme le carré
	for x in range(i,i+e2):
		for y in range(j-e2,j):
			#compte les pixels noirs
			if x < img.shape[0] and y < img.shape[1]:
				if img[x][y] == 0:
					somme = 1 + somme
					
	#si on remplit plus de pc_cro % du carré
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
		
		#si on remplit plus de pc_cro % du carré
		if somme*100 >= pc_cro*e2*e2:
			p = plt2.Rectangle((j,i),e2,e2,color='b')
			plt2.gcf().gca().add_artist(p)
			rep = 1
	return rep

"""
	img : image sur laquelle on travaille
	ecart : ecart moyen entre les portées
	i : abscisse du point à considérer
	j : ordonnée du point à considérer
	pc_cro : pourcentage minimal de remplissage du carré
	
	On s'intéresse à la présence d'une croche en bas de la barre
	A gauche du point de coordonnées i,j
	on trace virtuellement un carré de longueur ecart 
	on fait la somme des pixels noirs contenus dans le carré
	si la somme dépasse le seuil en argument
	on considère qu'il y a une croche et on la dessine
	Dans le cas contraire, on recommence à droite du point
	
	on renvoie un entier indiquant la présence ou non d'une croche
	1 : une croche, 0 : pas de croche
"""
def existe_croche_bas(img,ecart,i,j,pc_cro):
	somme = 0
	rep = 0
	ecart = int(round(ecart))
	e2 = int(round(ecart/2))
	#forme le carré
	for x in range(i-e2,i):
		for y in range(j-e2,j):
			#compte les pixels noirs
			if x < img.shape[0] and y < img.shape[1]:
				if img[x][y] == 0:
					somme = 1 + somme
					
	if somme*100 >= pc_cro*e2*e2:
		p = plt2.Rectangle((j-e2,i-e2),e2,e2,color='b')
		plt2.gcf().gca().add_artist(p)
		rep = 1
		
	else:
		somme = 0
		#forme le carré
		for x in range(i-e2,i):
			for y in range(j,j+e2):
				#compte les pixels noirs
				if x < img.shape[0] and y < img.shape[1]:
					if img[x][y] == 0:
						somme = 1 + somme
		if somme*100 >= pc_cro*e2*e2:
			p = plt2.Rectangle((j-e2,i-e2),e2,e2,color='b')
			plt2.gcf().gca().add_artist(p)
			rep = 1
	return rep


"""
	Pour chacune des barres verticales de la liste en argument
	si on lui a détecté une note et déjà une croche
	on cherche d'éventuelles autres croches
	en haut et en bas de la barre
"""
def existe_autre_croche(img,liste,ecart,pc_cro):
	ecart = int(round(ecart))
	for elt in liste:
		#si on a une liste de la forme [ord1,ord2,ab,note,croche]
		if len(elt) > 5:
			#si on a bien déjà détecté une croche
			if elt[5] != 0:
				for i in range(1,nbr_croches):
					elt[5] = (existe_croche_haut(img,ecart,elt[0]+i*ecart,elt[2],pc_cro) or existe_croche_bas(img,ecart,elt[1]-i*ecart,elt[2],pc_cro)) + elt[5]
	return liste

"""
	img : image sur laquelle on travaille pour les croches
	img2 : image sur laquelle on travaille pour les blanches
	liste : liste de barres verticales
	ecart : ecart moyen entre les portées
	pc_cro : pourcentage de remplissage minimal pour avoir une croche
	pc_blan : pourcentage de remplissage minimal pour avoir une blanche
	
	Pour chaque barre verticale
	si on a une noire en haut on cherche une croche en bas
	si on a une noire en bas on cherche une croche en haut
	si on a pas de noire on cherche une blanche
	en haut et en bas de la barre verticale
	si on ne détecte pas de blanche, on a une barre de mesure
"""
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
