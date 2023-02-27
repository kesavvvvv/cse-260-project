"""
Command to run this file:
python3 convert_landmarks_txt_to_pp_points.py \
    --model deca
    --landmarks_dir <path_to_the_stored_landmarks_dir> \
    --output_dir <path_to_store_the_pp_points>
"""

import argparse
import os

class IgnorePoints():
    def __init__(self, model):
        self.model = model
        self.deca_ignore_pts = [33, 36, 39, 42, 45, 48, 54]
        self.mica_ignore_pts = []
    def get_points(self):
        if self.model == 'deca':
            return self.deca_ignore_pts
        elif self.model == 'mica':
            raise NotImplementedError('MICA points to ignore is not implmented!')

def parse_args():
    parser = argparse.ArgumentParser(description = "Picked points file converter")
    parser.add_argument("--model", "-m", type=str, default="deca",
                        help="Type of model")
    parser.add_argument("--landmarks_dir", "-ld", type=str, required=True,
                        help="Path to the predicted landmarks_dir")
    parser.add_argument("--output_dir", "-od", type=str, default="output",
                        help="Path to the output directory to stored the converted files")
    args = parser.parse_args()
    if not os.path.exists(args.landmarks_dir):
        raise RuntimeError("Landmarks directory doesn't exist")
    if os.path.exists(args.output_dir):
        raise RuntimeError("Output directory already exists! Change the output directory.")
    os.makedirs(args.output_dir)
    return args

args = parse_args()

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

points_to_ignore = IgnorePoints(model=args.model).get_points()
point_format =  '<point x="{}" y="{}" z="{}" active="1" name="{}"/>'

all_landmarks = [filename for filename in os.listdir(args.landmarks_dir) 
                    if os.path.splitext(filename)[1] == ".txt"]
for landmark_file in all_landmarks:
    points = []
    with open(os.path.join(args.landmarks_dir, landmark_file), 'r') as reader:
        for idx, line in enumerate(reader):
            if idx not in points_to_ignore:
                continue
            line = list(map(float, line.strip().split())) + [idx]
            points.append(line)
    point_str = "\t\t"
    for pt in points:
        point_str += point_format.format(pt[0], pt[1], pt[2], pt[4])
        point_str += "\n\t\t"
    file_format = pp_format.format(landmark_file, point_str)
    with open(os.path.join(
            args.output_dir, os.path.splitext(landmark_file)[0] + ".pp"), 'w'
        ) as writer:
        writer.write(file_format)