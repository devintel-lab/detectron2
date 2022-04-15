import PIL
import argparse
import json
import os.path as osp
import os

from PIL import Image

import filters
import random


def collage(box_dir, subsample=1., max_width_pixels=3000):
    files = [x for x in os.listdir(box_dir) if x.endswith(".jpg")]
    random.shuffle(files)
    files = files[:int(len(files)*subsample)]
    imgs = [Image.open(osp.join(box_dir, f)) for f in files]

    sorted_imgs = sorted(imgs, key=lambda x: x.size[1], reverse=True)

    # get max image width
    max_width = (0, None)
    for i in sorted_imgs:
        if i.size[0] > max_width[0]:
            max_width = (i.size[0], i)


    img_matrix = [[]]

    total_x_consumed = 0
    curr_row = 0
    for i in sorted_imgs:
        print()

    max_height = sorted_imgs[0].size[1]

    output = Image.new("RGB", (max_width_pixels, max_height*5))

    print()



if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--box_image_dir", type=str, required=True)
    parser.add_argument("--out_dir", type=str, required=False)
    parser.add_argument("--subsample", type=float, required=False, default=1.0)

    args = parser.parse_args()

    if not osp.isdir(args.out_dir):
        os.makedirs(args.out_dir)

    c = collage(args.box_image_dir, args.subsample)
