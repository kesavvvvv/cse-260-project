"""
Command to run this file:
python3 convert_pp_to_numpy_landmarks.py <path_to_the_input_pp_file>
"""
import numpy as np
import os
import sys
import xml.etree.ElementTree as ET

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
    input_file_path = sys.argv[1]
    output_file_path = os.path.split(input_file_path)[1]
    np.save(output_file_path, XML_to_Numpy_Converter(input_file_path).get_coords())