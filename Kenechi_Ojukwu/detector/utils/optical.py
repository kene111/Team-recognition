import sys
import cv2
import torch
import atexit
import bisect
import multiprocessing as mp
from collections import deque

from detectron2.data import MetadataCatalog
from detectron2.engine.defaults import DefaultPredictor
from detectron2.utils.video_visualizer import VideoVisualizer
from detectron2.utils.visualizer import ColorMode, Visualizer

#sys.path.append('/content/drive/MyDrive/ParallelScore/Person-Detector/')
from detector.utils.frameskip import  ImageSelector



classes = {0:"Player"}

label_list = list(classes.values())


class Visualize(object):

    def __init__(self, instance_mode=ColorMode.IMAGE, steps=100, f_count=None, skip=False, skip_type="n_seconds"):

        self.instance_mode = instance_mode
        self.steps = steps
        self.f_count = f_count
        self.skip = skip
        self.skip_type = skip_type


    def frame_from_video_(self, video):

        while video.isOpened():
            success, frame = video.read()
            if success:
                yield frame
            else:
                break


    def run_on_video(self, video):
        
        frame_gen = self.frame_from_video_(video)

        if self.skip:
            if self.skip_type == "n_frames":
                frame_master =  ImageSelector(n_steps=self.steps, frame_count=self.f_count)
                frame_gen = frame_master.extract_n_frames(frame_gen)

            else:
                fps = video.get(cv2.CAP_PROP_FPS)
                frame_master =  ImageSelector(n_steps=self.steps, frame_count=self.f_count)
                frame_gen = frame_master.extract_n_sec_frames(frame_gen, fps)
                
        
        
        
        for frame in frame_gen:
            yield frame 


