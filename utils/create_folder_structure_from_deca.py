import argparse
import glob
import os
import shutil

def parse_args():
    parser = argparse.ArgumentParser(description="Script to create the predicted mesh folder structure")
    parser.add_argument("--deca_pred_dir", "-pd", type=str, required=True,
                        help="Path to the predicted mesh directory")
    parser.add_argument("--valid_imgs", "-vi", type=str,
                        default="/data/datasets/now_dataset/imagepathsvalidation.txt",
                        help="Path to the NoW dataset validation txt file")
    parser.add_argument("--pred_ready_dir", "-pr", type=str,
                        default="prediction_mesh_directory",
                        help="Path to the predicted mesh directory")
    args = parser.parse_args()
    if not os.path.exists(args.deca_pred_dir):
        raise RuntimeError("Deca prediction directory doesn't exist")
    if not os.path.exists(args.valid_imgs):
        raise RuntimeError("NoW validation images filepath doesn't exist")
    if os.path.exists(args.pred_ready_dir):
        msg = "Output prediction mesh directory already present."
        raise RuntimeError(msg)

    os.makedirs(args.pred_ready_dir)

    return args

def read_the_validation_file(valid_file_path):
    data = {}
    with open(valid_file_path) as reader:
        for line in reader:
            line = line.strip()
            folders, img = os.path.split(line)
            data[img] = folders
    return data

def get_deca_images_dirs(deca_pred_dir, valid_img_folder_data):
    deca_prediction_directories = {}
    for file_dir_name in os.listdir(deca_pred_dir):
        if os.path.isdir(os.path.join(deca_pred_dir, file_dir_name)):
            if file_dir_name + '.jpg' in valid_img_folder_data:
                deca_prediction_directories[os.path.join(deca_pred_dir, file_dir_name)] = \
                    [file_dir_name + ".obj", file_dir_name + "_flame_kpt3d.npy",
                     file_dir_name + ".obj", file_dir_name + ".npy"]
    return deca_prediction_directories

def main(args):
    valid_imgs_folder_data = read_the_validation_file(args.valid_imgs)
    deca_prediction_directories = get_deca_images_dirs(args.deca_pred_dir, valid_imgs_folder_data)
    for img, folder in valid_imgs_folder_data.items():
        os.makedirs(os.path.join(args.pred_ready_dir, folder), exist_ok=True)
        img_path = os.path.join(args.deca_pred_dir, os.path.splitext(img)[0])
        detail_obj_file, flame_kpt_file, out_obj_file, out_kpt_file = deca_prediction_directories[img_path]
        detail_obj_file_path = os.path.join(img_path, detail_obj_file)
        flame_kpt_file_path = os.path.join(img_path, flame_kpt_file)
        out_detail_obj_file = os.path.join(args.pred_ready_dir, folder, out_obj_file)
        out_flame_kpt_file = os.path.join(args.pred_ready_dir, folder, out_kpt_file)
        shutil.copy(detail_obj_file_path, out_detail_obj_file)
        shutil.copy(flame_kpt_file_path, out_flame_kpt_file)



if __name__ == "__main__":
    main(parse_args())