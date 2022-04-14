import cv2
import os
import numpy as np
import re


class GreenDot:

    def __init__(self):
        self.stats = []
        self.frames = []
        self.outs = []
        self.t = 0
        self.get_frames()
    
    def get_frames(self):

        vidcap = cv2.VideoCapture('Video 1.mp4')
        success,image = vidcap.read()
        self.count = 0
        while success:
            self.frames.append(image)  
            success,image = vidcap.read()
            self.count += 1

        print(f"total frames: {self.count}")

        self.create_mask_hsv()

    def create_mask_hsv(self):

        for h in self.frames:

            hsv = cv2.cvtColor(h, cv2.COLOR_BGR2HSV)
        
            lower_green = np.array([30,65,100])
            upper_green = np.array([90,230,255])
        
            mask = cv2.inRange(hsv, lower_green, upper_green)           

            self.find_countours(mask)

        self.add_red_dot()

    def find_countours(self,mask):
        ret,thresh = cv2.threshold(mask,127,255,cv2.THRESH_BINARY)
        connectivity = 4
        output = cv2.connectedComponentsWithStats(thresh, connectivity, cv2.CV_32S)
        self.stats.append(output[2])
        

    def add_red_dot(self):

        cursor = 0

        for b in self.frames:

            stats = self.stats[cursor]

            for i in stats:
                l = []
                if i[4]<130 or i[4] > 10000:
                    continue
                l.append(int(i[0]+(i[2]/2)))
                l.append(int(i[1]+(i[3]/2))) 
                b = cv2.circle(b,l,int(i[4]*4/100),(0,0,255),-1)

            self.outs.append(b)
            cursor += 1

        self.frame_compile()

    def frame_compile(self):

    
        img = self.outs[0]
        height, width, layers = img.shape
        size = (width,height)
         
        out = cv2.VideoWriter('Output1.mp4',cv2.VideoWriter_fourcc(*'mp4v'),30, size)
         
        for i in self.outs:
            out.write(i)
        out.release()


if __name__ == "__main__":

    prg = GreenDot()
    print("Completed")