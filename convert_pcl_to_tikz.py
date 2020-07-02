import numpy as np
import subprocess
import os
import sys


class PclTikzConverter:
    def __init__(self, npy_path_data, npy_path_labels, tex_template_path):
        self.dataset_names = ["Airplane",
                              "Bathtub",
                              "Bed",
                              "Bench",
                              "Bookshelf",
                              "Bottle",
                              "Bowl",
                              "Car",
                              "Chair",
                              "Cone",
                              "Cup",
                              "Curtain",
                              "Desk",
                              "Door",
                              "Dresser",
                              "Flower Pot",
                              "Glass Box",
                              "Guitar",
                              "Keyboard",
                              "Lamp",
                              "Laptop",
                              "Mantel",
                              "Monitor",
                              "Night Stand",
                              "Person",
                              "Piano",
                              "Plant",
                              "Radio",
                              "Range Hood",
                              "Sink",
                              "Sofa",
                              "Stairs",
                              "Stool",
                              "Table",
                              "Tent",
                              "Toilet",
                              "TV Stand",
                              "Vase",
                              "Wardrobe",
                              "Xbox"]
        self.dataset_pcl = np.load(npy_path_data)
        self.dataset_label = np.load(npy_path_labels)
        self.dataset_count = self.dataset_pcl.shape[0]
        self.dataset_n = self.dataset_pcl.shape[1]
        self.tex_template_path = tex_template_path
        with open(tex_template_path, "r") as f:
            self.tex_template = f.read()

    def get_pcl_string(self, index, div=1, x_mul=-10.0, y_mul=10.0, z_mul=-10.0):
        if self.tex_template_path == "template1.tex.in":
            pass
        else:
            if self.tex_template_path == "template2.tex.in":
                return self.get_pcl_string_template2(index, div, x_mul, y_mul, z_mul)

    def get_pcl_string_template2(self, index, div, x_mul, y_mul, z_mul):
        def limit_rgb(val):
            if val > 255:
                return 255
            if val < 0:
                return 0
            return int(val)

        N = self.dataset_pcl.shape[1] / div
        N = int(N)
        pcl = self.dataset_pcl[index, :, :]
        pcl[:, 0] = pcl[:, 0] * x_mul
        pcl[:, 1] = pcl[:, 1] * y_mul
        pcl[:, 2] = pcl[:, 2] * z_mul

        x_min = np.min(pcl[:, 0])
        x_max = np.max(pcl[:, 0])
        x_range = x_max - x_min

        y_min = np.min(pcl[:, 1])
        y_max = np.max(pcl[:, 1])
        y_range = y_max - y_min

        z_min = np.min(pcl[:, 2])
        z_max = np.max(pcl[:, 2])
        z_range = z_max - z_min

        s = ""
        for n in range(N):
            [x, y, z] = pcl[n, :]
            rgb_r = limit_rgb((x - x_min) * 255.0 / x_range)
            rgb_g = limit_rgb((y - y_min) * 255.0 / y_range)
            rgb_b = limit_rgb((z - z_min) * 255.0 / z_range)

            s += '\\node[fill={rgb,255:red,' + str(rgb_r) + '; green,' + str(rgb_g) + '; blue,' + str(
                rgb_b) + '},circle,inner ' \
                         'sep=1.0pt] at ( '

            for i in range(3):
                s += str(pcl[n, i])
                if i != 2:
                    s += ","
            s += ") {};\n"
        return s

    def configure_file(self, src_string, var_string, replacing_string):
        tmpl_parts = src_string.split(var_string)
        return ''.join([tmpl_parts[0], replacing_string, tmpl_parts[1]])

    def generate_tex(self, dataset_index):
        tex_pcl = self.get_pcl_string(dataset_index, 1)

        model_class_idx = self.dataset_label[dataset_index, 0]
        model_classname = self.dataset_names[model_class_idx]

        fname = ''.join(['build/top_index', str(dataset_index), '.tex'])
        fname2 = ''.join(['top_index', str(dataset_index)])

        output_tex_string = self.tex_template
        output_tex_string = self.configure_file(output_tex_string, "$PCL$", tex_pcl)
        output_tex_string = self.configure_file(output_tex_string, "$PCLNAME$", model_classname)
        output_tex_string = self.configure_file(output_tex_string, "$PCL_N$", str(self.dataset_n))
        file_out = open(fname, "w")
        file_out.write(output_tex_string)
        file_out.close()
        return fname2


def main():
    if len(sys.argv) != 3:
        print("Error, wrong args.")
        print("Usage: python3 convert_pcl_to_tikz.py <MODEL START INDEX> <MODEL STOP INDEX>")
        print("Make sure the folder \"build\" is present in the current directory.")
        print("Make sure to run the script from the same directory that the script is located.")
        sys.exit(1)

    batch_start = int(sys.argv[1])
    batch_stop = int(sys.argv[2])
    assert batch_stop > batch_start

    converter = PclTikzConverter(
        "modelnet40_B2048_pcl.npy",
        "modelnet40_B2048_labels_int32.npy",
        "template2.tex.in"
    )
    for i in range(1, 2):
        fname2 = converter.generate_tex(i)
        os.system(''.join(["sh ", os.path.dirname(os.path.realpath(__file__)), "/build_pdf.sh ", fname2]))


main()
