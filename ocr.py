import os
import easyocr
import cv2
import numpy as np
from tkinter.filedialog import askdirectory
from tkinter import *

class TextExtractor:

	def __init__(self):

		self.reader = easyocr.Reader(['en'])
		self.get_all_images()

	def get_all_images(self):

		
		root = Tk()
		root.withdraw()
		self.image_direct = []
		self.directory= askdirectory()
		root.destroy()
		for name in os.listdir(self.directory):
			if name.endswith("jpg") or name.endswith("png") or name.endswith("jpeg"):
				self.image_direct.append(self.directory+"/"+name)

		self.get_text()



	def get_text(self):
		self.result_list = []
		for direct in self.image_direct:
			img = cv2.imread(direct)
			self.result_list.append(self.reader.readtext(img))
		self.write_text()

	def write_text(self):
		font = cv2.FONT_HERSHEY_TRIPLEX
		dr = 0
		for i in self.result_list:
			direct = self.image_direct[dr]
			img = cv2.imread(direct)
			for j in range(len(i)):            #loop for making squares
				top_left = i[j][0][0]
				bottom_right = i[j][0][2]
				try:
					img = cv2.rectangle(img,top_left,bottom_right,(0,0,255),2)
				except:
					continue
			
			for k in range(len(i)):          #loop for marking text
				top_left = i[k][0][0]
				bottom_right = i[k][0][2]
				text = i[k][1]
				try:
					img = cv2.putText(img,text,bottom_right,font , 0.6,(0,145,29),1,cv2.LINE_AA)
				except:
					continue
			dirr = os.getcwd()+"\\License Outputs\\"+direct.split("/")[-1].split('.')[0]+".png"
			cv2.imwrite(dirr, img)
			dr += 1



			
if __name__ == "__main__":

	
	ocr_obj = TextExtractor()
	print("Completed")
	


