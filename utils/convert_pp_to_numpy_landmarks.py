"""
Command to run this file:
python3 convert_pp_to_numpy_landmarks.py \
    --pp_directory <path_to_pp_landmarks_directory_files> \
    --npy_directory <path_to_npy_output_directory>
"""
import numpy as np
import os
import xml.etree.ElementTree as ET
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="Script to convert the PP landmarks to npy")
    parser.add_argument('--pp_directory', '-pp', required=True,
                        help="Path to the input pp files directory")
    parser.add_argument('--npy_directory', '-nd', required=True,
                        help="Path to store the npy output files")
    args = parser.parse_args()
    if not os.path.exists(args.pp_directory):
        raise RuntimeError("PP directory is missing")
    if os.path.exists(args.npy_directory):
        raise RuntimeError("Output npy files directory already exists!")
    os.makedirs(args.npy_directory)

    return args

class XML_to_Numpy_Converter():
    def __init__(self, xml_file_path):
        self.xml_file_path = xml_file_path

    def get_coords(self):
        mytree = ET.parse(self.xml_file_path)
        root = mytree.getroot()
        all_points = root.findall('point')
        points = []
        for point in all_points:
            attr = point.attrib
            points.append([int(attr['name']), float(attr['x']), float(attr['y']), float(attr['z'])])
        
        points = sorted(points, key=lambda x:x[0])
        final_result = np.array([[x, y, z] for _, x, y, z in points])
        return final_result

if __name__ == "__main__":
    args = parse_args()
    pp_files = [filename for filename in os.listdir(args.pp_directory) if os.path.splitext(filename)[1] == '.pp']
    for filename in pp_files:
        input_file_path = os.path.join(args.pp_directory, filename)
        output_filename = os.path.splitext(filename)[0]
        output_file_path = os.path.join(args.npy_directory, output_filename)
        np.save(output_file_path, XML_to_Numpy_Converter(input_file_path).get_coords())