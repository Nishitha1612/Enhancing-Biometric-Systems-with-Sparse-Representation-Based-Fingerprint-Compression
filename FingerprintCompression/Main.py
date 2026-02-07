from matplotlib import pyplot as plt
from tkinter import *
from tkinter import simpledialog
from tkinter.filedialog import askopenfilename
import tkinter
from tkinter import filedialog
import os
import SVD
from SVD import *
import cv2

root = tkinter.Tk()
root.title("FINGERPRINT COMPRESSION BASED ON SPARSE REPRESENTATION")
root.geometry("1000x500")

global filename
global normal
global compress


def uploadImage():
    global filename
    filename = askopenfilename(initialdir = "sample_finger_images")
    trainpath.config(text=filename+' loaded')

def compressImage():

    global normal

    global compress
    SVD.compression(filename)
    normal = os.stat(filename).st_size
    compress = os.stat('compress/Compress.jpg').st_size

    original_image = cv2.imread(filename)
    original_image = cv2.resize(original_image,(500,500))
    compress_image = cv2.imread('compress/Compress.jpg')
    compress_image = cv2.resize(compress_image,(500,500))
    cv2.imshow("Original Image & its Size : "+str(normal),original_image);
    cv2.imshow("SVD Compress Image & its Size : "+str(compress),compress_image);
    cv2.waitKey();
    
    
def graph():
    height = [normal,compress]
    bars = ('Normal File Size','Compress File Size')
    y_pos = numpy.arange(len(bars))
    plt.bar(y_pos, height)
    plt.xticks(y_pos, bars)
    plt.show()

def close():
    root.destroy()

ttt = Label(root)
ttt.grid(row=0)

ttt1 = Label(root)
ttt1.grid(row=3)

font = ('times', 14, 'bold')
trainpath = Label(root)
trainpath.grid(row=6)
trainpath.config(font=font)

uploadimageButton = Button(root, text="Upload Image", command=uploadImage)
uploadimageButton.grid(row=15)
uploadimageButton.config(font=font)

tt1 = Label(root)
tt1.grid(row=18)

imageButton = Button(root, text="Compress Image using SVD", command=compressImage)
imageButton.grid(row=21)
imageButton.config(font=font)

tt2 = Label(root)
tt2.grid(row=24)

graphButton = Button(root, text="Comparison Graph", command=graph)
graphButton.grid(row=27)
graphButton.config(font=font)

tt3 = Label(root)
tt3.grid(row=30)

closeButton = Button(root, text="Close Application", command=close)
closeButton.grid(row=33)
closeButton.config(font=font)


root.mainloop()
