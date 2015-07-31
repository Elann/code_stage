#!/usr/bin/python
# -*- coding: Utf-8 -*

#----------------------------------------------------------
# Importation des librairies

from pymorph import *
from matplotlib import pylab as plt
import cv2
import sys
import warnings

from portees_chgt_repere import *
from fonctions_annexes import *
from barres_verticales import *
from notes_compacite import *
from reconnaissance_clef import *

#----------------------------------------------------------
# Importation des images

img0 = cv2.imread('images/partition20.jpg')
img0 = cv2.cvtColor(img0,cv2.COLOR_BGR2GRAY)

img_fa = cv2.imread('images/clef_fa2.jpg',0)
img_sol = cv2.imread('images/clef_sol.jpg',0)
img_ut = cv2.imread('images/clef_ut.jpg',0)

#----------------------------------------------------------
# Variables globales empiriques

#Nombre de croches
nbr_croches = 2

#Valeur minimale du critère de compacité acceptée
seuil_comp = 0.7
#Valeur minimale du critère de compacité acceptée
seuil_comp2 = 0.55

#----------------------------------------------------------
# Programme

#empêche les warning (apparus par magie) quand on ferme la fenêtre de pyplot
warnings.simplefilter("ignore")


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

#Vachement long si on trace les points rouges
l1 = trouve_noir_matrice(img)
l2 = les_milieux_liste_de_liste(l1)
l4 = groupe_cinq_points_liste_de_liste(l2)
l4b = ajoute_abscisse(l4)
l4t = liste_sans_liste_vide(l4b)
l5 = split_listes(l4t)

#On a les coordonnées des droites (5) de chaque portée (n)
lprem = premiere_coordonnee_liste_de_liste(l5)
lprem = separe_les_portees(lprem,[])
lsec = deuxieme_coordonnee_liste_de_liste(l5)
lsec = separe_les_portees(lsec,[])
lter = troisieme_coordonnee_liste_de_liste(l5)
lter = separe_les_portees(lter,[])
lqua = quatrieme_coordonnee_liste_de_liste(l5)
lqua = separe_les_portees(lqua,[])
lcin = cinquieme_coordonnee_liste_de_liste(l5)
lcin = separe_les_portees(lcin,[])


#on applique la méthode des moindres carrées pour trouver la droite de la portée

#On calcule les coefficients (A, B, C, D, E, F)
abcdef_prem = calcul_abcdef_plusieurs_listes(lprem)
abcdef_sec = calcul_abcdef_plusieurs_listes(lsec)
abcdef_ter = calcul_abcdef_plusieurs_listes(lter)
abcdef_qua = calcul_abcdef_plusieurs_listes(lqua)
abcdef_cin = calcul_abcdef_plusieurs_listes(lcin)

#On calcule les solutions (b,c) : (pente,ordonnée à l'origine)
solprem = solution_liste(abcdef_prem)
solsec = solution_liste(abcdef_sec)
solter = solution_liste(abcdef_ter)
solqua = solution_liste(abcdef_qua)
solcin = solution_liste(abcdef_cin)

#liste des listes de couples solutions
tab = [solprem,solsec,solter,solqua,solcin]

#A partir des équations, on trace les droites de chaque portée
tracer_droite_liste(solprem,img1)
tracer_droite_liste(solsec,img1)
tracer_droite_liste(solter,img1)
tracer_droite_liste(solqua,img1)
tracer_droite_liste(solcin,img1)

#On affiche l'image et les droites
plt.imshow(img1)
plt.gray()
plt.show()

moy = moyenne_pentes(tab)
try:
	e0 = ecart_moyen(tab)
except IndexError:
	print "erreur lors de la détection des portées"
	sys.exit(1)

#PERTINENT ?
#changement de repère
img2 = changement_repere(img1,moy)

#nouveau tracé des droites
tab2 = changement_de_repere_tableau(img1,tab,moy)
tracer_droite_hori_liste(tab2,img2)

plt.imshow(img2)
plt.show()

#détection des barres verticales
#on ne garde que les barres > 3*écart entre les lignes de portée
img3 = close(img2,seline(3*e0))

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
tracer_droite_hori_liste(tab2,img2)
plt.imshow(img2)
plt.show()

#événement magique qui garde les noires et les croches
cimg = cv2.medianBlur(img0,5)

#on passe en binaire (fait n'importe quoi avec le threshold Gaussien)
cimg = binary(cimg,100)
#cimg = imgbooltoint(cimg) (effet nul, pourquoi ?)
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

img5 = erode(img5,sedisk(1))

#Fond : 0, motifs : 1
img5a = inverse_0_1(img5)
#labellisation
img6 = label(img5a)

if e0 > 7:
	k = e0+2
else:
	k = e0-2

tableau = calcule_aires(img6,k)
tableau = calcule_perimetres(img6,tableau)

comp = calcule_compacite(tableau)
(n1,img7) = colorie_bons(img6,comp,seuil_comp)

#on vérifie que les barres verticales sont collées à une note
v8 = bv_collee_notes(v6,n1,e0)
#Listes de la forme [ord1,ord2,ab,ord_note ou 0]
v9 = liste_listes_note(v8)

# CROCHES

#on retire les notes (les croches sont rectangulaires ou ellipsoïdales)
img8 = enleve_notes(cimg,n1)
img8 = erode(img8,sedisk(1))

#on récupère les pixels noirs de l'image
n2 = recupere_points(img8)
#on trouve les croches simples
v10 = bv_collee_croche(v9,n2,e0,img8,1)
#on trouve les croches doubles/triples... 
n3 = existe_autre_croche(img8,v10,e0,nbr_croches)
#Listes de la forme [ord1,ord2,ab,ord_note ou 0, nbr_croches]
n4 = liste_listes_croche(n3)

#BLANCHES

#on retire les portées
img9 = enleve_portees_liste(img1,tab)
#on "referme" les blanches
img9 = open(img9,seline(7))
img9 = open(img9,seline(7,90))
img9 = open(img9,sedisk(3))
#on retire les barres verticales
img91 = close(img9,seline(3*e0))
img9 = soustraction_img(img9,img91)
#on grossit les notes
img9 = erode(img9,sedisk(1))

#Fond : 0, motifs : 1
img9a = inverse_0_1(img9)
#labellisation
img10 = label(img9a)

#Calcul de compacité
tableau2 = calcule_aires(img10,e0)
tableau2 = calcule_perimetres(img10,tableau2)
comp2 = calcule_compacite(tableau2)
(n12,img11) = colorie_bons(img10,comp2,seuil_comp2)

#plt.imshow(img11)
#plt.show()

#Listes de la forme [ord1,ord2,ab,ord_note ou 0, nbr_croches, ord_blanche ou 0]
nb = cherche_blanche(n4,n12,e0)
nb = liste_toutes_notes(nb)

# BARRES DE MESURE

n51 = barres_mesure(nb,e0)

# CLEF

#liste de n listes, n étant le nombre de portées
n5 = notes_par_portees(n51,tab2,e0)

#on adapte la taille des templates à celle de l'image
fa,sol,ut = redimensionne_img(e0,img_fa,img_sol,img_ut)

#on découpe l'image en portées pour les étudier une à une
list_img = decoupe_images_en_portees(tab2,img0)

# NOM DES NOTES

#abscisse de la note la plus à gauche
#on pourrait le calculer pour chaque portée... utile ?
one = ab_premiere_note(n51,img0)

#on trouve le nom des notes (noires, (doubles, triples) croches, blanches)
#la fonction cherche la clef de la portée à chaque fois
n6 = nom_notes(n5,tab2,e0,list_img,sol,fa,ut,one)

print n5
print e0

#affichage
img71 = inverse_0_1(img7)
trace_verticales_liste(v6)
tracer_droite_hori_liste(tab2,img2)
plt.imshow(img71)
plt.show()
