#!/usr/bin/python
# -*- coding: Utf-8 -*

"""Module reconnaissance de le clef"""

import cv2
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.pyplot as plt2
import warnings


def redimensionne_img(ecart,imgf,imgs,imgu):
	h = int(round(4*ecart))
	h2 = int(round(7*ecart))
	bf = int(round(19*h/34))
	bs = int(round(43*h2/103))
	bu = int(round(69*h/106))
	template_fa = cv2.resize(imgf,(bf,h))
	template_sol = cv2.resize(imgs,(bs,h2))
	template_ut = cv2.resize(imgu,(bu,h))
	return (template_fa,template_sol,template_ut)


def verifie_pertinence_clef(tab,pt,pt2):
	j = 0
	comp = 0
	rep = 0
	while j in range(len(tab[0])):
	
		for i in range(5):
			if tab[i][j] <= pt2 and tab[i][j] >= pt:
				comp = comp + 1
			if comp == 4:
				rep = 1
				break
				
		j = j + 1
		comp = 0
	return rep


#on cherche une unique occurence de la clef
def cherche_clef(img,temp,tab):
	rep = 0
	w,h = temp.shape[::-1]
	res = cv2.matchTemplate(img,temp,cv2.TM_CCOEFF_NORMED)
	min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
	
	#les clefs sont en début de partition (à bricoler)
	if (max_loc[0] < img.shape[0]/7) and (verifie_pertinence_clef(tab,max_loc[1],max_loc[1]+h) == 1):
		cv2.rectangle(img, max_loc, (max_loc[0] + w, max_loc[1] + h), 0, 2)
		rep = 1
	
	return img,rep

#on cherche plusieurs occurences de la clef
def cherche_clef2(img,temp):
	rep = 0
	w,h = temp.shape[::-1]
	res = cv2.matchTemplate(img,temp,cv2.TM_CCOEFF_NORMED)
	threshold = 0.6 #ce n'est pas un minimum mais plusieurs au-dessus d'un certain seuil, comment le déterminer ?
	loc = np.where(res >= threshold)
	for pt in zip(*loc[::-1]):
		if pt[0] < img.shape[0]/7:
			cv2.rectangle(img, pt, (pt[0] + w, pt[1] + h),0, 2)
			rep = 1
			
	return img,rep

"""

#plusieurs occurences
w,h = temp.shape[::-1]
	res = cv2.matchTemplate(img,temp,cv2.TM_CCOEFF_NORMED)
	threshold = 0.6 #ce n'est plus un minimum mais plusieurs au-dessus d'un certain seuil, comment le déterminer ?
	loc = np.where(res >= threshold)
	for pt in zip(*loc[::-1]):
		cv2.rectangle(img, pt, (pt[0] + w, pt[1] + h), 255, 2)
		
#si on ne cherche qu'une occurence
res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

cv2.rectangle(img_rgb, max_loc, (max_loc[0] + w, max_loc[1] + h), 255, 2)


b = 28
img = Image.open('images/clef_fa.jpg')
w = b/float(img.size[1])
h = int(float(w)*float(img.size[0]))
img = img.resize((h,b),Image.ANTIALIAS)

plt.imshow(img)
plt.show()

w,h = img.size

template = adaptors.PIL2Ipl(img)
print template

template = np.zeros(img.size)
for i in range(w):
	for j in range(h):
		template[i][j] = img[i][j]
"""
