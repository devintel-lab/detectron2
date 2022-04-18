import argparse
import os
import os.path as osp
import json
from PIL import Image

def main(args):
    img_dir = args.image_dir

    dataset = []

    imgs = os.listdir(img_dir)

    for img_id, img_path in enumerate(imgs):
        img = Image.open(osp.join(img_dir, img_path))
        
        entry = {
            "file_name": osp.abspath(osp.join(img_dir, img_path)),
            "image_id": img_id,
            "width": img.width,
            "height": img.height,
            "annotations": []
        }

        dataset.append(entry)

    with open(osp.join(args.output_dir, f"{args.dataset_name}.json"), "w") as out:
        json.dump(dataset, out, indent=3)

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--image_dir")
    parser.add_argument("--dataset_name")
    parser.add_argument("--output_dir")

    args = parser.parse_args()

    main(args)