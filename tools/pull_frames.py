import argparse
import os
import os.path as osp
import random
from shutil import copy

def main(args):
    subj_dirs = list(filter(lambda x: x.startswith("__2"), os.listdir(args.exp_dir)))
    frame_dirs = [osp.join(dir, "cam07_frames_p") for dir in subj_dirs]

    frames = []

    for dir in frame_dirs:
        dir_frames = [osp.join(args.exp_dir, dir, f) for f in os.listdir(osp.join(args.exp_dir, dir))]
        frames.extend(dir_frames)
    
    random.shuffle(frames)

    return frames[:args.num_samples]

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--exp_dir")
    parser.add_argument("--output_dir")
    parser.add_argument("--num_samples", default=2000)

    args = parser.parse_args()

    frames = main(args)

    for f in frames:
        copy(f, args.output_dir)
