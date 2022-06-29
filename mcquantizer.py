import argparse
import math
import colorsys
import numpy as np
from skimage.io import imread, imsave


def convert_rgb_to_hsv(red, green, blue):
    # rgb normal: range (0-255, 0-255, 0.255)

    # get rgb percentage: range (0-1, 0-1, 0-1 )
    red_percentage = red / float(255)
    green_percentage = green / float(255)
    blue_percentage = blue / float(255)

    # get hsv percentage: range (0-1, 0-1, 0-1)
    color_hsv_percentage = colorsys.rgb_to_hsv(
        red_percentage, green_percentage, blue_percentage)

    # get normal hsv: range (0-360, 0-255, 0-255)
    color_h = round(360*color_hsv_percentage[0])
    color_s = round(100*color_hsv_percentage[1])
    color_v = round(100*color_hsv_percentage[2])
    color_hsv = (color_h, color_s, color_v)

    print('color_hsv: ', color_hsv)


def median_cut_quantize(img, img_arr):
    global color_index
    # when it reaches the end, color quantize
    r_average = np.mean(img_arr[:, 0])
    g_average = np.mean(img_arr[:, 1])
    b_average = np.mean(img_arr[:, 2])
    
    for data in img_arr:
        sample_img[data[3]][data[4]] = [r_average, g_average, b_average]
        
    print(f"\n\nColor #{color_index} \nColor_RGB: ({r_average:.0f},{g_average:.0f},{b_average:.0f})")
    convert_rgb_to_hsv(r_average, g_average, b_average)
    color_index += 1


def split_into_buckets(img, img_arr, depth):
    if len(img_arr) == 0:
        return

    if depth == 0:
        median_cut_quantize(img, img_arr)
        return

    r_range = np.max(img_arr[:, 0]) - np.min(img_arr[:, 0])
    g_range = np.max(img_arr[:, 1]) - np.min(img_arr[:, 1])
    b_range = np.max(img_arr[:, 2]) - np.min(img_arr[:, 2])

    space_with_highest_range = 0

    if g_range >= r_range and g_range >= b_range:
        space_with_highest_range = 1
    elif b_range >= r_range and b_range >= g_range:
        space_with_highest_range = 2
    elif r_range >= b_range and r_range >= g_range:
        space_with_highest_range = 0

    # sort the image pixels by color space with highest range
    # and find the median and divide the array.
    img_arr = img_arr[img_arr[:, space_with_highest_range].argsort()]
    median_index = int((len(img_arr) + 1) / 2)

    # split the array into two blocks
    split_into_buckets(img, img_arr[0:median_index], depth - 1)
    split_into_buckets(img, img_arr[median_index:], depth - 1)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Perform Median Cut Color Quantization on image.')
    parser.add_argument('-c', '--colors', type=int,
                        help='Number of colors needed in power of 2, ex: for 16 colors pass 4 because 2^4 = 16')
    parser.add_argument('-i', '--input', type=str,
                        help='path of the image to be quantized')
    parser.add_argument('-o', '--output', type=str,
                        help='output path for the quantized image')

    # get the arguments
    args = parser.parse_args()

    # get the values from the arguments
    colors = args.colors
    print("reducing the image to {} color palette".format(int(math.pow(2, colors))))

    output_path = args.output
    input_path = args.input

    # read the image
    sample_img = imread(input_path)
    
    color_index = 1

    flattened_img_array = []
    for rindex, rows in enumerate(sample_img):
        for cindex, color in enumerate(rows):
            flattened_img_array.append(
                [color[0], color[1], color[2], rindex, cindex])

    flattened_img_array = np.array(flattened_img_array)

    # start the splitting process
    split_into_buckets(sample_img, flattened_img_array, colors)

    # save the final image
    imsave(output_path, sample_img)
