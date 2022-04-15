import json
import os.path as osp

def home_15_train_dataset():
    print(osp.join(osp.dirname(__file__), "home15_train.json"))
    with open(osp.join(osp.dirname(__file__), "home15_train.json"), "r") as input:
        data = json.load(input)
        return data

def home_15_test_dataset():
    with open(osp.join(osp.dirname(__file__), "home15_test.json"), "r") as input:
        data = json.load(input)
        return data

def home_15_fulltrain_dataset():
    with open(osp.join(osp.dirname(__file__), "home15.json"), "r") as input:
        data = json.load(input)
        return data


from detectron2.data import DatasetCatalog
DatasetCatalog.register("home15_train", home_15_train_dataset)
DatasetCatalog.register("home15_test", home_15_test_dataset)
DatasetCatalog.register("home15_fulltrain", home_15_fulltrain_dataset)

home15_classes = ["bison", "alligator", "drop", "kettle",
                  "koala", "lemon", "mango", "moose",
                  "pot", "seal", "pot_yellow", "pot_black"]

from detectron2.data import MetadataCatalog
from detectron2.evaluation import COCOEvaluator

MetadataCatalog.get("home15_train").set(thing_classes = home15_classes)
MetadataCatalog.get("home15_test").set(thing_classes = home15_classes)
MetadataCatalog.get("home15_fulltrain").set(thing_classes = home15_classes)

MetadataCatalog.get("home15_train").set(evaluator_type="coco")
MetadataCatalog.get("home15_test").set(evaluator_type="coco")
MetadataCatalog.get("home15_fulltrain").set(evaluator_type="coco")