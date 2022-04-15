import argparse
import json
import os.path as osp
import os

from PIL import Image

# import filters


# def crop_boxes(boxes, frame_dir, out_dir=None):
#     for f, bs in boxes.items():
#         img_path = osp.join(frame_dir, f)
#         orig_img = Image.open(img_path)
#         for cat, box in bs.items():
#             cropped = orig_img.crop((box['bbox'][0], box['bbox'][1],
#                                      box['bbox'][0] + box['bbox'][2], box['bbox'][1] + box['bbox'][3]))
#             cat_dir = osp.join(out_dir, str(cat))
#             if not osp.isdir(cat_dir):
#                 os.mkdir(cat_dir)
#             fname = f.replace(".jpg", f"_itemcrop{cat}.jpg")
#             cropped.save(osp.join(cat_dir, fname))
#             print(f"cropped: {fname}")


# if __name__ == "__main__":

#     parser = argparse.ArgumentParser()

#     parser.add_argument("--frame_dir", required=True)
#     parser.add_argument("--bbox_file", required=False)
#     parser.add_argument("--out_dir", type=str, required=False)
#     parser.add_argument("--min_thresh", type=float, required=False, default=0.7)

#     args = parser.parse_args()


#     with open(args.bbox_file, "r") as input:
#         boxes = json.load(input)
#         boxes = filters.chunk_items(boxes)
#         boxes = filters.process_boxes(boxes, min_thresh=args.min_thresh)

#         if not osp.isdir(args.out_dir):
#             os.makedirs(args.out_dir)

#         crop_boxes(boxes, args.frame_dir, args.out_dir)


def main(args):
    with open(args.bbox_file, "r") as input:
        boxes = json.load(input)

        img_dict = {x['id']: x['file_name'] for x in boxes['images']}
        for annot in boxes['annotations']:
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
            # print(f"cropped: {fname}")


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--bbox_file")
    parser.add_argument("--output_dir")

    args = parser.parse_args()


    main(args)