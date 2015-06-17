#!/usr/bin/python
# -*- coding: Utf-8 -*

"""Module portees_chgt_repere"""

#----------------------------------------------------------
# Importation des librairies

import numpy as np
from matplotlib import pylab as plt
from math import *


#----------------------------------------------------------
# Variables globales empiriques

#longueur max d'un intervalle de noir représentant une portée
seuil_portee = 2
#marge autorisée pour les distances entre les lignes de la portée
delta_portee = 2 
#marge autorisée entre les ordonnées des points d'une même ligne de portée
delta_dist = 5


#----------------------------------------------------------
# Fonctions

				
#cherche à détecter les morceaux noirs
def trouve_noir(img,col):
	memoire = 1
	l = []
	for x in range(img.shape[0]):
		if img[x][col] != memoire:
			#plt.plot(col,x-1,'ro')
			memoire = not memoire
			l.append(x-1)
	return l

#parcourt toute la matrice pour trouver les intervalles
def trouve_noir_matrice(img):
	l2 = []
	for x in range(img.shape[1]):
		l = trouve_noir(img,x)
		l2.append(l)
	return l2

#pour une liste donnée, regarde la distance entre deux valeurs consécutives, si elle est assez petite, c'est potentiellement une portée et on en prend le milieu sinon (valeurs isolées) on l'élimine
def les_milieux(l,l2):
	if (len(l) >= 2):
		if l[1]-l[0] > seuil_portee:
			les_milieux(l[1:],l2)
		else:
			l2.append((l[1]+l[0])/2)
			les_milieux(l[2:],l2)
	return l2

#pour toutes les listes d'intervalles noirs, on cherche les milieux et on élimine les points isolés
def les_milieux_liste_de_liste(liste):
	l = []
	for elt in liste:
		l.append(les_milieux(elt,[]))
	return l

def test_cinq(a,b,c,d,e):
	if (b-a) < delta_portee+(c-b) and (c-b) < delta_portee+(d-c) and (d-c) < delta_portee+(e-d) and (e-d) < delta_portee+(b-a):
		rep = 1
	else:
		rep = 0
	return rep

#les listes doivent représenter les portées donc elles doivent être composées de 5/10/15/... points successifs
# problème du bruit ??
def groupe_cinq_points(l,l2):
	if (len(l) >= 5):
		if test_cinq(l[0],l[1],l[2],l[3],l[4]) == 0:
			groupe_cinq_points(l[1:],l2)
		else:
			l2.append([l[0],l[1],l[2],l[3],l[4]])
			groupe_cinq_points(l[5:],l2)
	return l2

#Pour toutes les listes d'intervalles, on ne garde que les points de portée		
def groupe_cinq_points_liste_de_liste(liste):
	l = []
	for elt in liste:
		l.append(groupe_cinq_points(elt,[]))
	return l

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

#donne la première coordonnée de chaque portée (et l'abscisse)
def premiere_coordonnee_liste_de_liste(liste):
	l = []
	for elt in liste:
		l.append((elt[0],elt[5]))
	return l

#donne la deuxième coordonnée de chaque portée (et l'abscisse)
def deuxieme_coordonnee_liste_de_liste(liste):
	l = []
	for elt in liste:
		l.append((elt[1],elt[5]))
	return l

#donne la troisième coordonnée de chaque portée (et l'abscisse)
def troisieme_coordonnee_liste_de_liste(liste):
	l = []
	for elt in liste:
		l.append((elt[2],elt[5]))
	return l

#donne la quatrième coordonnée de chaque portée (et l'abscisse)
def quatrieme_coordonnee_liste_de_liste(liste):
	l = []
	for elt in liste:
		l.append((elt[3],elt[5]))
	return l

#donne la cinquième coordonnée de chaque portée (et l'abscisse)
def cinquieme_coordonnee_liste_de_liste(liste):
	l = []
	for elt in liste:
		l.append((elt[4],elt[5]))
	return l
	
#à partir d'une liste de coordonnées, on sépare les différentes portées (les unes en dessous des autres sur la partition)
def separe_les_portees(liste,l2):
	liste.sort()
	l = []
	r = 1
	if len(liste) > 0:
		for i in range(len(liste)-1):
			if (liste[i][0] > liste[i+1][0]+delta_dist) or (liste[i][0] < liste[i+1][0]-delta_dist):
				l2.append(liste[:i+1])
				liste = liste[i+1:]
				separe_les_portees(liste,l2)
				r = 0 #on ne finit pas la boucle
				break
			else:
				l.append(liste[i])
		if r != 0: #si on a fini la boucle
			l.append(liste[len(liste)-1])
			l2.append(l)
	return l2

def somme_ab_carre(liste):
	som = 0
	for elt in liste:
		som = elt[1]*elt[1] + som
	return som
	
def somme_ab(liste):
	som = 0
	for elt in liste:
		som = elt[1] + som
	return som
	
def somme_ab_ord(liste):
	som = 0
	for elt in liste:
		som = elt[0]*elt[1] + som
	return som
	
def somme_ord(liste):
	som = 0
	for elt in liste:
		som = elt[0] + som
	return som
	
def somme_ord_carre(liste):
	som = 0
	for elt in liste:
		som = elt[0]*elt[0] + som
	return som

#Somme des abscisses au carré = A
#Nombre de points = B
#Somme des abscisses = C
#Somme des abscisses fois ordonnées = D
#Somme des ordonnées = E
#Somme des ordonnées au carré= F
	
def calcul_abcdef(liste):
	a = somme_ab_carre(liste)
	b = len(liste)
	c = somme_ab(liste)
	d = somme_ab_ord(liste)
	e = somme_ord(liste)
	f = somme_ord_carre(liste)
	return (a,b,c,d,e,f)

def calcul_abcdef_plusieurs_listes(liste):
	l = []
	for elt in liste:
		l.append(calcul_abcdef(elt))
	return l

def delta(tup):
	d = tup[0]*tup[1] - tup[2]*tup[2]
	return d

def delta_m(tup):
	d = tup[3]*tup[1] - tup[4]*tup[2]
	return d

def delta_p(tup):
	d = tup[0]*tup[4] - tup[3]*tup[2]
	return d
	
def solution(tup):
	b = 0
	c = 0
	if delta(tup) != 0:
		b = float(float(delta_m(tup))/float(delta(tup)))
		c = float(float(delta_p(tup))/float(delta(tup)))
	return (b,c)
	
def solution_liste(liste):
	l = []
	for elt in liste:
		l.append(solution(elt))
	return l

def tracer_droite(soluce,img):
	x = (0,img.shape[1])
	y = (soluce[1],soluce[1]+soluce[0]*img.shape[1])
	plt.plot(x,y,color = 'blue')
	

def tracer_droite_liste(liste,img):
	for elt in liste:
			tracer_droite(elt,img)

#liste de listes de couples (pente,ordonnée à l'origine)
def moyenne_pentes(liste):
	somme = 0
	compt = 0
	for elt in liste:
		for elt2 in elt:
			somme = elt2[0] + somme
			compt = 1 + compt
	return somme/compt

#Ecart moyen entre les lignes d'une portée
def ecart_moyen(liste):
	somme = 0
	compt = 0
	for i in range(len(liste)-1):
		for j in range(len(liste[i])):
			somme = abs(liste[i][j][1]-liste[i+1][j][1]) + somme
			compt = 1 + compt
	return somme/compt



#effectue le changement de repère sur l'image
def changement_repere(img,pente):
	img2 = np.zeros(img.shape,np.int)
	if pente != 0:
		teta = -atan(pente) #le repère est "inversé"
		(x0,y0) = (img.shape[1]/2,img.shape[0]/2) #rotation depuis le milieu de l'image
		for i in range(img.shape[0]):
			for j in range(img.shape[1]):
				try:
					img2[i][j] = img[round((i-x0)*cos(teta)-(j-y0)*sin(teta)+x0)][round((i-x0)*sin(teta)+(j-y0)*cos(teta)+y0)]
				except: 0
	return img2

def remet_listes_cinq(liste):
	i=0
	l=[]
	while i < len(liste):
		l.append(liste[i:i+5])
		i=i+5
	return l
	
#donne les nouvelles valeurs des ordonnées à l'origine après changement de repère
def changement_de_repere_tableau(img,liste,pente):
	teta = -atan(pente)
	(x0,y0) = (img.shape[1]/2,img.shape[0]/2)
	u = []
	l = []
	for elt in liste:
		for elt2 in elt:
			a = round(-x0*sin(teta)+(elt2[1]-y0)*cos(teta)+y0)
			u.append(a)
	return remet_listes_cinq(u)

#trace les droites de pente zéro
def tracer_droite_hori(soluce,img):
	x = (0,img.shape[1])
	y = (soluce,soluce)
	plt.plot(x,y,color = 'blue')

def tracer_droite_hori_liste(liste,img):
	for elt in liste:
		for elt2 in elt:
			tracer_droite_hori(elt2,img)
