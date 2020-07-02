# PCL to Tex Converter
This repository contains a simple python3 script that generates `Tik-z` picture for the given indices of the pointcloud dataset. The provided dataset(numpy `*.npy` files) are from `ModelNet40` dataset(subsampled to 1024 points per model).
<p align="center"><img src="https://github.com/salehjg/pointcloud_to_tikz_converter/blob/master/build/top_index1.png?raw=true" /></p>

# Usage
Just run the script with:
```buildoutcfg
python3 convert_pcl_to_tikz.py 1 2
```
The first argument is the starting index and the second one is the stopping index. After the script has finished running, the output files(compiled PDFs and their `Tex` files) will be available in the `build` directory.