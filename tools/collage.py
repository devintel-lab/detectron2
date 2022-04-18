import PIL
import argparse
import json
import os.path as osp
import os

from PIL import Image

import random


def collage(box_dir, subsample=1., max_width_pixels=1500):
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

    max_height = sorted_imgs[0].size[1]

    output = Image.new("RGB", (max_width_pixels, max_height*15))

    y_cursor = 0
    x_cursor = 0

    for i in sorted_imgs:
        output.paste(i, (x_cursor, y_cursor))
        x_cursor += i.size[0]
        if x_cursor > 0.90*max_width_pixels:
            x_cursor = 0
            y_cursor += i.size[1]

    output.save(osp.join(args.out_dir, f"{osp.basename(box_dir)}.jpg"))



if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--box_image_dir", type=str, required=True)
    parser.add_argument("--out_dir", type=str, required=False)
    parser.add_argument("--subsample", type=float, required=False, default=1.0)

    args = parser.parse_args()

    if not osp.isdir(args.out_dir):
        os.makedirs(args.out_dir)

    c = collage(args.box_image_dir, args.subsample)
