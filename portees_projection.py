#!/usr/bin/python
# -*- coding: Utf-8 -*

"""Module portees_projection"""

#----------------------------------------------------------
# Importation des librairies

import numpy as np
from matplotlib import pylab as plt
from math import *
import sys

#----------------------------------------------------------
# Variables globales empiriques

#marge autorisée pour les distances entre les lignes de la portée
delta_portee = 2 

#----------------------------------------------------------
# Fonctions

#Teste si 5 ordonnées peuvent former une portée
def test_cinq(a,b,c,d,e):
	if (b-a) < delta_portee+(c-b) and (c-b) < delta_portee+(d-c) and (d-c) < delta_portee+(e-d) and (e-d) < delta_portee+(b-a):
		rep = 1
	else:
		rep = 0
	return rep

#Groupe les résultats de la projection en portées
def groupe_portee(l,l2):
	if len(l) != 0:
		try:
			len(l)%5 != 0
			if test_cinq(l[0][1],l[1][1],l[2][1],l[3][1],l[4][1]) == 1:
				l2.append(l[:5])
				groupe_portee(l[5:],l2)
			else:
				groupe_portee(l[1:],l2)
		except:
			print "pas de portées correctes détectées"
			sys.exit(1)
	return l2

def projection_lignes(img):
	a = np.zeros(img.shape[0],np.int)
	l = []
	for i in range(img.shape[0]):
		for j in range(img.shape[1]):
			if img[i][j] == 0:
				a[i] = a[i] + 1
	#on ajoute les ordonnées
	for i in range(len(a)):
		l.append((a[i],i))
	return l

def maxi_locaux(a,img):
	l = []
	for i in range(2,len(a)-2):
		if a[i][0] > a[i-2][0] and a[i][0] > a[i-1][0] and a[i][0] >= a[i+1][0] and a[i][0] > a[i+2][0] and (3*a[i][0] > 2*img.shape[1]):
			l.append(a[i])
	#mod = len(l)%5
	#if mod != 0:
	#	for i in range(mod):
	#		l.remove(min(l))
	return l
	
def garde_ordonnees(liste):
	l2 = []
	for j in range(5):
		l = []
		for i in range(len(liste)):
			l.append(liste[i][j][1])
		l2.append(l)
	return l2

def ecart_moyen(liste):
	somme = 0
	compt = 0
	for i in range(len(liste)-1):
		for j in range(len(liste[i])):
			somme = abs(liste[i][j]-liste[i+1][j]) + somme
			compt = 1 + compt
	return somme/compt	

#trace les droites de pente zéro
def tracer_droite_hori(soluce,img):
	x = (0,img.shape[1])
	y = (soluce,soluce)
	plt.plot(x,y,color = 'blue')

def tracer_droite_hori_liste(liste,img):
	for elt in liste:
		for elt2 in elt:
			tracer_droite_hori(elt2,img)
