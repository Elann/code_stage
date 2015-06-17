#!/usr/bin/python
# -*- coding: Utf-8 -*

"""Module barres_verticales"""

#----------------------------------------------------------
# Importation des librairies

import numpy as np
from matplotlib import pylab as plt

#----------------------------------------------------------
# Variables globales empiriques

#Nombre de pixels minimum qu'il doit y avoir entre deux barres verticales
entre_bv = 2

#----------------------------------------------------------
# Fonctions

#trouve les barres verticales
def trouve_vertical(img,col):
	memoire = 1
	l = []
	for x in range(img.shape[0]):
		if img[x][col] != memoire:
			#plt.plot(col,x,'ro')
			memoire = not memoire
			l.append(x)
	return l	

def trouve_barres_verticales(img):
	l2 = []
	for x in range(img.shape[1]):
		l = trouve_vertical(img,x)
		l2.append(l)
	return l2
	
#ajoute l'abscisse au bout de chaque liste
def ajoute_abscisse(liste):
	for i in range(len(liste)):
		if len(liste[i]) > 0:
			for elt in liste[i]:
				elt.append(i)
	return liste

#On retire les listes vides (elles sont inutiles)	
def liste_sans_liste_vide(liste):
	l = []
	for elt in liste:
		if len(elt) > 0:
			l.append(elt)
	return l

#on passe de liste de listes de listes à liste de listes
def split_listes(liste):
	l = []
	for elt in liste:
		for elt2 in elt:
			l.append(elt2)
	return l

#Actuellement inutile
def garde_longues_barres(l,l2,taille_bv):
	if (len(l) >= 2):
		if l[1]-l[0] > taille_bv:
			l2.extend([l[0],l[1]])
			garde_longues_barres(l[2:],l2,taille_bv)
		else:
			garde_longues_barres(l[2:],l2,taille_bv) #peut planter, on part du principe que les points vont toujours deux par deux
	return l2	

#on ne garde que les barres suffisamment longues pour représenter une barre de mesure ou de note
def garde_longues_barres_liste_de_liste(liste,taille_bv):
	l = []
	for elt in liste:
		l.append(garde_longues_barres(elt,[],taille_bv))
	return l

#une droite, une liste
def groupe_deux_points(l,l2):
	if (len(l) >= 2):
		l2.append([l[0],l[1]])
		groupe_deux_points(l[2:],l2)
	return l2
	
def groupe_deux_points_liste_de_liste(liste):
	l = []
	for elt in liste:
		l.append(groupe_deux_points(elt,[]))
	return l

#on supprime les barres qui sont trop proches (en tenant compte de leur ordonnée...
def supprime_barres_trop_proches(liste):
	l = []
	l2 = []
	g = sorted(liste,key=lambda colonnes: colonnes[0])
	if len(g) >= 2:
		for i in range(len(g)-1):
			if (g[i][2] <= g[i+1][2]+entre_bv) and (g[i][2] >= g[i+1][2]-entre_bv):
				continue
			else:
				l.append(g[i])
		if (g[len(g)-1][2] > l[len(l)-1][2]+entre_bv) or (g[len(g)-1][2] < l[len(l)-1][2]-entre_bv):
			l.append(g[len(g)-1])
	
	h = sorted(l,key=lambda colonnes: colonnes[1])
	if len(h) >= 2:
		for i in range(1,len(h)):
			if (h[i-1][2] <= h[i][2]+entre_bv) and (h[i-1][2] >= h[i][2]-entre_bv):
				continue
			else:
				l2.append(h[i])
		if (h[0][2] > l2[0][2]+entre_bv) or (h[0][2] < l2[0][2]-entre_bv):
			l2.append(h[0])
	return l2

#tracé des droites verticales
def trace_verticales(tupl):
	x = (tupl[2],tupl[2])
	y = (tupl[0],tupl[1])
	plt.plot(x,y,color = 'red')

def trace_verticales_liste(liste):
	for elt in liste:
		trace_verticales(elt)
