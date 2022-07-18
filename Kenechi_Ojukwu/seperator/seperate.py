import os
import cv2
import numpy as np
from PIL import Image
from collections import Counter
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from skimage.color import rgb2lab, deltaE_cie76



class PlayerSeparator(object):

    def __init__(self, output_file=None):

        if output_file:
            self.output_file = output_file
            os.makedirs(f"{self.output_file}/TEAMS/BLUE/")
            os.makedirs(f"{self.output_file}/TEAMS/YELLOW/")
        else:
            raise 'Please pass in an output file path'
        
       
        

    def get_image_(self, image_path):
        image = Image.open(image_path) 
        image = np.asarray(image)
        image = image[:,:, ::-1]   
        return image

    def get_colors_(self, image, number_of_colors):
        modified_image = cv2.resize(image, (128, 128), interpolation = cv2.INTER_AREA)
        modified_image = modified_image.reshape(modified_image.shape[0]*modified_image.shape[1], 3)
        clf = KMeans(n_clusters = number_of_colors)
        labels = clf.fit_predict(modified_image)
        counts = Counter(labels)

        center_colors = clf.cluster_centers_
        # We get ordered colors by iterating through the keys
        ordered_colors = [center_colors[i] for i in counts.keys()]
        rgb_colors = [ordered_colors[i] for i in counts.keys()]


        return rgb_colors

    def match_image_by_color_(self, image, color, threshold = 60, number_of_colors = 10): 
    
        image_colors = self.get_colors_(image, number_of_colors, False)
        selected_color = rgb2lab(np.uint8(np.asarray([[color]])))

        select_image = False
        for i in range(number_of_colors):
            curr_color = rgb2lab(np.uint8(np.asarray([[image_colors[i]]])))
            diff = deltaE_cie76(selected_color, curr_color)
            if (diff < threshold):
                select_image = True
        
        return select_image

    def save_yellow_players_(self,images, color, threshold, colors_to_match):

        for i in range(len(images)):
            selected = self.match_image_by_color_(images[i], color[1], threshold, colors_to_match)
            if selected:
                image = Image.fromarray(images[i])#,mode='RGB')
                image.save( f'{self.output_file}/TEAMS/{color[0]}/{i}.jpg')


    def save_blue_players_(self, images, color):

        for i in range(len(images)):

            is_yellow = self.match_image_by_color_(images[i], [255, 255, 0], 60, 7)

            if is_yellow:
                pass
            else:

                hsv_image= cv2.cvtColor(images[i],cv2.COLOR_BGR2HSV)

                mask = cv2.inRange(hsv_image, (50,0,0), (255, 50, 50))
                pixels = cv2.countNonZero(mask)

                if pixels > 0:
                    image = Image.fromarray(images[i],mode='RGB')
                    image.save( f'{self.output_file}/TEAMS/{color}/{i}.jpg')


    def get_image_path_(self, diir):
        pictures = []
        for picture in os.listdir(diir) :
            if picture != 'Thumbs.db':
                pictures.append(diir + picture)
        return pictures


    def seperate_players(self, diir):

        COLORS = {
            'YELLOW': ('YELLOW',[255, 255, 0])
        }

        images = []
        image_paths = self.get_image_path_(diir)

        for image in image_paths:
            images.append(self.get_image_(image))

        self.save_yellow_players_(images, COLORS['YELLOW'], 60, 7)
        self.save_blue_players_(images, 'BLUE')

    