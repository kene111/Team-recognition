import cv2
import numpy as np
import os, json, random

import detectron2
from detectron2 import model_zoo
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2.utils.visualizer import Visualizer, ColorMode
from detectron2.data import MetadataCatalog, DatasetCatalog
from detector.utils.optical import Visualize
from detector.utils.helper import Model, Assistant
try:
    from detector.utils.sort import Sort
    
except:
    from detector.utils.sort import Sort


class ExtractPerson(object):

    def __init__(self, skip=False, skip_type="n_seconds"):
        self.skip = skip
        self.skip_type = skip_type
        self.model_weights = "/ps/challenge/detector/person_detector_1.pth"
        self.cfg_file = "/ps/challenge/detector/person_detector_output_1.yaml"
        self.video_path = "/ps/challenge/video/deepsort_30sec.mp4"
        self.model = Model(self.cfg_file, self.model_weights)
        self.assistant = Assistant()


    

    def extract_person(self):

        uniq_players = set()
        mot_tracker = Sort(max_age=1, min_hits=2, iou_threshold=0.11)
        video_handler = Visualize(skip=self.skip, skip_type=self.skip_type)
        model = self.model.init_model()

        video = cv2.VideoCapture(self.video_path)
        
        for frame in video_handler.run_on_video(video):

            pred = model(frame)
            dets = self.asistant.re_construct_predicton(pred) #output ==> [[x1,y1,x2,y2,scores], ... ] #numpy array
            track_bbs_ids = mot_tracker.update(dets) #output==> [[x1,y1,x2,y2,ID], ... ]

            for player_info in track_bbs_ids:
                temp = np.copy(frame)
                id_ = round(player_info[-1])

                if id_ not in uniq_players:
                
                    uniq_players.add(id_)
                    self.assistant.extract_n_save_person(temp, player_info[:-1],id_)



  