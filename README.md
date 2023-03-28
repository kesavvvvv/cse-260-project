# cse-260-project

This repository contains the submodules that are relevant to our project on 3D Face Reconstruction using iPhone's TrueDepth Sensor. Please find the [project report](docs/report.pdf) and [presentation slides](docs/presentation_slides.pdf) in the docs directory.

### Clone the repository

```bash
git clone --recurse-submodules https://github.com/kesavvvvv/cse-260-project.git
```

### Creating the prediction folder structure for NoW Evaluation

This script will convert the output of the models MICA and DECA to the folder structure that is required for the NoW Evaluation pipeline. The details about the folder structure for the NoW benchmark is present in this [link](https://now.is.tue.mpg.de/download.php).

```bash
python3 create_folder_structure.py \
    --pred_dir <path_to_the_predicted_results> \
    --valid_imgs <path_to_the_now_evaluation_validation_images_path> \
    --pred_ready_dir <output_path_for_the_now_folder_structure> \
    --model <type_of_model>
```

You can find the detailed instructions to run the NoW evaluation pipeline in this [link](https://github.com/soubhiksanyal/now_evaluation).

### Conversion of the Landmarks in various formats

#### PP to Numpy

This script converts the PP points to the .npy format. It is helpful when you want to convert the PP points marked using the Meshlab to the Numpy array.

```bash
cd utils
python3 convert_pp_to_numpy_landmarks.py \
    --pp_directory <path_to_pp_landmarks_directory_files> \
    --npy_directory <path_to_npy_output_directory>
```

#### Text to PP

This script converts the landmarks stored in the text file to the PP point format.

```bash
cd utils
python3 convert_landmarks_txt_to_pp_points.py \
    --model deca
    --landmarks_dir <path_to_the_stored_landmarks_dir> \
    --output_dir <path_to_store_the_pp_points>
```

#### Symlink creation

This script will help to create the symlinks to the NoW validation dataset images. Models such as DECA and MICA require a directory of images to perform inference. So, one must create a directory of input images prior to feeding it to these models to the inference pipeline. Therefore, this script will only create symbolic links to the images that are present in the validation dataset directory.

```bash
cd utils
python3 create_now_dataset_images_symlinks.py \
    -vf <path to the imagepathsvalidation.txt file> \
    -dp <root directory of the download NoW dataset> \
    -od <output directory to create symlinks of NoW dataset validation images>
```