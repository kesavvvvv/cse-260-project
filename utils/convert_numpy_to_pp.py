import numpy as np
import os
import xml.etree.ElementTree as ET
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="Script to convert the PP landmarks to npy")
    parser.add_argument('--npy_directory', '-np', required=True,
                        help="Path to the input pp files directory")
    parser.add_argument('--pp_directory', '-pp', required=True,
                        help="Path to store the npy output files")
    args = parser.parse_args()
    if not os.path.exists(args.npy_directory):
        raise RuntimeError("NPY directory is missing")
    if os.path.exists(args.pp_directory):
        raise RuntimeError("Output pp files directory already exists!")
    os.makedirs(args.pp_directory)

    return args

pp_format = """
<!DOCTYPE PickedPoints>
<PickedPoints>
 <DocumentData>
  <DateTime time="18:19:00" date="2018-11-03"/>
  <User name="utkarsh"/>
  <DataFileName name="{}"/>
  <templateName name="new Template"/>
 </DocumentData>
    {}
</PickedPoints>
"""

point_format =  '<point x="{}" y="{}" z="{}" active="1" name="{}"/>'

args = parse_args()

all_files = [filename for filename in os.listdir(args.npy_directory)
                if os.path.splitext(filename)[1] == '.npy']
for filename in all_files:
    filepath = os.path.join(args.npy_directory, filename)
    pp_out_file_path = os.path.join(args.pp_directory, os.path.splitext(filename)[0] + '.pp')
    data = np.load(filepath).tolist()
    pp_points = "\t\t"
    with open(pp_out_file_path, 'w') as writer:
        for idx, point in enumerate(data):
            temp_point = point_format.format(point[0], point[1], point[2], idx)
            pp_points += temp_point
            pp_points += "\n\t\t"
        writer.write(pp_format.format(os.path.splitext(filename)[0], pp_points))

