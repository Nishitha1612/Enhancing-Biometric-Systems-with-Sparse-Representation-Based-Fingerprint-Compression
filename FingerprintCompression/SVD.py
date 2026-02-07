  
import io
from PIL import Image
import numpy
import matplotlib.pyplot as plt
import cv2
from collections import defaultdict
import os

img_pixels = defaultdict(list) #define dictionary for svd compression
global height
global width

def SVDCompress(compressed_image):
    dictionary_size = 256
    dictionary_arr = dict((i, chr(i)) for i in range(dictionary_size))
    results = io.StringIO()
    pixel = chr(compressed_image.pop(0))
    results.write(pixel)
    for m in compressed_image:
        if m in dictionary_arr:
            entry_pixel = dictionary_arr[m]
        elif m == dictionary_size:
            entry_pixel = pixel + pixel[0]
        else:
            raise ValueError('Bad compression m: %s' % m)
        results.write(entry_pixel)
 
        # Adding pixel to the dictionary.
        dictionary_arr[dictionary_size] = pixel + entry_pixel[0]
        dictionary_size += 1
        pixel = entry_pixel
    return results.getvalue()


def SVDCompressDict(uncompressed_image):
    dictionary_size = 256
    dictionary_arr = dict((chr(i), i) for i in range(dictionary_size))
    pixel = ""
    results = []
    for chars in uncompressed_image:
        pixel_chars = pixel + chars
        if pixel_chars in dictionary_arr:
            pixel = pixel_chars
        else:
            results.append(dictionary_arr[pixel])
            dictionary_arr[pixel_chars] = dictionary_size
            dictionary_size += 1
            pixel = chars

    new_dictionary = list(dictionary_arr.items())
    if pixel:
        results.append(dictionary_arr[pixel])
    return results

def LosslessEncodeImage(codes,image_name):
    pixel_list = []
    for code in codes:
        pixel_list.append(ord(code))
    
    arr = numpy.asarray(pixel_list)
    img = arr.reshape(height,width)
    print(img.shape)

    orig = numpy.zeros((height,width,3))
    for i in range(width):
        for j in range(height):
            value = int(img[j,i])
            values = img_pixels.get(str(i)+","+str(j))
            if values is not None:
                values = values[0]
                r = values[0]
                g = values[1]
                b = values[2]
                orig[j][i][0] = b
                orig[j][i][1] = g
                orig[j][i][2] = r
    cv2.imwrite(image_name, orig,[cv2.IMWRITE_JPEG_QUALITY, 45])
    img = cv2.imread(image_name)            
    

    
def compressImage(uncompress_image):
    compress_image = SVDCompressDict(uncompress_image)
    arr = numpy.asarray(compress_image)
    arr1 = numpy.zeros(10000)
    for i in range(len(arr1)):
        arr1[i] = arr[i]
    compress_image = SVDCompress(compress_image)
    LosslessEncodeImage(compress_image,'compress/Compress.jpg')


def getImagePixels(image_path):
    global height
    global width
    input_image = Image.open(image_path)
    pixels = input_image.load() 
    widths, heights = input_image.size
    width = widths
    height = heights
    pixels_arr = []
    for i in range(widths):
        for j in range(heights):
            color_pixel = pixels[i, j]
            gray_value = int(round(sum(color_pixel) / float(len(color_pixel))))
            img_pixels[str(i)+","+str(j)].append(color_pixel)
            pixels_arr.append(gray_value)
     
    return pixels_arr

def compression(input_image):
    img_pixels.clear()
    pixel_values = []
    for p in getImagePixels(input_image):
        pixel_values.append(p)
    pixelString = []
    String_pixel = ""
    for f in pixel_values:
        pixelString.append(chr(f))
    for ps in pixelString:
        String_pixel +=str(ps)
    compressImage(String_pixel)



    
