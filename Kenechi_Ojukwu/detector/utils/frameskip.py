import cv2
import numpy as np

class ImageSelector(object):
    
    def __init__(self,n_steps=100, frame_count= None):

        self.n_steps = n_steps
        self.frame_count = frame_count
        
    
    def get_frames_(self,frames):
        local_frames = []
        for idx , frame in enumerate(frames):
            local_frames.append(frame)
        return local_frames

    def get_n_step_frames_(self,local_frames):
        assert self.n_steps < len(local_frames)-1,f"The number of steps you picked is greater than the number of frames available: There are {len(local_frames)} number frames."
        return [i for i in range(0,len(local_frames)-1,self.n_steps)]


    def frames_btw_steps_(self,steps):
        all_nodes = []

        if self.frame_count  is None:
            self.frame_count = len(self.n_steps)/6

        for i in range(len(steps)):
            if i == len(steps)-1:
                continue
            else:
                all_nodes.extend([i for i in range(steps[i], steps[i+1],self.frame_count)])
        return all_nodes


    def select_frames_per_second_(self,frames, fps):
        seg_ = []
        temp_ = []
        fps = int(fps)
        count = 0

        for i in range(len(frames)-1):
            temp_.append(i)

            if count == fps:
                seg_.append(temp_)
                count = 0
                temp_ = []
            count += 1

        return seg_

    def collect_frame_per_n_frames_(self,list_frames):
        final_frames = []

        for frames in list_frames:
            final_frames.append(frames[0])
        return final_frames


    def extract_n_frames(self, frames):

        local_frames = self.get_frames_(frames)
        final_frames = self.frames_btw_steps_(self.get_n_step_frames_(local_frames))

        print(f'The number of frames have been reduced from {len(local_frames)-1} to {len(final_frames)}.')

        for i in final_frames:
            yield local_frames[i]

        


    def extract_n_sec_frames(self, frames, fps):

        local_frames = self.get_frames_(frames)
        lis_fps = self.select_frames_per_second_(local_frames, fps)
        final_frames = self.collect_frame_per_n_frames_(lis_fps)

        print(f'The number of frames have been reduced from {len(local_frames)-1} to {len(final_frames)}.')

        for i in final_frames:
            yield local_frames[i]

        
        




