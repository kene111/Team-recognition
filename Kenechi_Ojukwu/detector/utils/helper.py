import numpy as np
from PIL import Image 
import detectron2
from detectron2.config import CfgNode, get_cfg
from detectron2.engine import DefaultPredictor

class Assistant(object):

    def __init__(self):
        self.output_path = '/ps/challenge/players/'

    
    def get_round_values_(self, listfloatvalues):
        value = []
        for i in listfloatvalues:
            value.append(round(i))
        return value

    def scale_bbox_(self, xmin,ymin,xmax,ymax,perc=100):
        "https://techoverflow.net/2021/04/26/how-to-make-bounding-box-larger-by-a-percentage-in-python/"

        n = (perc/2) * 0.01
        xmin -= n * (xmax - xmin)
        xmax += n * (xmax - xmin)
        ymin -= n * (ymax - ymin)
        ymax += n * (ymax - ymin)

        return [xmin,ymin,xmax,ymax]

    def re_construct_predicton(self, prediction):
        output = []
        instances = prediction["instances"]
        scores = instances.get_fields()["scores"].tolist()
        pred_boxes = instances.get_fields()["pred_boxes"].tensor.tolist()

        for i in range(len(scores)):
            boxes = self.get_round_values_(pred_boxes[i]) 
            scaled_bbox = self.scale_bbox_(*boxes)
            score = scores[i]
            scaled_bbox.append(score)
            output.append(scaled_bbox)
        return np.array(output)

    def extract_n_save_person(self, image, coor, name):
        
        image = Image.fromarray(image,mode='RGB')
        cropped_image = image.crop(coor)
        cropped_image.save( f'{self.output_path}{name}.jpg')
        return 

    
class Model(object):

    def __init__(self, cfg_file, model_weights):
        self.cfg_file = cfg_file
        self.model_weights = model_weights

    def setup_cfg_(self):
        cfg = CfgNode(new_allowed=True)
        cfg.merge_from_other_cfg(get_cfg())
        cfg.set_new_allowed(True)
        cfg.MODEL.DEVICE = 'cpu'
        cfgfile = self.cfg_file
        cfg.merge_from_file(cfgfile)
        cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.9
        cfg.MODEL.ROI_HEADS.NUM_CLASSES = 1
        cfg.MODEL.WEIGHTS = self.model_weights 
        
        return cfg

    def init_model(self):
        model = DefaultPredictor(self.setup_cfg_())
        return model