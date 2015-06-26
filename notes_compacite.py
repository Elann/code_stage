#!/usr/bin/python
# -*- coding: Utf-8 -*

"""
	Module notes_compacite
"""

#----------------------------------------------------------
# Importation des librairies

import numpy as np
from matplotlib import pylab as plt
import matplotlib.pyplot as plt2
from math import *
from pymorph import *

from fonctions_annexes import *
from reconnaissance_clef import *


#----------------------------------------------------------
# Variables globales empiriques

#Distance entre la note et l'extrémité de la barre verticale
dist_note_barre = 5
#Distance entre le symbole croche et l'extrémité de la barre verticale
dist_croche_barre = 5
#Aire minimale acceptée pour être une noire
#aire = 70
#Pourcentage de remplissage du carré pour accepter une double croche
pc_cro = 35

#----------------------------------------------------------
# Fonctions

"""
	A partir d'une image labellisée
	on compte pour chaque label le nombre de pixel qui le composent
	ce nombre forme l'aire élargie (aire+périmètre)
	de la composante connexe
	si l'aire est inférieure à celle d'un cercle de rayon ecart/2
	on l'annule
"""
def calcule_aires(img,ecart):
	a = np.zeros((2,max_matrice(img)+1),np.int)
	pi = 4*atan(1)
	for i in range(img.shape[0]):
		for j in range(img.shape[1]):
			if img[i][j] != 0:
				co = img[i][j]
				a[0][co] = a[0][co] + 1
	for i in range(a.shape[1]):
		#l'aire pour être une note doit au moins être celle d'un cercle de rayon ecart/2
		if a[0][i] < (pi*ecart*ecart)/4:
			a[0][i] = 0
	return a

"""
	A partir d'une image labellisée
	pour chaque label on compte le nombre de pixel
	dont les quatre voisins ne sont pas identiques
	ce nombre est le périmètre de chaque composante connexe
	
	On soustrait à l'aire de chaque composante
	le périmètre de la composante
	on obtient un tableau composé des aires et des périmètres
"""
def calcule_perimetres(img,tab):
	for i in range(1,img.shape[0]-1):
		for j in range(1,img.shape[1]-1):
			#si le pixel n'appartient pas au fond
			if img[i][j] != 0:
				#si tous les voisins ne sont pas de la même "couleur"
				if img[i][j] != img[i-1][j] or img[i][j] != img[i][j-1] or img[i][j] != img[i+1][j] or img[i][j] != img[i][j+1]:
					co = img[i][j]
					tab[1][co] = tab[1][co] + 1
	#soustraction des périmètres aux aires
	for i in range(tab.shape[1]):
		tab[0][i] = max(tab[0][i]-tab[1][i],0)
	return tab

"""
	A partir d'un tableau des aires et des périmètres
	on calcule la compacité de chaque composante connexe
"""
def calcule_compacite(tab):
	pi = 4*atan(1)
	a = np.zeros(tab.shape[1],np.float)
	for i in range(len(a)):
		if tab[1][i] != 0:
			a[i] = (4*pi*tab[0][i])/(tab[1][i]*tab[1][i])
	return a

"""
	A partir du tableau des compacités et de l'image
	on ajoute à une liste tous les pixels de l'image
	dont la compacité dépasse un certain seuil
"""
def colorie_bons(img,tab,seuil_comp):
	l = []
	for i in range(img.shape[0]):
		for j in range(img.shape[1]):
			#chaque pixel a un numéro (labellisation)
			co = img[i][j]
			if tab[co] > seuil_comp:
				img[i][j] = 255
				l.append((i,j))
				#plt.plot(j,i,'ro')
	return (l,img)


"""
	i : abscisse de la barre verticale
	note : ordonnée de la supposée note
	j : ordonnée de la barre verticale
	ecart : écart moyen entre les portées
	place : 'b' pour en bas de la barre, 'h' pour en haut
	coul : couleur à utiliser pour le dessin de la note
	
	si la différence entre l'ordonnée de la note
	et celle de la barre verticale
	est inférieure à un certain seuil
	alors on a une note qu'on dessine
	à gauche de la barre si on est en bas de la barre
	à droite de la barre si on est en haut de la barre
"""
def existe_noire(i,note,j,ecart,place,coul):
	rep = 0
	e2 = int(round(ecart/2))
	if abs(i - note) <= dist_note_barre:
		rep = i
		if place == 'b':
			c2 = plt2.Circle(((2*j-ecart)/2,i),e2,color=coul)
			plt2.gcf().gca().add_artist(c2)
		else:
			c2 = plt2.Circle(((2*j+ecart)/2,i),e2,color=coul)
			plt2.gcf().gca().add_artist(c2)
	return rep

"""
	Pour chaque barre verticale de la liste en paramètre
	on trouve les pixels des composantes connexes
	qui ont la même abscisse
	et dont l'ordonnée se trouve dans l'intervalle de la barre
	on vérifie alors si le pixel est celui d'une note
	en bas puis en haut
"""
def bv_collee_notes(bv,note,ecart):
	for elt in bv:
		for elt2 in note:
			if (elt[2] == elt2[1]) and (elt2[0] < elt[1]) and (elt2[0] > elt[0]):
				if len(elt) < 4:
					bas = existe_noire(elt[1],elt2[0],elt[2],ecart,'b','red')
					haut = existe_noire(elt[0],elt2[0],elt[2],ecart,'h','red')
					if bas !=0:
						#on réhausse un peu la note
						elt.append(bas-2)
					elif haut != 0:
						elt.append(haut-1)
	return bv

"""
	A partir de la liste des barres verticales
	auxquelles on a ajouté les notes détectées
	on ajoute un 0 aux barres verticales qui n'ont pas de note
"""
def liste_notes(liste):
	somme = 0
	l = []
	#plusieurs notes détectées
	if len(liste) > 4:
		for i in range(3,len(liste)):
			somme = somme + liste[i]
			l.extend(liste[:3])
			#on fait la moyenne des ordonnées
			l.append(somme/(len(liste)-3))
	#pas de note détectée
	elif len(liste) == 3:
		l = liste
		l.append(0)
	#une seule note détectée
	else:
		l = liste
	return l

"""
	Pour chaque liste de la liste en paramètre
	on la met sous la forme [ord1,ord2,ab,ord_note ou 0]
"""
def liste_listes_note(liste):
	l = []
	for elt in liste:
		l.append(liste_notes(elt))
	return l

#--------------------------------------------------------------
#Croches
	
"""
	On retire de l'image en paramètre
	les pixels associés aux notes de la liste en paramètre
"""
def enleve_notes(img,liste):
	for elt in liste:
		(i,j) = elt
		#on retire les noires précédemment sélectionnées en les mettant en "blanc - fond"
		img[i][j] = 1
	return img

"""
	A partir de l'image en paramètre
	on récupère les pixels noirs
"""
def recupere_points(img):
	l = []
	for i in range(img.shape[0]):
		for j in range(img.shape[1]):
			#on récupère les pixels noirs
			if img[i][j] != 1 or img[i][j] == False:
				#plt.plot(j,i,'ro')
				l.append((i,j))
	return l

"""
	i : abscisse de la barre verticale
	croche : ordonnée de la supposée croche
	j : ordonnée de la barre verticale
	ecart : écart moyen entre les portées
	place : 'b' pour en bas de la barre, 'h' pour en haut
	numero_croche : 1 pour croche simple, 2 pour double croche...
	
	si la différence entre l'ordonnée de la croche
	et celle de la barre verticale
	est inférieure à un certain seuil
	alors on a une note qu'on dessine
	à gauche de la barre si on est en bas de la barre
	à droite de la barre si on est en haut de la barre
"""
def existe_croche(i,croche,j,ecart,place,numero_croche):
	rep = 0
	e2 = int(round(ecart/2))
	if abs(i - croche) <= (numero_croche-1)*e2+dist_croche_barre:
		rep = 1
		if place == 'b':
			p = plt2.Rectangle((j-e2,i-e2-(numero_croche-1)*ecart),e2,e2,color='b')
			plt2.gcf().gca().add_artist(p)
		else:
			p = plt2.Rectangle((j,i+ecart*(numero_croche-1)),e2,e2,color='b')
			plt2.gcf().gca().add_artist(p)
	return rep

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

"""
	On utilise la méthode par amas faute de mieux
	
	Pour chacune des barres verticales de la liste en argument
	si on lui a détecté une note et déjà une croche
	on cherche d'éventuelles autres croches
	en haut et en bas de la barre
"""
def existe_autre_croche(img,bv,ecart,nbr_croches):
	ecart = int(round(ecart))
	for elt in bv:
		if len(elt) == 5:
			if elt[4] < 2:
				if elt[4] == 0: #on cherche en bas
					for i in range(1,nbr_croches):
						elt[4] = 1 + existe_croche_bas(img,ecart,elt[1]-i*ecart,elt[2],pc_cro) + elt[4]
				elif elt[4] == 1: #on cherche en haut
					for i in range(1,nbr_croches):
						elt[4] = existe_croche_haut(img,ecart,elt[0]+i*ecart,elt[2],pc_cro) + elt[4]
	return bv

"""
	Pour chaque barre verticale de la liste en paramètre
	on trouve les pixels des composantes connexes
	qui ont la même abscisse
	et dont l'ordonnée se trouve dans l'intervalle de la barre
	on vérifie alors si le pixel est celui d'une croche
	en bas puis en haut
"""
def bv_collee_croche(bv,croche,ecart,img,numer):
	e2 = int(round(ecart/2))
	for elt in bv:
		for elt2 in croche:
			if (elt[2] == elt2[1]) and (elt2[0] < elt[1]) and (elt2[0] > elt[0]):		
				#si on a une note et pas encore détecté de croche
				if (elt[3] != 0) and (len(elt) < 5):
					bas = existe_croche(elt[1],elt2[0],elt[2],ecart,'b',numer)
					haut = existe_croche(elt[0],elt2[0],elt[2],ecart,'h',numer)
					if bas !=0:
						elt.append(0) 
					elif haut != 0:
						elt.append(1) 
	#on renvoie la liste des barres verticales augmentées
	return bv

"""
	Si la liste représentant une barre verticale en argument
	n'a pas 5 arguments (donc si elle n'a pas de croche)
	on lui ajoute un zéro
"""
def liste_croches(liste):
	l = []
	#pas de croche
	if len(liste) == 4:
		l = liste
		l.append(0)
	else:
		l = liste
	return l

"""
	On met chaque barre verticale de la liste
	sous la forme [ord1,ord2,ab,ord_note ou 0,nbr_croches]
"""
def liste_listes_croche(liste):
	l = []
	for elt in liste:
		l.append(liste_croches(elt))
	return l

#--------------------------------------------------------------
#Noms des notes

"""
	On sépare la liste des barres verticales
	en cinq portées portée
	en cherchant à quelle portée appartient
	le milieu de la barre verticale
"""
def notes_par_portees(liste,tab,ecart):
	#on crée un tableau de la taille "nombre de portées"
	l = []
	for i in range(len(tab[0])):
		l.append([])
		
	#on parcourt les portées
	for i in range(len(tab[0])):
		for j in range(len(liste)):
			m = (liste[j][1]+liste[j][0])/2 
			#si le milieu de la barre appartient à la portée i, on l'ajoute à la case i
			if m >= tab[0][i]-2*ecart and m <= tab[4][i]+2*ecart:
				l[i].append(liste[j])
	return l

"""
	j : ordonnée de l'extrémité de la barre où se trouve la note
	tab : liste des ordonnées des portées
	ecart : ecart moyen entre les portées
	inter_note : intervalle autour de la position théorique de la note
	x : numéro de la portée (à partir de 0)
	
	Pour chaque note, on regarde où elle se place
	par rapport aux lignes de la portée
	on en déduit sa valeur pour la clef de sol
"""
def determine_note_sol(j,tab,ecart,inter_note,x):
	rep = ''
	#notes sur les lignes
	if j > tab[0][x]-inter_note and j < tab[0][x]+inter_note:
		rep = 'fa'
	elif j > tab[1][x]-inter_note and j < tab[1][x]+inter_note:
		rep = 're'
	elif j > tab[2][x]-inter_note and j < tab[2][x]+inter_note:
		rep = 'si'
	elif j > tab[3][x]-inter_note and j < tab[3][x]+inter_note:
		rep = 'sol'
	elif j > tab[4][x]-inter_note and j < tab[4][x]+inter_note:
		rep = 'mi grave'
	#notes entre les lignes
	elif j > (tab[0][x]+tab[1][x])/2-inter_note and j < (tab[0][x]+tab[1][x])/2+inter_note:
		rep = 'mi'
	elif j > (tab[1][x]+tab[2][x])/2-inter_note and j < (tab[2][x]+tab[1][x])/2+inter_note:
		rep = 'do'
	elif j > (tab[2][x]+tab[3][x])/2-inter_note and j < (tab[3][x]+tab[2][x])/2+inter_note:
		rep = 'la'
	elif j > (tab[3][x]+tab[4][x])/2-inter_note and j < (tab[4][x]+tab[3][x])/2+inter_note:
		rep = 'fa grave'
	#notes en-dessous des lignes
	elif j > (2*tab[4][x]+ecart)/2-inter_note and j < (2*tab[4][x]+ecart)/2+inter_note:
		rep = 're grave'
	elif j > tab[4][x]+ecart-inter_note and j < tab[4][x]+ecart+inter_note:
		rep = 'do grave'
	elif j > (2*tab[4][x]+3*ecart)/2-inter_note and j < (2*tab[4][x]+3*ecart)/2+inter_note:
		rep = 'si grave'
	elif j > tab[4][x]+2*ecart-inter_note and j < tab[4][x]+2*ecart+inter_note:
		rep = 'la grave'
	#notes au-dessus des lignes
	elif j > (2*tab[0][x]-ecart)/2-inter_note and j < (2*tab[0][x]-ecart)/2+inter_note:
		rep = 'sol aigu'
	elif j > tab[0][x]-ecart-inter_note and j < tab[0][x]-ecart+inter_note:
		rep = 'la aigu'
	elif j > (2*tab[0][x]-3*ecart)/2-inter_note and j < (2*tab[0][x]-3*ecart)/2+inter_note:
		rep = 'si aigu'
	elif j > tab[0][x]-2*ecart-inter_note and j < tab[0][x]-2*ecart+inter_note:
		rep = 'do aigu'
	return rep

"""
	j : ordonnée de l'extrémité de la barre où se trouve la note
	tab : liste des ordonnées des portées
	ecart : ecart moyen entre les portées
	inter_note : intervalle autour de la position théorique de la note
	x : numéro de la portée (à partir de 0)
	
	Pour chaque note, on regarde où elle se place
	par rapport aux lignes de la portée
	on en déduit sa valeur pour la clef de fa
"""
def determine_note_fa(j,tab,ecart,inter_note,x):
	rep = ''
	#notes sur les lignes
	if j > tab[0][x]-inter_note and j < tab[0][x]+inter_note:
		rep = 'la aigu'
	elif j > tab[1][x]-inter_note and j < tab[1][x]+inter_note:
		rep = 'fa'
	elif j > tab[2][x]-inter_note and j < tab[2][x]+inter_note:
		rep = 're'
	elif j > tab[3][x]-inter_note and j < tab[3][x]+inter_note:
		rep = 'si'
	elif j > tab[4][x]-inter_note and j < tab[4][x]+inter_note:
		rep = 'sol'
	#notes entre les lignes
	elif j > (tab[0][x]+tab[1][x])/2-inter_note and j < (tab[0][x]+tab[1][x])/2+inter_note:
		rep = 'sol aigu'
	elif j > (tab[1][x]+tab[2][x])/2-inter_note and j < (tab[2][x]+tab[1][x])/2+inter_note:
		rep = 'mi'
	elif j > (tab[2][x]+tab[3][x])/2-inter_note and j < (tab[3][x]+tab[2][x])/2+inter_note:
		rep = 'do'
	elif j > (tab[3][x]+tab[4][x])/2-inter_note and j < (tab[4][x]+tab[3][x])/2+inter_note:
		rep = 'la'
	#notes en-dessous des lignes
	elif j > (2*tab[4][x]+ecart)/2-inter_note and j < (2*tab[4][x]+ecart)/2+inter_note:
		rep = 'fa grave'
	elif j > tab[4][x]+ecart-inter_note and j < tab[4][x]+ecart+inter_note:
		rep = 'mi grave'
	elif j > (2*tab[4][x]+3*ecart)/2-inter_note and j < (2*tab[4][x]+3*ecart)/2+inter_note:
		rep = 're grave'
	elif j > tab[4][x]+2*ecart-inter_note and j < tab[4][x]+2*ecart+inter_note:
		rep = 'do grave'
	#notes au-dessus des lignes
	elif j > (2*tab[0][x]-ecart)/2-inter_note and j < (2*tab[0][x]-ecart)/2+inter_note:
		rep = 'si aigu'
	elif j > tab[0][x]-ecart-inter_note and j < tab[0][x]-ecart+inter_note:
		rep = 'do aigu'
	elif j > (2*tab[0][x]-3*ecart)/2-inter_note and j < (2*tab[0][x]-3*ecart)/2+inter_note:
		rep = 're aigu'
	elif j > tab[0][x]-2*ecart-inter_note and j < tab[0][x]-2*ecart+inter_note:
		rep = 'mi aigu'
	return rep

"""
	j : ordonnée de l'extrémité de la barre où se trouve la note
	tab : liste des ordonnées des portées
	ecart : ecart moyen entre les portées
	inter_note : intervalle autour de la position théorique de la note
	x : numéro de la portée (à partir de 0)
	
	Pour chaque note, on regarde où elle se place
	par rapport aux lignes de la portée
	on en déduit sa valeur pour la clef d'ut
"""
def determine_note_ut(j,tab,ecart,inter_note,x):
	rep = ''
	#notes sur les lignes
	if j > tab[0][x]-inter_note and j < tab[0][x]+inter_note:
		rep = 'sol'
	elif j > tab[1][x]-inter_note and j < tab[1][x]+inter_note:
		rep = 'mi'
	elif j > tab[2][x]-inter_note and j < tab[2][x]+inter_note:
		rep = 'do'
	elif j > tab[3][x]-inter_note and j < tab[3][x]+inter_note:
		rep = 'la'
	elif j > tab[4][x]-inter_note and j < tab[4][x]+inter_note:
		rep = 'fa grave'
	#notes entre les lignes
	elif j > (tab[0][x]+tab[1][x])/2-inter_note and j < (tab[0][x]+tab[1][x])/2+inter_note:
		rep = 'fa'
	elif j > (tab[1][x]+tab[2][x])/2-inter_note and j < (tab[2][x]+tab[1][x])/2+inter_note:
		rep = 're'
	elif j > (tab[2][x]+tab[3][x])/2-inter_note and j < (tab[3][x]+tab[2][x])/2+inter_note:
		rep = 'si'
	elif j > (tab[3][x]+tab[4][x])/2-inter_note and j < (tab[4][x]+tab[3][x])/2+inter_note:
		rep = 'sol grave'
	#notes en-dessous des lignes
	elif j > (2*tab[4][x]+ecart)/2-inter_note and j < (2*tab[4][x]+ecart)/2+inter_note:
		rep = 'mi grave'
	elif j > tab[4][x]+ecart-inter_note and j < tab[4][x]+ecart+inter_note:
		rep = 're grave'
	elif j > (2*tab[4][x]+3*ecart)/2-inter_note and j < (2*tab[4][x]+3*ecart)/2+inter_note:
		rep = 'do grave'
	elif j > tab[4][x]+2*ecart-inter_note and j < tab[4][x]+2*ecart+inter_note:
		rep = 'sol grave'
	#notes au-dessus des lignes
	elif j > (2*tab[0][x]-ecart)/2-inter_note and j < (2*tab[0][x]-ecart)/2+inter_note:
		rep = 'la aigu'
	elif j > tab[0][x]-ecart-inter_note and j < tab[0][x]-ecart+inter_note:
		rep = 'si aigu'
	elif j > (2*tab[0][x]-3*ecart)/2-inter_note and j < (2*tab[0][x]-3*ecart)/2+inter_note:
		rep = 'do aigu'
	elif j > tab[0][x]-2*ecart-inter_note and j < tab[0][x]-2*ecart+inter_note:
		rep = 're aigu'
	return rep

"""
	bv : liste des barres verticales
	tab : liste des ordonnées des portées
	ecart : écart moyen entre les portées
	list_img : images des portées découpée dans l'image d'étude
	sol : template de la clef de sol
	fa : template de la clef de fa
	ut : template de la clef d'ut
	dist : abscisse maximale de la clef sur la portée
"""
def nom_notes(bv,tab,ecart,list_img,sol,fa,ut,dist):
	rep = ''
	rep2 = ''
	
	#détermination de l'intervalle [X-inter_note,X+internote] dans lequel se trouve la note
	if ecart < 10:
		inter_note = 2
	elif ecart < 20:
		inter_note = 3
	else:
		inter_note = 5
		
	for i in range(len(bv)):
	
		#pour une portée, on détermine la clef
		clef,ab = cherche_bonne_clef(list_img[i],sol,fa,ut,tab,dist)
	
		for elt in bv[i]:
			#si on a une note et qu'elle se trouve après la clef
			if (elt[3] != 0 or elt[5] != 0) and elt[2] > ab:
			
				if elt[3] != 0:
					n = elt[3]
				elif elt[5] != 0:
					n = elt[5]
				
				#notes
				if clef == 'sol':
					rep = determine_note_sol(n,tab,ecart,inter_note,i)
				elif clef == 'fa':
					rep = determine_note_fa(n,tab,ecart,inter_note,i)
				elif clef == 'ut':
					rep = determine_note_ut(n,tab,ecart,inter_note,i)
			
				#croches
				if elt[4] == 1:
					rep2 = 'croche '+rep
					elt.append(rep2)
				elif elt[4] == 2:
					rep2 = 'double croche '+rep
					elt.append(rep2)
				elif elt[4] == 3:
					rep2 = 'triple croche '+rep
					elt.append(rep2)
				elif elt[5] != 0:
					rep2 = 'blanche '+rep
					elt.append(rep2)
				else:
					elt.append(rep)
				
				#on affiche le nom de la note sous celle-ci
				plt2.text(elt[2]-1,elt[1]+4*ecart,rep,fontsize=7,color='g')
	return bv

#------------------------------------------------------------
#Blanches

"""
	A partir d'une équation de droite définie par
	son ordonnée à l'origine b et sa pente a
	on retire de l'image en paramètre
	tous les points (x,y) tels que y = ax+b
"""
def enleve_portees(img,soluce):
	for x in range(img.shape[0]):
		for y in range(img.shape[1]):
			if round(y*soluce[0]+soluce[1]) == x:
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
		for elt2 in elt:
			img1 = enleve_portees(img,elt2)
			img2 = union(img2,img1)
	return img2

"""
	Pour chaque barre verticale de la liste en paramètre
	qui n'ont pas encore de note
	on trouve les pixels des composantes connexes
	qui ont la même abscisse
	et dont l'ordonnée se trouve dans l'intervalle de la barre
	on vérifie alors si le pixel est celui d'une blanche
	en bas puis en haut
"""
def cherche_blanche(bv,note,ecart):
	for elt in bv:
		#si on a pas encore de note
		if elt[3] == 0:	
			for elt2 in note:
				if (elt[2] == elt2[1]) and (elt2[0] < elt[1]) and (elt2[0] > elt[0]):
					if len(elt) < 6:
						bas = existe_noire(elt[1],elt2[0],elt[2],ecart,'b','magenta')
						haut = existe_noire(elt[0],elt2[0],elt[2],ecart,'h','magenta')
						if bas !=0:
							#on réhausse un peu la note
							elt.append(bas-2)
						elif haut != 0:
							elt.append(haut-1)
	return bv

"""
	On met chaque barre verticale de la liste en argument
	sous la forme [ord1,ord2,ab,ord_note ou 0,
	nbr_croches,ord_blanche ou 0]
"""
def liste_toutes_notes(note):
	for elt in note:
		if len(elt) < 6:
			elt.append(0)
	return note


#----------------------------------------------------------
# Barres de mesure

"""
	Pour chaque barre verticale de la liste en argument
	si on a ni noire, ni blanche
	et que la longueur de l'intervalle dépasse un seuil
	alors c'est une barre de mesure
"""
def barres_mesure(bv,ecart):
	l = []
	for elt in bv:
		if elt[3] == 0 and elt[5] == 0:
			longueur = elt[1]-elt[0]
			#une barre de mesure doit au moins faire la largeur de la portée
			if longueur >= 4*ecart:
				l.append(elt)
				plt.plot([elt[2],elt[2]],[elt[1],elt[0]],'b',linewidth=3)
		else:
			l.append(elt)
	return l
