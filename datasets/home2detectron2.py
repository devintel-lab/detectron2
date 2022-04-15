import argparse
import os
import os.path as osp
import json
from PIL import Image
import random

def convert_coordinates(box, w, h):
    box[0] = box[0] * w
    box[1] = box[1] * h
    box[2] = box[2] * w
    box[3] = box[3] * h

    # convert from center coordinates to edges
    box[0] = box[0] - box[2]/2
    box[1] = box[1] - box[3]/2

    box_w = abs(box[2] - box[0])
    box_h = abs(box[3] - box[1])

    return box, box_w, box_h

def read_label_file(path):
    result = []
    with open(path) as input:
        for line in input:
            line = line.strip()
            if not line:
                continue
            vals = line.split()
            ctg = int(vals[0])
            box = [float(x) for x in vals[1:]]
            result.append([ctg]+box)
    return result


def main(args):
    img_dir = osp.join(args.data_dir, "JPEGImages")
    label_dir = osp.join(args.data_dir, "labels")

    dataset = []

    imgs = os.listdir(img_dir)

    for img_id, img_path in enumerate(imgs):
        img = Image.open(osp.join(img_dir, img_path))
        label_file = osp.join(label_dir, img_path.replace(".jpg", ".txt"))
        labels = read_label_file(label_file)
        if len(labels) == 0:
            continue
        

        entry = {
            "file_name": osp.abspath(osp.join(img_dir, img_path)),
            "image_id": img_id,
            "width": img.width,
            "height": img.height,
            "annotations": []
        }

        for l in labels:
            bbox, box_w, box_h = convert_coordinates(l[1:], w=img.width, h=img.height)
            entry['annotations'].append({
                'bbox': bbox,
                "bbox_mode": 1, # XYWH_ABS
                "category_id": l[0]
            })

        dataset.append(entry)

    return dataset

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--data_dir", default="home15")
    parser.add_argument("--test_pct", default=10)
    
    args = parser.parse_args()

    dataset = main(args)
    random.shuffle(dataset)


    num_test = int(len(dataset) * args.test_pct/100)

    test = dataset[:num_test]
    train = dataset[num_test:]

    with open(args.data_dir+"_train.json", "w") as out:
        json.dump(train, out, indent=3)

    with open(args.data_dir+"_test.json", "w") as out:
        json.dump(test, out, indent=3)