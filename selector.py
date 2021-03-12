import cv2 
import numpy as np
import pandas as pd
from PIL import Image 

img = cv2.imread("square.png")
clean_img = img.copy()

#variables iniciales 
ix = -1
iy = -1
dragging = False

#funcionamiento del drag-draw
def drag_rectangle(event, x, y, flags, param): 
	
	global ix, iy, dragging, img, clean_img
	
	if event == cv2.EVENT_LBUTTONDOWN: 
		dragging = True
		ix = x 
		iy = y 
			
	elif event == cv2.EVENT_MOUSEMOVE: 
		if dragging == True:
			#uso una copia limpia de la imagen para dibujarle encima
			img = clean_img.copy()
			cv2.rectangle(img, pt1 =(ix, iy), 
						pt2 =(x, y), 
						color =(0, 255, 0), 
						thickness = 2) 
	
	#cuando se deja de dibujar (se levanta el mouse) da la info pedida
	elif event == cv2.EVENT_LBUTTONUP: 
		dragging = False
		cv2.rectangle(img, pt1 =(ix, iy), 
					pt2 =(x, y), 
					color =(0, 255, 0), 
					thickness = 2)
		#obtengo el sample, me fijo de que lado vino la seleccion
		if(y<iy):
			aux = y
			y = iy
			iy = aux
		if(x<ix):
			aux = x
			x = ix
			ix = aux
		sample = clean_img[iy:y, ix:x]

		#busca el mean de cada canal cromatico RGB
		average = sample.mean(axis=0).mean(axis=0)
		average = average.astype(int)
		RGB = (average[0], average[1], average[2])
		pixels = abs((x - ix)*(y - iy))
		print(pixels)
		print(RGB)

		#muestro el color promedio
		pixel = Image.new(mode = "RGB", size = (100,100), color = RGB)
		pixel.show()


#abrir ventana aparte para dibujar sobre imagen
cv2.namedWindow(winname = "Selected Image") 
cv2.setMouseCallback("Selected Image", 
					drag_rectangle) 

while True: 
	cv2.imshow("Selected Image", img) 

	#Sale al apretar esc
	if cv2.waitKey(20) == 27: 
		break

cv2.destroyAllWindows() 
