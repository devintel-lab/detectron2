from detectron2 import model_zoo
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2.utils.visualizer import Visualizer
from detectron2.data import MetadataCatalog, DatasetCatalog
import numpy as np
import os, json, cv2, random

import argparse
import os.path as osp

import sys
sys.path.append("../datasets")
import home15

def get_latest_weights(outdir):
    with open(osp.join(outdir, "last_checkpoint"), "r") as input:
        latest = input.read().strip()
        return latest

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config-file")
    args = parser.parse_args()

    cfg = get_cfg()
    cfg.merge_from_file(args.config_file)
    # cfg.merge_from_list(args.opts)
    

    latest_model = get_latest_weights(cfg.OUTPUT_DIR)

    cfg.MODEL.WEIGHTS = osp.join(cfg.OUTPUT_DIR, latest_model)  # path to the model we just trained
    cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.7   # set a custom testing threshold
    cfg.freeze()

    home_metadata = MetadataCatalog.get("home15_train")
    predictor = DefaultPredictor(cfg)

    dataset = home15.home_15_randomsample_inference_dataset()
    for d in random.sample(dataset, 3):    
        im = cv2.imread(d["file_name"])
        outputs = predictor(im)
        print(outputs)
        v = Visualizer(im[:, :, ::-1],
                   metadata=home_metadata, 
                   scale=0.5, 
                #    instance_mode=ColorMode.IMAGE_BW   # remove the colors of unsegmented pixels. This option is only available for segmentation models
        )
        out = v.draw_instance_predictions(outputs["instances"].to("cpu"))
        out.save(f"test_detections/{osp.basename(d['file_name'])}")
        print()