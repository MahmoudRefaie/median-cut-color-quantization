from mcquantizer import quantize
import argparse
import math
from skimage.io import imread, imsave
import numpy as np
import glob


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Perform Median Cut Color Quantization on batch of images in the same folder.')
    parser.add_argument('-c', '--colors', type=int,
                        help='Number of colors needed in power of 2, ex: for 16 colors pass 4 because 2^4 = 16')
    

    # get the arguments
    args = parser.parse_args()

    # get the values from the arguments
    colors = args.colors
    print("reducing the image to {} color palette".format(int(math.pow(2, colors))))
    
    # clear log.txt file
    with open('log.txt','a') as file:
        file.seek(0)
        file.truncate()
    
    jpg_file_paths = glob.glob(r"*.jpg")
    for i, jpg_file_path in enumerate(jpg_file_paths):
        # open log.txt file and add image name
        with open('log.txt','a') as file:
            file.write(f"\nImage: {jpg_file_path}\n")
        
        # read the image
        sample_img = imread(jpg_file_path)

        flattened_img_array = []
        for rindex, rows in enumerate(sample_img):
            for cindex, color in enumerate(rows):
                flattened_img_array.append(
                    [color[0], color[1], color[2], rindex, cindex])

        flattened_img_array = np.array(flattened_img_array)
        
        # start the splitting process
        quantize(sample_img, flattened_img_array, colors)
        

        # save the final image
        imsave(jpg_file_path[:-4]+"q.jpg", sample_img)
