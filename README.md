# Median cut Color Quantization Algorithm implementation
The code supplements the description provided in the article https://muthu.co/reducing-the-number-of-colors-of-an-image-using-median-cut-algorithm/

## Usage
### Single image
```
usage: mcquantizer.py [-h] [-c COLORS] [-i INPUT] [-o OUTPUT]

Perform Median Cut Color Quantization on image.

optional arguments:
  -h, --help            show this help message and exit
  -c COLORS, --colors COLORS
                        Number of colors needed in power of 2, ex: for 16
                        colors pass 4 because 2^4 = 16
  -i INPUT, --input INPUT
                        path of the image to be quantized
  -o OUTPUT, --output OUTPUT
                        output path for the quantized image



Example:  python3 mcquantizer.py -c 6 -o /path/girl64.jpg -i /path/girl.jpg
```
### Batch of images 
```
usage: batch-convert-all-in-folder.py [-h] [-c COLORS]

Perform Median Cut Color Quantization on batch of images in the same folder.

options:
  -h, --help            show this help message and exit
  -c COLORS, --colors COLORS
                        Number of colors needed in power of 2, ex: for 16
                        colors pass 4 because 2^4 = 16

Example:  python3 batch-convert-all-in-folder.py -c 6

```

## Licence
MIT
