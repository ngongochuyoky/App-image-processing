import cv2 as cv
from tkinter import *
from PIL import Image, ImageTk
from tkinter.font import Font
from tkinter import filedialog
from os import path
import numpy as np
import scipy.misc
from scipy import ndimage
import matplotlib.pyplot as plt

root = Tk()
root.title("Xử lý ảnh")
root.geometry("1250x700")
root.maxsize(1250, 700)

temp_img = None

# Image box before
# Open Img
pic_default = Image.open('./Image/img_1.png')

# convert images to ImageTK format
img_def = ImageTk.PhotoImage(pic_default)
# tieu de anh truoc xu ly
after_name = Label(root, text="Anh đã chọn", fg="#000", bd=0, bg="pink")
after_name.config(font=("Arial", 16, "bold"))
after_name.grid(column=0, row=1, columnspan=2, padx=10, pady=10)
# anh truoc xu ly
box_img_before = Label(root, image=img_def, width=450,
                       height=450, bg="#303030")
box_img_before.grid(column=0, row=2, columnspan=2, padx=10, pady=10)

# tiêu đề ảnh sau khi lọc
after_name = Label(root, text="Ảnh đã lọc", fg="#000", bd=0, bg="pink")
after_name.config(font=("Arial", 16, "bold"))
after_name.grid(column=2, row=1, columnspan=2, padx=10, pady=10)

# Ảnh đã lọc
box_img_after = Label(root, image=img_def, width=450,
                      height=450, bg="#303030")
box_img_after.grid(column=2, row=2, columnspan=2, padx=10, pady=10)


def clear():
    pic_default = Image.open('./Image/img_1.png')
    # chuyển đổi hình ảnh sang định dạng ImageTK
    img_def = ImageTk.PhotoImage(pic_default)
    # đặt hình ảnh thành Nhãn mặc định trước
    box_img_before.configure(image=img_def)
    box_img_before.image = img_def

    # đặt hình ảnh thành Nhãn mặc định sau
    box_img_after.configure(image=img_def)
    box_img_after.image = img_def
    return 0


def select():
    global path, temp_img

    path = filedialog.askopenfilename()

    if len(path) > 0:
        # load the image from disk
        img = cv.imread(path)
        temp_img = path
        # Convert img to RGB
        img = cv.cvtColor(img, cv.COLOR_BGR2RGB)

        # convert images to PIL format
        img = Image.fromarray(img)

        # resize Image
        resize_bf = img.resize((450, 450), Image.ANTIALIAS)

        # convert images to ImageTK format
        img_bf = ImageTk.PhotoImage(resize_bf)

        # set image to Label
        box_img_before.configure(image=img_bf)
        box_img_before.image = img_bf
    return 0
#Tạo ra hình ảnh với các cạnh
def Laplacian(input_image):
    im = cv.imread(input_image, 0)
    temp = im.copy()
    # print(im.shape[0],im.shape[1])
    for i in range(1, im.shape[0]-1):
        for j in range(1, im.shape[1]-1):
            A = (4*im.item(i, j)-im.item(i, j+1) -
                 im.item(i+1, j)-im.item(i-1, j)-im.item(i, j-1))
            #B = abs(im.item(i-1,j-1)+im.item(i,j-1)+im.item(i-1,j)-im.item(i+1,j+1)-im.item(i,j+1)-im.item(i+1,j))
            #mag = (A*A + B*B)**(.5)
            if(A < 0):
                temp.itemset((i, j), 0)
            elif(A > 255):
                temp.itemset((i, j), 255)
            else:
                temp.itemset((i, j), A)

    img_path = "Laplacian.jpg"
    cv.imwrite(img_path, temp)

    # resize Image
    resize_bf = Image.open(img_path).resize((450, 450), Image.ANTIALIAS)
    # # convert images to ImageTK format
    img = ImageTk.PhotoImage(resize_bf)
    # set image to Label
    box_img_after.configure(image=img)
    box_img_after.image = img
    return


def Gray_Scale(input_image):
    gray_img = Image.open(input_image)
    pixel_val = gray_img.load()
    print(pixel_val[0, 0])
    for i in range(gray_img.size[0]):
        for j in range(gray_img.size[1]):
            sum = 0
            for k in range(0, 3):
                sum += pixel_val[i, j][k]
            pixel_val[i, j] = (sum//3, sum//3, sum//3)
    img_path = "Gray.jpg"
    gray_img.save(img_path)
    # resize Image
    resize_bf = Image.open(img_path).resize((450, 450), Image.ANTIALIAS)
    # # convert images to ImageTK format
    img = ImageTk.PhotoImage(resize_bf)
    # set image to Label
    box_img_after.configure(image=img)
    box_img_after.image = img
    return


def Histogram(input_image):
    im = cv.imread(input_image)
    # tính toán giá trị trung bình từ các kênh RGB và làm phẳng thành mảng 1D
    vals = im.mean(axis=2).flatten()
    # plot histogram with 255 bins
    b, bins, patches = plt.hist(vals, 255)
    plt.xlim([0, 255])
    plt.show()
    return


def Binary(input_image):
    hist = []
    for i in range(0, 377):
        hist.append(0)
    binary_pt_image = Image.open(input_image)
    pixel_val = binary_pt_image.load()

    for i in range(binary_pt_image.size[0]):
        for j in range(binary_pt_image.size[1]):
            sum = 0
            for k in range(0, 3):
                sum += pixel_val[i, j][k]
            sum = sum//3
            # print(sum)
            hist[sum] += 1
    #percentage = 30
    threshold_pixels = binary_pt_image.size[0]*binary_pt_image.size[1]*0.6
    print(binary_pt_image.size[0]*binary_pt_image.size[1])
    print(threshold_pixels)

    for i in range(376, -1, -1):

        sum += hist[i]
        if(sum > threshold_pixels):
            threshold_value = i
            break
    print(threshold_value)
    for i in range(binary_pt_image.size[0]):
        for j in range(binary_pt_image.size[1]):
            sum = 0
            for k in range(0, 3):
                sum += pixel_val[i, j][k]
            sum = sum//3
            if(sum > threshold_value):
                pixel_val[i, j] = (255, 255, 255)
            else:
                pixel_val[i, j] = (0, 0, 0)

    img_path = "BinaryPT.jpg"
    binary_pt_image.save(img_path)
    # resize Image
    resize_bf = Image.open(img_path).resize((450, 450), Image.ANTIALIAS)
    # # convert images to ImageTK format
    img = ImageTk.PhotoImage(resize_bf)
    # set image to Label
    box_img_after.configure(image=img)
    box_img_after.image = img
    return


# button select
btn_select = Button(root, text="Select Image", font=(
    ("Arial"), 10, 'bold'), bg='#fff', fg='#000', command=select)
btn_select.grid(column=4, row=1)

# button clear
btn_clear = Button(root, text="Clear Image", font=(
    ("Arial"), 10, 'bold'), bg='#fff', fg='#000', command=clear)
btn_clear.grid(column=5, row=1)

# button quit
btn_cls = Button(root, text="Quit", font=(
    ("Arial"), 10, 'bold'), bg='#fff', fg='#000', command=root.quit)
btn_cls.grid(column=6, row=1)

# button Laplacian
btn_Laplacian = Button(root, text="Laplacian", font=(
    ("Arial"), 10, 'bold'), bg='#fff', fg='#000', command=lambda: Laplacian(temp_img))
btn_Laplacian.grid(column=4, row=0)

# button Gray Scale
btn_Gray_Scale = Button(root, text="Gray Scale", font=(
    ("Arial"), 10, 'bold'), bg='#fff', fg='#000', command=lambda: Gray_Scale(temp_img))
btn_Gray_Scale.grid(column=5, row=0)

# button Histogram
btn_Histogram = Button(root, text="Histogram", font=(
    ("Arial"), 10, 'bold'), bg='#fff', fg='#000', command=lambda: Histogram(temp_img))
btn_Histogram.grid(column=6, row=0)

# button Sobel
btn_Binary = Button(root, text="Binary", font=(
    ("Arial"), 10, 'bold'), bg='#fff', fg='#000', command=lambda: Binary(temp_img))
btn_Binary.grid(column=7, row=0)

root.mainloop()
