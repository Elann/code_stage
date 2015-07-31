#!/usr/bin/python
# -*- coding: Utf-8 -*

"""
	Module portees_chgt_repere
"""

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

"""
	On cherche les intervalles de pixels noirs
	pour une colonne d'une image donnée
"""
def trouve_noir(img,col):
	memoire = 1
	l = []
	for x in range(img.shape[0]):
		if img[x][col] != memoire:
			#plt.plot(col,x-1,'ro')
			memoire = not memoire
			l.append(x-1)
	return l

"""
	Pour chaque colonne de l'image en argument
	on cherche les intervalles de pixels noirs
"""
def trouve_noir_matrice(img):
	l2 = []
	for x in range(img.shape[1]):
		l = trouve_noir(img,x)
		l2.append(l)
	return l2

"""
	Pour la liste en argument
	on regarde la distance entre deux valeurs consécutives
	si elle est assez petite c'est potentiellement une portée
	et on en prend le milieu
	sinon (valeurs isolées) on l'élimine
"""
def les_milieux(l,l2):
	if (len(l) >= 2):
		if l[1]-l[0] > seuil_portee:
			les_milieux(l[1:],l2)
		else:
			l2.append((l[1]+l[0])/2)
			les_milieux(l[2:],l2)
	return l2

"""
	pour toutes les listes d'intervalles noirs
	on cherche les milieux et on élimine les points isolés
"""
def les_milieux_liste_de_liste(liste):
	l = []
	for elt in liste:
		l.append(les_milieux(elt,[]))
	return l

"""
	Les cinq ordonnées en argument forment une portée
	si la distance qui les sépare deux à deux reste constante
"""
def test_cinq(a,b,c,d,e):
	if (b-a) < delta_portee+(c-b) and (c-b) < delta_portee+(d-c) and (d-c) < delta_portee+(e-d) and (e-d) < delta_portee+(b-a):
		rep = 1
	else:
		rep = 0
	return rep

"""
	On vérifie que la liste en argument
	contient une ou plusieurs portées
	qu'on sépare dans le cas de plusieurs
"""
def groupe_cinq_points(l,l2):
	if (len(l) >= 5):
		if test_cinq(l[0],l[1],l[2],l[3],l[4]) == 0:
			groupe_cinq_points(l[1:],l2)
		else:
			l2.append([l[0],l[1],l[2],l[3],l[4]])
			groupe_cinq_points(l[5:],l2)
	return l2

"""
	Pour toutes les listes de la liste en argument
	on ne garde que celles représentant une ou plusieurs portées
"""	
def groupe_cinq_points_liste_de_liste(liste):
	l = []
	for elt in liste:
		l.append(groupe_cinq_points(elt,[]))
	return l

"""
	Pour chaque liste de la liste en argument
	on ajoute l'abscisse (le numéro de la liste) en queue
"""
def ajoute_abscisse(liste):
	for i in range(len(liste)):
		if len(liste[i]) > 0:
			for elt in liste[i]:
				elt.append(i)
	return liste

"""
	De la liste composée de listes passée en argument
	on retire les listes vides
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
	Donne la première ordonnée et l'abscisse
	de chaque portée de la liste
"""
def premiere_coordonnee_liste_de_liste(liste):
	l = []
	for elt in liste:
		l.append((elt[0],elt[5]))
	return l

"""
	Donne la deuxième ordonnée et l'abscisse
	de chaque portée de la liste
"""
def deuxieme_coordonnee_liste_de_liste(liste):
	l = []
	for elt in liste:
		l.append((elt[1],elt[5]))
	return l

"""
	Donne la troisième ordonnée et l'abscisse
	de chaque portée de la liste
"""
def troisieme_coordonnee_liste_de_liste(liste):
	l = []
	for elt in liste:
		l.append((elt[2],elt[5]))
	return l

"""
	Donne la quatrième ordonnée et l'abscisse
	de chaque portée de la liste
"""
def quatrieme_coordonnee_liste_de_liste(liste):
	l = []
	for elt in liste:
		l.append((elt[3],elt[5]))
	return l

"""
	Donne la cinquième ordonnée et l'abscisse
	de chaque portée de la liste
"""
def cinquieme_coordonnee_liste_de_liste(liste):
	l = []
	for elt in liste:
		l.append((elt[4],elt[5]))
	return l
	
"""
	A partir d'une liste de coordonnées
	on sépare les différentes portées
	les unes en dessous des autres sur la partition
"""
def separe_les_portees(liste,l2):
	liste.sort()
	l = []
	r = 1
	if len(liste) > 0:
		for i in range(len(liste)-1):
			#si la liste en i est trop éloignée de la liste en i+1
			#elles font partie de portées différentes
			if (liste[i][0] > liste[i+1][0]+delta_dist) or (liste[i][0] < liste[i+1][0]-delta_dist):
				l2.append(liste[:i+1])
				liste = liste[i+1:]
				#on recommence
				separe_les_portees(liste,l2)
				r = 0 #on ne finit pas la boucle
				break
			else:
				l.append(liste[i])
		if r != 0: #si on a fini la boucle
			l.append(liste[len(liste)-1])
			l2.append(l)
	return l2

"""
	A partir d'une liste de coordonnées
	on fait la somme des abscisses au carré
"""
def somme_ab_carre(liste):
	som = 0
	for elt in liste:
		som = elt[1]*elt[1] + som
	return som

"""
	A partir d'une liste de coordonnées
	on fait la somme des abscisses
"""	
def somme_ab(liste):
	som = 0
	for elt in liste:
		som = elt[1] + som
	return som

"""
	A partir d'une liste de coordonnées
	on fait la somme des ordonnées fois les abscisses
"""	
def somme_ab_ord(liste):
	som = 0
	for elt in liste:
		som = elt[0]*elt[1] + som
	return som

"""
	A partir d'une liste de coordonnées
	on fait la somme des ordonnées
"""
def somme_ord(liste):
	som = 0
	for elt in liste:
		som = elt[0] + som
	return som

"""
	A partir d'une liste de coordonnées
	on fait la somme des ordonnées au carré
"""
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

"""
	Calcule les éléments nécessaires à la méthode des moindres carrés
	Somme des abscisses au carré = A
	Nombre de points = B
	Somme des abscisses = C
	Somme des abscisses fois ordonnées = D
	Somme des ordonnées = E
	Somme des ordonnées au carré= F
"""
def calcul_abcdef(liste):
	a = somme_ab_carre(liste)
	b = len(liste)
	c = somme_ab(liste)
	d = somme_ab_ord(liste)
	e = somme_ord(liste)
	f = somme_ord_carre(liste)
	return (a,b,c,d,e,f)

"""
	Pour chaque liste de la liste en argument
	on calcule A,B,C,D,E et F
"""
def calcul_abcdef_plusieurs_listes(liste):
	l = []
	for elt in liste:
		l.append(calcul_abcdef(elt))
	return l

"""
	On calcule le delta de la méthode des moindres carrés
	à partir d'un tuple (A,B,C,D,E,F)
"""
def delta(tup):
	d = tup[0]*tup[1] - tup[2]*tup[2]
	return d

"""
	On calcule le delta m de la méthode des moindres carrés
	à partir d'un tuple (A,B,C,D,E,F)
"""
def delta_m(tup):
	d = tup[3]*tup[1] - tup[4]*tup[2]
	return d

"""
	On calcule le delta p de la méthode des moindres carrés
	à partir d'un tuple (A,B,C,D,E,F)
"""
def delta_p(tup):
	d = tup[0]*tup[4] - tup[3]*tup[2]
	return d
	
"""
	Pour un tuple (A,B,C,D,E,F)
	on calcule l'ordonnée à l'origine et la pente
	de la droite solution
"""
def solution(tup):
	b = 0
	c = 0
	if delta(tup) != 0:
		b = float(float(delta_m(tup))/float(delta(tup)))
		c = float(float(delta_p(tup))/float(delta(tup)))
	return (b,c)

"""
	Pour une liste de tuples (A,B,C,D,E,F)
	on calcule à chaque fois la droite solution
"""
def solution_liste(liste):
	l = []
	for elt in liste:
		l.append(solution(elt))
	return l

"""
	A partir du couple (pente,ordonnée à l'origine)
	on trace la droite correspondante
"""
def tracer_droite(soluce,img):
	x = (0,img.shape[1])
	y = (soluce[1],soluce[1]+soluce[0]*img.shape[1])
	plt.plot(x,y,color = 'blue')
	
"""
	Pour chaque droite de la liste
	on la trace
"""
def tracer_droite_liste(liste,img):
	for elt in liste:
			tracer_droite(elt,img)

"""
	A partir des couples solutions représentant les droites
	on calcule la pente moyenne
"""
def moyenne_pentes(liste):
	somme = 0
	compt = 0
	for elt in liste:
		for elt2 in elt:
			somme = elt2[0] + somme
			compt = 1 + compt
	return somme/compt

"""
	A partir des couples solutions représentant les droites
	on calcule l'écart moyen entre les lignes d'une même portée
"""
def ecart_moyen(liste):
	somme = 0
	compt = 0
	for i in range(len(liste)-1):
		for j in range(len(liste[i])):
			somme = abs(liste[i][j][1]-liste[i+1][j][1]) + somme
			compt = 1 + compt
	return somme/compt


"""
	A partir de la pente moyenne des droites des portées
	on calcule l'angle de la rotation
	nécessaire pour que les portées de la partition
	soient horizontales
	on effectue le changement de repère sur l'image
"""
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

"""
	On met le contenu de la liste en argument
	sous la forme de cinq listes
	correspondant aux cinq portées
"""
def remet_listes_cinq(liste):
	i=0
	l=[]
	gr = len(liste)/5
	while i < len(liste):
		l.append(liste[i:i+gr])
		i=i+gr
	return l
	
"""
	On donne les nouvelles valeurs des ordonnées à l'origine
	des droites des portées
	après le changement de repère
"""
def changement_de_repere_tableau(img,liste,pente):
	teta = -atan(pente)
	(x0,y0) = (img.shape[1]/2,img.shape[0]/2)
	u = []
	for elt in liste:
		for elt2 in elt:
			a = round(-x0*sin(teta)+(elt2[1]-y0)*cos(teta)+y0)
			u.append(a)
	return remet_listes_cinq(u)

"""
	On trace la droite de pente zéro
	et d'ordonnée à l'origine donnée
"""
def tracer_droite_hori(soluce,img):
	x = (0,img.shape[1])
	y = (soluce,soluce)
	plt.plot(x,y,color = 'blue')

"""
	Pour chaque droite de la liste
	on la trace
"""
def tracer_droite_hori_liste(liste,img):
	for elt in liste:
		for elt2 in elt:
			tracer_droite_hori(elt2,img)
