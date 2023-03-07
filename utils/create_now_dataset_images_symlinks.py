"""
python3 create_now_dataset_images_symlinks.py \
    -vf /data/datasets/now_dataset/imagepathsvalidation.txt \
    -dp /data/datasets/now_dataset/ \
    -od /MICA/demo/now_dataset/
"""

import argparse
import os

Iphone_Pictures_Path = "./NoW_Dataset/final_release_version/iphone_pictures/"
cmd = "ln -s {} {}"

def parse_args():
    parser = argparse.ArgumentParser(description="NoW dataset images symlink creator")
    parser.add_argument("--validation_file", "-vf", type=str, required=True,
                        help="Path to the imagesvalidation.txt")
    parser.add_argument("--dataset_path", "-dp", type=str, required=True,
                        help="Root path of the NoW dataset folder")
    parser.add_argument("--output_dir", "-od", type=str, default="now_dataset",
                        help="Output directory path where symlinks will be created")
    args = parser.parse_args()

    if not os.path.exists(args.validation_file):
        raise RuntimeError("Validation file path doesn't exists")
    if not os.path.exists(args.dataset_path):
        raise RuntimeError("NoW dataset path is missing")
    if os.path.exists(args.output_dir):
        raise RuntimeError("Output directory already exists")

    os.makedirs(args.output_dir)
    return args

def main(args):
    imgs_dir = os.path.join(args.dataset_path, Iphone_Pictures_Path)
    cmds = []
    with open(args.validation_file) as reader:
        for line in reader:
            line = line.strip()
            inp_img_path = os.path.abspath(
                        os.path.join(
                            args.dataset_path, Iphone_Pictures_Path, line))
            img_name = os.path.split(inp_img_path)[1]
            out_img_path = os.path.join(os.path.abspath(args.output_dir), img_name)
            cmds.append(cmd.format(inp_img_path, out_img_path))
    for cmd_line in cmds:
        os.system(cmd_line)

if __name__ == "__main__":
    main(parse_args())