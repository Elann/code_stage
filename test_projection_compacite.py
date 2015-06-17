#!/usr/bin/python
# -*- coding: Utf-8 -*

#----------------------------------------------------------
# Importation des librairies

from pymorph import *
from matplotlib import pylab as plt
import cv2
import sys
import warnings

from portees_projection import *
from fonctions_annexes import *
from barres_verticales import *
from notes_compacite import *


#----------------------------------------------------------
# Importation de l'image

img0 = cv2.imread('images/partition8.jpg',0)

# si problème avec la fonction qui grise :  as_grey=True (ne garantit pas des entiers)

#empêche les warning (apparus par magie) quand on ferme la fenêtre de pyplot
warnings.simplefilter("ignore")

#----------------------------------------------------------
# Programme

img1 = cv2.adaptiveThreshold(img0,1,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,21,2)

plt.imshow(img1)
plt.gray()
plt.show()

#on supprime les composantes connexes de trop petite taille
img1 = areaclose(img1,2000)

plt.imshow(img1)
plt.show()

#on supprime tout ce qui n'est pas barre horizontal (à quelques degrés près)
a = 7
img2 = close(img1,seline(a,90))
img3 = close(img1,seline(a,89))
img4 = close(img1,seline(a,88))
img5 = close(img1,seline(a,87))
img6 = close(img1,seline(a,91))
img7 = close(img1,seline(a,92))
img8 = close(img1,seline(a,93))
img9 = close(img1,seline(a,94))

img = union(img2,img3,img4,img5,img6,img7,img8,img9)
plt.imshow(img)
plt.show()

#On projette sur l'axe des ordonnées pour trouver les portées
l = projection_lignes(img)
l1 = maxi_locaux(l,img)
l2 = groupe_portee(l1,[])
#Ordonnées à l'origine de toutes les portées [[ligne1],[ligne2],...,[ligne5]]
l3 = garde_ordonnees(l2)

#on affiche l'image et les droites
tracer_droite_hori_liste(l3,img)
plt.imshow(img)
plt.show()

try:
	e0 = ecart_moyen(l3)
except IndexError:
	print "erreur lors de la détection des portées"
	sys.exit(1)

#détection des barres verticales
#on ne garde que les barres > 3*écart entre les lignes de portée
img3 = close(img1,seline(3*e0))
plt.imshow(img3)
plt.show()

v1 = trouve_barres_verticales(img3)
#v2 = garde_longues_barres_liste_de_liste(v1,3*e0)
v3 = groupe_deux_points_liste_de_liste(v1)
v4 = ajoute_abscisse(v3)
v4b = liste_sans_liste_vide(v4)
v5 = split_listes(v4b)
v6 = supprime_barres_trop_proches(v5)

trace_verticales_liste(v6)
tracer_droite_hori_liste(l3,img1)
plt.imshow(img1)
plt.show()

#événement magique qui garde les noires et les croches
cimg = cv2.medianBlur(img0,5)

#on passe en binaire (fait n'importe quoi avec le threshold Gaussien)
cimg = binary(cimg,100)
#cimg = imgbooltoint(cimg) (effet nul, pourquoi ?)

#trace_verticales_liste(v6)
plt.imshow(cimg)
plt.show()

#on enleve les barres ~horizontales possiblement restantes
b = 2*e0 #taille suivant les images !
img52 = close(cimg,seline(b,90))
img53 = close(cimg,seline(b,89))
img54 = close(cimg,seline(b,88))
img55 = close(cimg,seline(b,91))
img56 = close(cimg,seline(b,92))
img57 = close(cimg,seline(b,93))
img58 = close(cimg,seline(b,87))
img59 = close(cimg,seline(b,86))
img60 = close(cimg,seline(b,94))
img61 = close(cimg,seline(b,0))
img62 = union(img52,img53,img54,img55,img56,img57,img58,img59,img60)

img5 = soustraction_img(cimg,img62)
img5 = soustraction_img(img5,img61)

#labellisation
img5a = inverse_0_1(img5)
img6 = label(img5a)

plt.imshow(img6)
plt.show()

tab = calcule_aires(img6)
tab = calcule_perimetres(img6,tab)

comp = calcule_compacite(tab)
(bons_points,img7) = colorie_bons(img6,comp)

#on transforme les barres verticales en série de pixels
v7 = extrait_pixels(v6)
#on vérifie que les barres verticales sont collées à une note
v8 = bv_collee_notes(v7,bons_points)
v9 = suppr_points_inutiles(v8)

trace_verticales_liste(v6)
tracer_droite_hori_liste(l3,img7)
affiche_points(v9)
plt.imshow(neg(img7))
plt.show()
