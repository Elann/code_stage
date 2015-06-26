#!/usr/bin/python
# -*- coding: Utf-8 -*

"""
	Module barres_verticales
"""

#----------------------------------------------------------
# Importation des librairies

import numpy as np
from matplotlib import pylab as plt

#----------------------------------------------------------
# Variables globales empiriques

"""
	Nombre de pixels minimum
	entre deux barres verticales
"""
entre_bv = 2

#----------------------------------------------------------
# Fonctions

"""
	Trouve les intervalles de pixels noirs
	sur une colonne de l'image
"""
def trouve_vertical(img,col):
	memoire = 1
	l = []
	for x in range(img.shape[0]):
		if img[x][col] != memoire:
			memoire = not memoire
			l.append(x)
	return l	

"""
	Trouve tous les intervalles de pixels noirs
	sur l'image en paramètre
	
	retourne une liste contenant une liste par abscisse
	contenant les ordonnées des intervalles (ou vide)
"""
def trouve_barres_verticales(img):
	l2 = []
	for x in range(img.shape[1]):
		l = trouve_vertical(img,x)
		l2.append(l)
	return l2
	
"""
	A chaque liste contenue dans la liste en paramètre
	on ajoute l'abscisse (le numéro de la liste) en queue
"""
def ajoute_abscisse(liste):
	for i in range(len(liste)):
		if len(liste[i]) > 0:
			for elt in liste[i]:
				elt.append(i)
	return liste

"""
	On retire les listes vides contenues
	dans la liste en paramètre
"""
def liste_sans_liste_vide(liste):
	l = []
	for elt in liste:
		if len(elt) > 0:
			l.append(elt)
	return l

"""
	On passe de liste de listes de listes
	à liste de listes
"""
def split_listes(liste):
	l = []
	for elt in liste:
		for elt2 in elt:
			l.append(elt2)
	return l

"""
	A partir d'une liste l et d'un seuil
	on renvoie l composée des listes
	des intervalles au moins aussi grands que le seuil
	
	Non utilisé
"""
def garde_longues_barres(l,l2,taille_bv):
	if (len(l) >= 2):
		if l[1]-l[0] > taille_bv:
			l2.extend([l[0],l[1]])
			garde_longues_barres(l[2:],l2,taille_bv)
		else:
			garde_longues_barres(l[2:],l2,taille_bv) #peut planter, on part du principe que les points vont toujours deux par deux
	return l2	


"""
	Pour chaque liste de la liste en paramètre
	on ne garde que les intervalles d'une taille suffisante
	
	Non utilisé
"""
def garde_longues_barres_liste_de_liste(liste,taille_bv):
	l = []
	for elt in liste:
		l.append(garde_longues_barres(elt,[],taille_bv))
	return l

"""
	A partir d'une liste d'ordonnées
	on renvoie une liste de listes de deux ordonnées
"""
def groupe_deux_points(l,l2):
	if (len(l) >= 2):
		l2.append([l[0],l[1]])
		groupe_deux_points(l[2:],l2)
	return l2

"""
	Pour chaque liste de la liste en paramètre
	on s'arrange pour que chaque liste représente un intervalle
"""
def groupe_deux_points_liste_de_liste(liste):
	l = []
	for elt in liste:
		l.append(groupe_deux_points(elt,[]))
	return l

"""
	En paramètre, on a une liste de listes
	on la trie selon les ordonnées hautes (haut de la barre)
	on supprime les barres trop proches en abscisse
	on la trie selon les ordonnées basses (bas de la barre)
	on supprime les barres trop proches en abscisse
"""
def supprime_barres_trop_proches(liste):
	l = []
	l2 = []
	#tri selon les ordonnées hautes
	g = sorted(liste,key=lambda colonnes: colonnes[0])
	if len(g) >= 2:
		for i in range(len(g)-1):
			#si la barre en i et la barre en i+1 sont proches en abscisse
			if (g[i][2] <= g[i+1][2]+entre_bv) and (g[i][2] >= g[i+1][2]-entre_bv):
				continue
			else:
				l.append(g[i])
		
		#on applique la même comparaison pour la dernière barre
		if (g[len(g)-1][2] > l[len(l)-1][2]+entre_bv) or (g[len(g)-1][2] < l[len(l)-1][2]-entre_bv):
			l.append(g[len(g)-1])
	
	#tri selon les ordonnées basses
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

"""
def supprime_barres_trop_proches2(liste):
	l = []
	l2 = []
	i = 0
	
	g = sorted(liste,key=lambda colonnes: colonnes[0])
	if len(g) >= 2:
		while i < len(g)-1:
			#si la barre en i est très proche de celle en i+1
			if (g[i][2] <= g[i+1][2]+entre_bv) and (g[i][2] >= g[i+1][2]-entre_bv):
				#si la barre en i est plus grande que celle en i+1
				if (g[i][1]-g[i][0]) > (g[i+1][1]-g[i+1][0]):
					l.append(g[i])
					i = i + 2
				else:
					i = i + 1
			else:
				l.append(g[i])
				i = i+1
				
		if (g[len(g)-1][2] <= l[len(l)-1][2]+entre_bv) or (g[len(g)-1][2] >= l[len(l)-1][2]-entre_bv):
			if (g[len(g)-1][1]-g[len(g)-1][0]) > (l[len(l)-1][1]-l[len(l)-1][0]):
				l.append(g[len(g)-1])
		else:
			l.append(g[len(g)-1])
	
	i = 1
	h = sorted(l,key=lambda colonnes: colonnes[1])
	if len(h) >= 2:
		while i < len(h):
			#si la barre en i est très proche de celle en i+1
			if (h[i-1][2] <= h[i][2]+entre_bv) and (h[i-1][2] >= h[i][2]-entre_bv):
				#si la barre en i est plus grande que celle en i+1
				if (h[i-1][1]-h[i-1][0]) > (h[i][1]-h[i][0]):
					l2.append(h[i])
					i = i + 2
				else:
					i = i + 1
			else:
				l2.append(h[i])
				i = i+1

		if (h[0][2] <= l2[0][2]+entre_bv) or (h[0][2] >= l2[0][2]-entre_bv):
			if (h[0][1]-h[0][0]) > (l2[0][1]-l2[0][0]):
				l2.append(h[0])
		else:
			l2.append(h[0])
	return l2
"""	
	
"""
	Trace le segment d'abscisse le troisième argument du triplet
	Ordonnées allant du premier argument
	au deuxième argument du triplet
"""
def trace_verticales(tupl):
	x = (tupl[2],tupl[2])
	y = (tupl[0],tupl[1])
	plt.plot(x,y,color = 'red')

"""
	Pour chaque liste de la liste en paramètre
	trace la barre verticale qu'elle représente
"""
def trace_verticales_liste(liste):
	for elt in liste:
		trace_verticales(elt)
