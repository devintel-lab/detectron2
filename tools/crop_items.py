import argparse
import json
import os.path as osp
import os

from PIL import Image


def main(args):
    with open(args.coco_instances_file, "r") as input:
        detections = json.load(input)
    with open(args.bbox_file, "r") as input:
        boxes = json.load(input)

        boxes['annotations'] = detections
       

        img_dict = {x['id']: x['file_name'] for x in boxes['images']}
        for annot in boxes['annotations']:
            if annot['score'] < 0.7:
                continue
            img_path = img_dict[annot['image_id']]
            cat = annot['category_id']
            orig_img = Image.open(img_path)
        
            cropped = orig_img.crop((annot['bbox'][0], annot['bbox'][1],
                                     annot['bbox'][0] + annot['bbox'][2], annot['bbox'][1] + annot['bbox'][3]))
            cat_dir = osp.join(args.output_dir, str(cat))
            if not osp.isdir(cat_dir):
                os.mkdir(cat_dir)
            fname = osp.basename(img_path).replace(".jpg", f"_itemcrop{cat}.jpg")
            cropped.save(osp.join(cat_dir, fname))
            


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--bbox_file")
    parser.add_argument("--coco_instances_file")
    parser.add_argument("--output_dir")

    args = parser.parse_args()


    main(args)